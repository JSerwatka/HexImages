from django.db import models
from django.conf import settings
from django.db.models.fields import TextField
from django.utils.translation import gettext_lazy as _


def img_path(instance, filename):
    return f'images/{filename}'

# Create your models here.
class Images(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
    title = models.TextField(_('Title'), max_length=255)
    image = models.ImageField(_('Image'), upload_to=img_path)
    created = models.DateTimeField(_('Upload datetime'), auto_now_add=True)