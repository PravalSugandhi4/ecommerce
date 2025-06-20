from django.contrib import admin
from .models import *

admin.site.register(Categories)
admin.site.register(Products)

admin.site.register(wishlist)
from django.contrib import admin

from django.contrib import admin
from .models import users

@admin.register(users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('userid', 'get_full_name', 'get_email', 'phone')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Name'

    def get_email(self, obj):
        return obj.email
    get_email.short_description = 'Email'

search_fields = ['user__email', 'user__first_name', 'user__last_name', 'phone']
list_filter = ['user__is_active']