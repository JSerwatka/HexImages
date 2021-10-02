from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .validators import positive_int_list_validator


def img_path(instance, filename):
    return f'images/{filename}'

#TODO add plan to User
class User(AbstractUser):
    pass


class Image(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
    title = models.TextField(_('title'), max_length=255)
    image = models.ImageField(_('original image'), upload_to=img_path)
    created = models.DateTimeField(_('upload datetime'), auto_now_add=True)

    #TODO prevent filetypes different than PNG/JPG 
    class Meta:
        #TODO handle constrain validation with proper message
        unique_together = ['owner', 'title']


class Plan(models.Model):
    title = models.TextField(_('plan title'), max_length=255)
    img_heights = models.CharField(
        _('image heights'), 
        validators=[positive_int_list_validator(message=_('List must consist of comma separated positive integers'))], 
        max_length=255
    )
    original_exists = models.BooleanField(_('allow original image access'), default=False)
    expiring_exists = models.BooleanField(_('allow to generate expiring links'), default=False)


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)


