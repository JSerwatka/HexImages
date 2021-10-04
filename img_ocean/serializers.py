from django.urls import reverse
from rest_framework import serializers

from .models import Image, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class ImageSerializer(serializers.ModelSerializer):  
    #TODO use hidden field in production 
    # owner = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )
    
    owner = serializers.StringRelatedField(default=serializers.CurrentUserDefault())

    images = serializers.SerializerMethodField('get_images_urls')

    class Meta:
        model = Image
        #TODO hide image in response, but leave POST panel
        fields = ['owner', 'id', 'title', 'image', 'images']

    def get_images_urls(self, image):
        #TODO remove try/except - debug for admin
        try: 
            #TODO cleanup
            request = self.context.get('request')
            image_id = image.id
            customer_plan = image.owner.customer.plan
            available_heights = customer_plan.img_heights.split(',')

            resizer_url = reverse('thumbnailer:resize')
            response_obj = {}

            for height in available_heights:
                query = f'?id={image_id}&height={height}'
                response_obj[f'image-{height}px'] = request.build_absolute_uri(resizer_url + query)

            if customer_plan.original_exists:
                query = f'?id={image_id}'
                response_obj[f'image-original'] = request.build_absolute_uri(resizer_url + query)

            if customer_plan.expiring_exists:
                expiring_link_url = reverse('img_ocean:generate_expiring_link')
                query = f'?id={image_id}&height={height}&time=300'
                response_obj[f'image-expiring'] = request.build_absolute_uri(expiring_link_url + query)
        except:
            response_obj = {}


        return response_obj
