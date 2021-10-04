from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from .views import UserViewSet, ImageViewSet, generate_expiring_link


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'images', ImageViewSet, basename='Image')

#TODO when uncommented rest_framework auth doesnt work
app_name = 'img_ocean'

#TODO rest_framework redire

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('generate-expiring-link', generate_expiring_link, name='generate_expiring_link'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)