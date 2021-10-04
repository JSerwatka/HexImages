from django.http.response import HttpResponse
from django.urls import path

from .views import resize, expiring_link


app_name = 'thumbnailer'

urlpatterns = [
    path('', resize, name='resize'),
    path('/expiring-link/<str:uuid>', expiring_link, name='expiring_link')
]
