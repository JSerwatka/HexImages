from django.http.response import JsonResponse
from django.urls import reverse
from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):  
    #TODO use hidden field in production 
    # owner = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )
    image = serializers.ImageField(write_only=True)
    owner = serializers.StringRelatedField(default=serializers.CurrentUserDefault())
    images = serializers.SerializerMethodField('get_images_urls')

    class Meta:
        model = Image
        fields = ['owner', 'id', 'title', 'image', 'images']

    def validate_image(self, value):
        if value.content_type not in ['image/jpg', 'image/png']:
            raise serializers.ValidationError('Invalid extension, only JPG and PNG are supported') 
        return value

    def get_images_urls(self, image):
        request = self.context.get('request')
        customer_plan = image.owner.customer.plan
        available_heights = customer_plan.img_heights.split(',')
        
        resizer_url = reverse('thumbnailer:resize')
        response_obj = {}
        
        # Generate image links based on the customer's plan
        for height in available_heights:
            query = f'?id={image.id}&height={height}'
            response_obj[f'image-{height}px'] = request.build_absolute_uri(resizer_url + query)

        if customer_plan.original_exists:
            query = f'?id={image.id}'
            response_obj[f'image-original'] = request.build_absolute_uri(resizer_url + query)

        if customer_plan.expiring_exists:
            expiring_link_url = reverse('img_ocean:generate_expiring_link')
            query = f'?id={image.id}&height={height}&time=300'
            response_obj[f'image-expiring'] = request.build_absolute_uri(expiring_link_url + query)


        return response_obj
