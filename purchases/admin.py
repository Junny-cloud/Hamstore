from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
from django.urls import reverse
from django.utils.html import format_html

class ProduitsCommandesInline(admin.TabularInline):
    model = ProduitsCommandes
'''class CommandesAdmin(admin.ModelAdmin):
    
    inlines = (ProduitsCommandesInline,)
    list_display = ('reference','user', 'display_products','total_amount','date_registry', 'status')
    list_filter = ('reference','user','date_registry', 'status')
    list_display_links = ['reference']
    list_per_page = 25
    search_fields =  ('reference', 'user')
    fieldsets = (('Info Commande', {'fields': [ 'user', 'total_amount','status']}),
                 )
    
    def display_products(self, obj):
        products = obj.products.all()
        return ', '.join([product.name for product in products])'''

class CommandesAdmin(admin.ModelAdmin):
    change_list_template = "admin/purchases/list_commandes.html"

    def ma_page_link(self):
        link = reverse("/")
        return format_html(f'<a href="{link}">Commandes</a>')

    ma_page_link.short_description = "Lien vers ma page personnalisée"
     
        
class ProduitsCommandesAdmin(admin.ModelAdmin):
    list_display = ('slug','commande', 'product','price_unitaire', 'quantity', 'subtotal','date_registry', 'status')
    list_filter = ('commande', 'product','date_registry', 'status')
    list_display_links = ['slug']
    list_per_page = 25
    search_fields =  ('commande', 'product','date_registry', 'status')

    fieldsets = [('Produits Commandes', {'fields': [ 'product', 'quantity']}),]

def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(Commandes, CommandesAdmin) 
admin.site.register(ProduitsCommandes)