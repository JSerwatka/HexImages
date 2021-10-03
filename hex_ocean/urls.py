from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('img_ocean.urls')),
    path('thumbnailer', include('thumbnailer.urls'))
]
