from django.http.response import HttpResponse
from django.urls import path

from .views import resize


app_name = 'thumbnailer'

urlpatterns = [
    path('', resize, name='resize')
]
