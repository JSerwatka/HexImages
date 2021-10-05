from django.urls import path

from .views import ResizeImg, GetExpiringLink


app_name = 'thumbnailer'

urlpatterns = [
    path('', ResizeImg.as_view(), name='resize_img'),
    path('/expiring-link/<str:uuid>', GetExpiringLink.as_view(), name='get_expiring_link')
]
