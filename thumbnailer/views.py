import io
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from urllib.request import urlopen
from django.utils.datastructures import MultiValueDictKeyError

import PIL.Image

from img_ocean.models import Image


def resize(request):
    # Make sure image id query parameter is correct
    try:
        #TODO change path to url
        original_img_url = Image.objects.get(id=request.GET['id']).image.path
    except MultiValueDictKeyError:
        return JsonResponse({'error': 'Incorrect URL parameters'})
    except Image.DoesNotExist:
        return JsonResponse({'error': 'Image with this id does not exist'})
    
    # Get customer's plan restriction
    customer_plan = request.user.customer.plan
    available_heights = [int(str_height) for str_height in customer_plan.img_heights.split(',')]

    # Get the img
    output = io.BytesIO()
    img = PIL.Image.open(original_img_url)
    # Check format - JPG or PNG
    format = img.format 

    # Do not resize if original requested
    if not(customer_plan.original_exists and not request.GET.get('height')):
        # Make sure image height query parameter is correct
        try:    
            requested_height = int(request.GET['height'])
        except MultiValueDictKeyError:
            return JsonResponse({'error': 'Incorrect URL parameters'})

        if requested_height not in available_heights:
            return JsonResponse({'error': 'This plan does not support provided image height'})

        # --- Resize the image ---
        # Calculate width based on fixed height
        hpercent = (requested_height / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        # Resize image and save in a file object
        img = img.resize((wsize, requested_height), PIL.Image.LANCZOS)

    img.save(output, format)
    output.seek(0)

    return HttpResponse(output, content_type=f"image/{format.lower()}")