import io
from django.http.response import HttpResponse
from django.shortcuts import render
from urllib.request import urlopen
from PIL import Image

from img_ocean.models import Image

# D:\Obrazy\laptop-people-centered-banner.png'
def index(request):
    baseheight = 200
    output = io.BytesIO()

    # Open the requested img
    img = Image.open('D:\Obrazy\laptop-people-centered-banner.png')
    # Check format - JPG or PNG
    format = img.format 

    # Calculate width based on fixed height
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    # Resize image and save in a file object
    img = img.resize((wsize, baseheight), Image.LANCZOS)
    img.save(output, format)
    output.seek(0)

    return HttpResponse(output, content_type="image/jpeg")