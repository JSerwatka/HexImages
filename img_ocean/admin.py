from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Image, Plan, User, Customer


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'owner')


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'img_heights', 'original_exists', 'expiring_exists')


class CustomerInline(admin.StackedInline):
    model = Customer
    # can_delete = False
    # verbose_name_plural = 'employee'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (CustomerInline,)