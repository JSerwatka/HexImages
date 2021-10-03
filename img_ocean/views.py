from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions

from .serializers import UserSerializer, GroupSerializer, ImageSerializer
from .models import Image, User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ImageViewSet(viewsets.ModelViewSet):
    #TODO update user is not authenticated error msg
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     print(response.data)
    #     return response

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)

    # TODO remove in production
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
    