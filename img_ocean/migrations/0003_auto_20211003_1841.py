# Generated by Django 3.1.7 on 2021-10-03 16:41

import django.core.validators
from django.db import migrations, models
import img_ocean.models


class Migration(migrations.Migration):

    dependencies = [
        ('img_ocean', '0002_auto_20211003_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=img_ocean.models.img_path, validators=[django.core.validators.FileExtensionValidator(['jpg', 'png'], message='Invalid extension, only JPG and PNG are supported')], verbose_name='original image'),
        ),
    ]