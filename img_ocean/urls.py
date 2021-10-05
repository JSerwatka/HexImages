from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from .views import ImageViewSet, GenerateExpiringLink
# from .views import ImageViewSet, generate_expiring_link


app_name = 'img_ocean'

router = routers.DefaultRouter()
router.register(r'images', ImageViewSet, basename='Image')

urlpatterns = [
    path('', include(router.urls)),
    path('generate-expiring-link', GenerateExpiringLink.as_view(), name='generate_expiring_link')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)