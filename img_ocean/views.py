from datetime import datetime, timedelta

from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .serializers import ImageSerializer
from .models import ExpiringLink, Image

from thumbnailer.views import ImgParamValidationGenericAPI


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)


class GenerateExpiringLink(ImgParamValidationGenericAPI):
    def get(self, request):
        '''
        View creates new expiring link for an image based on "time" query parameter and returns this link
        '''
        # Validate params
        try:
            self.validate_url_params(request)
        except ValidationError as e:
            return Response({'error': e.message})

        # Check if the customer has expiring links option in their plan
        if not self.customer_plan.expiring_exists:
            return Response({'error': 'This plan does not expiring link generation'})
        
        # Validate time query parameter
        try:
            expiration_time = int(request.GET['time'])
        except MultiValueDictKeyError:
            return Response({'error': 'Incorrect URL parameters'})

        if expiration_time < 300 or expiration_time > 3000:
            return Response({'error': 'Expiration time must be between 300 and 3000 seconds'})

        expiration_date = datetime.utcnow() + timedelta(seconds=expiration_time)
        requested_height = self.requested_height if self.requested_height else 0

        # Create new expiring link
        new_link = ExpiringLink.objects.create(
            image = self.original_img , 
            img_height = requested_height,
            original_img = self.original_requested, 
            expires_on = expiration_date
        )

        expirng_link_url  = reverse('thumbnailer:get_expiring_link', kwargs={'uuid': new_link.id})
        
        return Response({'generated link': request.build_absolute_uri(expirng_link_url)})