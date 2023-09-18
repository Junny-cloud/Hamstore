from django.contrib import admin
from .models import *
from purchases.models import *
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.admin import AdminSite
from purchases.models import *

class DashboardAdmin(admin.ModelAdmin):
    change_list_template = "admin/banners/list_banners.html"

    def ma_page_link(self):
        link = reverse("/")
        return format_html(f'<a href="{link}">test banners</a>')

    ma_page_link.short_description = "Lien vers ma page personnalisée"




class CustomAdminSite(AdminSite):
     change_list_template = "admin/banners/list_banners.html"

     # Personnalisez votre tableau de bord ici
     site_header = 'Mon Tableau de Bord Personnalisé'
     site_title = 'Tableau de Bord'
     index_title = 'Accueil'

custom_admin_site = CustomAdminSite(name='customadmin')    
    
#admin.site.register(Banners, DashboardAdmin)

