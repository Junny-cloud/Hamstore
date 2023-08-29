from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as BaseUser
from .models import CustomUser
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

class UserAdmin(BaseUser):
    ordering = ['id']
    list_display = ['id', 'username', 'first_name', 'last_name', 'telephone', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    list_filter = ['username', 'first_name']
    list_per_page = 25
    search_fields =  ['username', 'first_name', 'last_name', 'telephone']

admin.site.register(CustomUser, UserAdmin)
