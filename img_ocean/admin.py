from django.contrib import admin
from .models import Image, Plan

# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'owner')

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'img_heights', 'orignal_exists', 'expiring_exists')
