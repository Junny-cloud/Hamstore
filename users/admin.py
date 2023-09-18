from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as BaseUser
from .models import CustomUser
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from config.admin import *

class UserAdmin(BaseUser):
    ordering = ['id']
    list_display = ['id', 'username', 'first_name', 'last_name', 'telephone', 'is_active', 'is_staff', 'is_superuser', 'date_joined']
    list_filter = []
    list_display_links = ['username']
    list_per_page = 25
    search_fields =  ['username', 'first_name', 'last_name', 'telephone']
    fieldsets = [
          ('Info perso', {'fields': [ 'first_name', 'last_name', 'telephone', 'date_naissance', 'abonnes_newsletters']}),
          ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
          
                    ]

myadmin.register(CustomUser, UserAdmin)
