from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from .views import UserViewSet, GroupViewSet, ImageViewSet



router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'images', ImageViewSet, basename='Image')

app_name = 'img_ocean'

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)