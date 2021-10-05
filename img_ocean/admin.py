from datetime import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _

from .models import (
    Image, 
    Plan, 
    User, 
    Customer,
    ExpiringLink
)


class LinkAvailableFilter(SimpleListFilter):
    '''#TODO docstring'''
    title = _('link available')
    parameter_name = 'available'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Yes')),
            ('no', _('No'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(expires_on__gt=datetime.utcnow())
        elif self.value() == 'no':
            return queryset.filter(expires_on__lt=datetime.utcnow())
        else:
            return queryset


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
    list_display = ('id', 'image', 'img_height', 'original_img', 'expires_on', 'available')
    list_filter = ('img_height', LinkAvailableFilter)

    def available(self, obj):
        '''#TODO docstring'''
        return obj.expires_on > datetime.utcnow()
    
    available.boolean = True