from datetime import datetime, timedelta

from django.http.response import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.urls import reverse
from rest_framework import viewsets, permissions

from .serializers import ImageSerializer
from .models import ExpiringLink, Image

from thumbnailer.decorators import test_img_parameters


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)

    # TODO remove in production
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


@test_img_parameters
def generate_expiring_link(request):
    # Check if the customer has expiring links option in their plan
    if not generate_expiring_link.customer_plan.expiring_exists:
        return JsonResponse({'error': 'This plan does not expiring link generation'})
    
    # Validate time query parameter
    try:
        expiration_time = int(request.GET['time'])
    except MultiValueDictKeyError:
        return JsonResponse({'error': 'Incorrect URL parameters'})

    if expiration_time < 300 or expiration_time > 3000:
        return JsonResponse({'error': 'Expiration time must be between 300 and 3000 seconds'})

    expiration_date = datetime.utcnow() + timedelta(seconds=expiration_time)
    requested_height = generate_expiring_link.requested_height if generate_expiring_link.requested_height else 0

    # Create new expiring link
    new_link = ExpiringLink.objects.create(
        image = generate_expiring_link.original_img , 
        img_height = requested_height,
        original_img = generate_expiring_link.original_requested, 
        expires_on = expiration_date
    )

    expirng_link_url  = reverse('thumbnailer:expiring_link', kwargs={'uuid': new_link.id})
    return JsonResponse({'generated link': request.build_absolute_uri(expirng_link_url)})