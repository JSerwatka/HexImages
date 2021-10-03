import io
from django.http.response import HttpResponse
from django.shortcuts import render
from urllib.request import urlopen
import PIL.Image

from img_ocean.models import Image

# D:\Obrazy\laptop-people-centered-banner.png'
def resize(request):
    print(request.GET)
    customer_plan = request.user.customer.plan
    available_heights = [int(str_height) for str_height in customer_plan.img_heights.split(',')]
    print(available_heights)
    baseheight = 200
    output = io.BytesIO()

    # Open the requested img
    img = PIL.Image.open('D:\Obrazy\laptop-people-centered-banner.png')
    # Check format - JPG or PNG
    format = img.format 

    # Calculate width based on fixed height
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    # Resize image and save in a file object
    img = img.resize((wsize, baseheight), PIL.Image.LANCZOS)
    img.save(output, format)
    output.seek(0)

    return HttpResponse(output, content_type=f"image/{format.lower()}")