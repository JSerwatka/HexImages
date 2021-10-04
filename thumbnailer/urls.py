from django.http.response import HttpResponse
from django.urls import path

from .views import resize


app_name = 'thumbnailer'

urlpatterns = [
    path('', resize, name='resize'),
    # path('generate-expiring', generate_expiring, name='generate_expiring')
    # path('/expiring/<str:hash>', expiring_link, name='expiring_link')
]
