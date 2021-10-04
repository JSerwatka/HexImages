from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    Image, 
    Plan, 
    User, 
    Customer,
    ExpiringLink
)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'owner')


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'img_heights', 'original_exists', 'expiring_exists')


class CustomerInline(admin.StackedInline):
    model = Customer


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline,)
    list_display = ('username', 'email', 'customer', 'is_staff')


@admin.register(ExpiringLink)
class ExpiringLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'img_height', 'original_img', 'expires_on')