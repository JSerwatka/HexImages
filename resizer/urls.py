from django.http.response import HttpResponse
from django.urls import path

from .views import resize


app_name = 'resizer'

urlpatterns = [
    path('', resize, name='resize')
]
