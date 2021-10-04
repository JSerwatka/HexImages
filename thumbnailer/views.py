import io

from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

import PIL.Image

from img_ocean.models import Image
from .decorators import test_img_parameters
from .utils import resize_img_to_height


@test_img_parameters
def resize(request):
    '''
    #TODO docstring resize
    '''


    original_img = resize.original_img
    original_requested = resize.original_requested

    # Get the img
    output = io.BytesIO()
    img = PIL.Image.open(original_img.image.path) #TODO change path to url
    # Check format - JPG or PNG
    format = img.format

    if not original_requested:
        requested_height = resize.requested_height
        img = resize_img_to_height(img, requested_height)

    img.save(output, format)
    output.seek(0)

    return HttpResponse(output, content_type=f"image/{format.lower()}")