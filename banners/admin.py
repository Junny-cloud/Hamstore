from django.contrib import admin
from .models import *
from purchases.models import *
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.admin import AdminSite
from purchases.models import *
from django.utils.safestring import mark_safe
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



class BannersAdmin(admin.ModelAdmin):
     list_display = ('images_view','title', 'event','status')
     list_filter =('title','event','status')
     search_fields =  ('title',)
     list_display_links = ['title']
     list_per_page = 10
     fieldsets = [('Info Banners', {'fields': [ 'title', 'images','event', 'status']}),
                   
                    ]

     def images_view(self, obj):
          if obj.images:
               return mark_safe('<img src="{url}" style="height:50px; width:100px">'.format(url=obj.images.url)) 
          else:
               return mark_safe('<img src="{url}" style="height:50px; width:100px">'.format(url='/assets/img/logo.png')) 

custom_admin_site = CustomAdminSite(name='customadmin')    
    
admin.site.register(Banners, BannersAdmin)