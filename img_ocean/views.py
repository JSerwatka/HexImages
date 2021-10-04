from datetime import datetime, timedelta

from django.http.response import JsonResponse
from rest_framework import viewsets
from rest_framework import permissions
from django.utils.datastructures import MultiValueDictKeyError
from django.urls import reverse

from thumbnailer.decorators import test_img_parameters

from .serializers import UserSerializer, ImageSerializer
from .models import ExpiringLink, Image, User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ImageViewSet(viewsets.ModelViewSet):
    #TODO update user is not authenticated error msg
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     print(response.data)
    #     return response

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)

    # TODO remove in production
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


@test_img_parameters
def generate_expiring_link(request):
    customer_plan = generate_expiring_link.customer_plan
    img = generate_expiring_link.original_img
    
    if not customer_plan.expiring_exists:
        return JsonResponse({'error': 'This plan does not expiring link generation'})
    
    try:
        expiration_time = int(request.GET['time'])
    except MultiValueDictKeyError:
        return JsonResponse({'error': 'Incorrect URL parameters'})

    if expiration_time < 300 or expiration_time > 3000:
        return JsonResponse({'error': 'Expiration time must be between 300 and 3000 seconds'})

    expiration_date = datetime.now() + timedelta(seconds=expiration_time)
    requested_height = generate_expiring_link.requested_height if generate_expiring_link.requested_height else 0 

    # Create new expiring link
    new_link = ExpiringLink.objects.create(
        image = img, 
        img_height = requested_height,
        original_img = True, 
        expires_on = expiration_date
    )

    return JsonResponse({'generated link': reverse('thumbnailer:expiring', kwargs={'uuid': new_link.id})})
    