from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('img_ocean.urls', namespace='img_ocean')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('thumbnailer', include('thumbnailer.urls', namespace='thumbnailer'))
]
