from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Image


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ImageSerializer(serializers.ModelSerializer):  
    #TODO use hidden field in production 
    # owner = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )
    
    owner = serializers.StringRelatedField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Image
        fields = ['owner', 'id', 'title', 'image']