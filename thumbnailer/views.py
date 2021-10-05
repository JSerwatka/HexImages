from datetime import datetime

from django.http.response import HttpResponse, JsonResponse

from img_ocean.models import ExpiringLink
from .decorators import test_img_parameters
from .utils import generate_new_img


@test_img_parameters
def resize(request):
    '''
    Resizes img based on query parameters (img id, requested height) 
    and returns HttpResponse of image/<img_format> content type
    '''
    new_img, format = generate_new_img(
        original_img = resize.original_img,
        original_requested = resize.original_requested,
        requested_height = resize.requested_height
    )

    return HttpResponse(new_img, content_type=f"image/{format.lower()}")

def expiring_link(request, uuid):
    '''
    Checks if expiring link expired
    if not returns resized image as HttpResponse of image/<img_format> content type
    '''
    try:
        link = ExpiringLink.objects.get(id=uuid, expires_on__gte=datetime.utcnow())
    except ExpiringLink.DoesNotExist:
        return JsonResponse({'error': 'This link is invalid or expired'})

    new_img, format = generate_new_img(
        original_img = link.image,
        original_requested = link.original_img,
        requested_height = link.img_height
    )

    return HttpResponse(new_img, content_type=f"image/{format.lower()}")