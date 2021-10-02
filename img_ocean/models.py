from django.db import models
from django.conf import settings
from django.db.models.fields import TextField
from django.utils.translation import gettext_lazy as _


def img_path(instance, filename):
    return f'images/{filename}'

# Create your models here.
class Image(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
    title = models.TextField(_('title'), max_length=255)
    image = models.ImageField(_('original image'), upload_to=img_path)
    created = models.DateTimeField(_('upload datetime'), auto_now_add=True)

    #TODO prevent filetypes different than PNG/JPG 
    class Meta:
        #TODO handle constrain validation with proper message
        unique_together = ['owner', 'title']



# class Plan(models.Model):
#     title = models.TextField(_('plan title'), max_length=255)
#     img_height = models.IntegerField(_('image height'), min=1)
#     orignal_exists = models.BooleanField(_('allow original image access'), default=False)
#     expiring_exists = models.BooleanField(_('allow to generate expiring links'), default=False)