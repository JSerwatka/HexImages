from functools import wraps

from django.http.response import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError

import PIL.Image

from img_ocean.models import Image


def test_img_parameters(view):
    """
    Decorator for views that checks  #TODO better docstring
    if the requested img exists and 
    if img height is available in the user's plan.
    
    Stores additional data in the wrapped view:
        original_img: requested image resource
        original_requested: whether the user requested for the original img
        requested_height: height of the requested img
        customer_plan: Plan object of the user
    """


    @wraps(view)
    def wrapper(request, *args, **kwargs):
        # Make sure image id query parameter is correct
        try:
            original_img = Image.objects.get(id=request.GET['id'], owner=request.user)
        except MultiValueDictKeyError:
            return JsonResponse({'error': 'Incorrect URL parameters'})
        except Image.DoesNotExist:
            return JsonResponse({'error': 'Image with this id does not exist or you are not authorized to view it'})
        
        # Get customer's plan restriction
        customer_plan = request.user.customer.plan
        available_heights = [int(str_height) for str_height in customer_plan.img_heights.split(',')]
        original_requested = customer_plan.original_exists and not request.GET.get('height')

        # Get requested height if resizing needed
        if not original_requested:
            # Make sure image height query parameter is correct
            try:    
                requested_height = int(request.GET['height'])
                wrapper.requested_height = requested_height
            except MultiValueDictKeyError:
                return JsonResponse({'error': 'This plan does not support original images'})

            if requested_height not in available_heights:
                return JsonResponse({'error': 'This plan does not support provided image height'})


        wrapper.customer_plan = customer_plan
        wrapper.original_img = original_img
        wrapper.original_requested = original_requested
        
        return view(request, *args, **kwargs)
    return wrapper
        