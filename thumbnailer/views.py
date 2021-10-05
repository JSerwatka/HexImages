from datetime import datetime

from django.http.response import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from img_ocean.models import ExpiringLink, Image
from .utils import generate_new_img


class ImgParamValidationGenericAPI(GenericAPIView):
    def validate_url_params(self, request):
        """
        Validation method for views that checks
        if the requested img exists and 
        if the img height is available in the user's plan.
        
        Stores additional data in the object:
            original_img: requested image object
            original_requested: whether the user requested for the original img
            requested_height: height of the requested img
            customer_plan: Plan object of the user
        """
        # Make sure image id query parameter is correct
        try:
            original_img = Image.objects.get(id=request.query_params['id'], owner=request.user)
        except MultiValueDictKeyError:
            return Response({'error': 'Incorrect URL parameters'})
        except Image.DoesNotExist:
            return Response({'error': 'Image with this id does not exist or you are not authorized to view it'})
        
        # Get customer's plan restriction
        customer_plan = request.user.customer.plan
        available_heights = [int(str_height) for str_height in customer_plan.img_heights.split(',')]
        original_requested = customer_plan.original_exists and not request.query_params.get('height')

        # Set additional data for the view
        self.requested_height = None
        self.customer_plan = customer_plan
        self.original_img = original_img
        self.original_requested = original_requested

        # Get requested height if resizing needed
        if not original_requested:
            # Make sure image height query parameter is correct
            try:    
                requested_height = int(request.GET['height'])
                self.requested_height = requested_height
            except MultiValueDictKeyError:
                return Response({'error': 'This plan does not support original images'})

            if requested_height not in available_heights:
                return Response({'error': 'This plan does not support provided image height'})


class ResizeImg(ImgParamValidationGenericAPI):
    def get(self, request):
        '''
        Resizes img based on query parameters (img id, requested height) 
        and returns HttpResponse of image/<img_format> content type
        '''
        # Validate params
        self.validate_url_params(request)

        new_img, format = generate_new_img(
            original_img = self.original_img,
            original_requested = self.original_requested,
            requested_height = self.requested_height
        )

        return HttpResponse(new_img, content_type=f"image/{format.lower()}")


class GetExpiringLink(GenericAPIView):
    def get(self, *args, **kwargs):
        '''
        Checks if expiring link expired
        if not returns resized image as HttpResponse of image/<img_format> content type
        '''
        try:
            link = ExpiringLink.objects.get(id=kwargs['uuid'], expires_on__gte=datetime.utcnow())
        except ExpiringLink.DoesNotExist:
            return Response({'error': 'This link is invalid or expired'})

        new_img, format = generate_new_img(
            original_img = link.image,
            original_requested = link.original_img,
            requested_height = link.img_height
        )

        return HttpResponse(new_img, content_type=f"image/{format.lower()}")