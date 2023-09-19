from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
from config.admin import *
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
     list_display = ('images_view','name', 'slug','date_registry', 'status')
     list_filter = ('name',)
     list_display_links = ['name']
     search_fields =  ('name',)
     list_per_page = 25
     fieldsets = [('Info Categorie', {'fields': [ 'name' ]}),
                    ('Visuel', {'fields': ['image', 'status']})
                    ]
     
     def images_view(self, obj):
          return mark_safe('<img src="{url}" style="height:50px; width:100px">'.format(url=obj.image.url)) 

class SubCategoryAdmin(admin.ModelAdmin):
     list_display = ('images_view','name', 'slug','category', 'date_registry','status')
     list_filter =('category',)
     search_fields =  ('name', 'category',)
     list_display_links = ['name']
     list_per_page = 25
     fieldsets = [('Info sous Categorie', {'fields': [ 'name', 'category', 'status']}),  ]

     def images_view(self, obj):
          return mark_safe('<img src="{url}" style="height:50px; width:100px">'.format(url=obj.category.image.url)) 

'''class VariantesAdmin(admin.ModelAdmin):
     list_display = ('reference','name', 'date_registry','status')
     list_filter = ('name', 'date_registry','status')
     search_fields =  ('name', 'reference','status')
     list_display_links = ['name']
     list_per_page = 25
     fieldsets = [('Info Variantes', {'fields': [ 'name', 'status']}),  ]'''
     
class VariantesAdmin(admin.ModelAdmin):
    change_list_template = "admin/products/stock_produits.html"

    def ma_page_link(self):
        link = reverse("/")
        return format_html(f'<a href="{link}">Stock Produits</a>')

    ma_page_link.short_description = "Lien vers Stock Produits"
     
class DescriptionPreciseAdmin(admin.ModelAdmin):
     list_display = ('name', 'valeur','date_registry','status')
     list_filter = ('name', 'date_registry','status')
     search_fields =  ('name', 'date_registry','status')
     list_display_links = ['name']
     list_per_page = 25
     fieldsets = [('Info Variantes', {'fields': [ 'name', 'valeur' ,'status']}),  ]

class EventAdmin(admin.ModelAdmin):
     list_display = ('images_view','title', 'subtitle','slug','date_limite', 'user','status')
     list_filter =('title', 'date_limite',)
     search_fields =  ('title',)
     list_display_links = ['title']
     list_per_page = 25
     fieldsets = [('Info sous Categorie', {'fields': [ 'title', 'subtitle','contenu', 'date_limite']}),
                    ('Visuel', {'fields': ['images', 'status']})
                    ]

     def images_view(self, obj):
          if obj.images:
               return mark_safe('<img src="{url}" style="height:50px; width:100px">'.format(url=obj.images.url)) 
          else:
               return mark_safe('<img src="{url}" style="height:50px; width:100px">'.format(url='/assets/img/logo.png')) 
class ImageInline(admin.TabularInline):
    model = Image
    
class ProductsAdmin(admin.ModelAdmin):
     inlines = [ImageInline]
     
     def display_first_image(self, obj):
          first_image = obj.image_set.first()
          if first_image:
               return mark_safe('<img src="{url}" style="height:50px; width:50px">'.format(url=first_image.image.url))
               
          else:
               return 'No Image'

     display_first_image.short_description = 'First Image'
     display_first_image.allow_tags = True

     list_display = ('display_first_image','name','slug','sub_category','get_variantes',  'price', 'prix_promo','date_registry','status')
     list_filter = ('sub_category', 'event')
     search_fields =  ('name',)
     list_display_links = ['name']
     list_per_page = 25
     fieldsets = [
          ('Info Produit', {'fields': [ 'name', 'sub_category', 'extras']}),
          ('Info Prix', {'fields': ['price', 'prix_promo', 'event']}),
          ('Info Details', {'fields': [ 'variantes','description', 'description_precise' ,'status']})
                    ]

     def get_variantes(self, obj):
        return ", ".join([variante.name for variante in obj.variantes.all()])
   
     def get_description_precise(self, obj):
        return ", ".join([description_precise.name for description_precise in obj.description_precise.all()])
     
     def get_event(self, obj):
        return ", ".join([event.Title for event in obj.event.all()])

     get_variantes.short_description = 'Variantes'
     get_description_precise.short_description = 'description precise'
     
     '''def images_view(self, obj):
          return mark_safe('<img src="{url}" style="height:50px; width:100px">'.format(url=obj.images.url)) '''


class CommentairesAdmin(admin.ModelAdmin):
     list_display = ('client','contenu','note', 'product', 'status','date_registry')
     list_filter = ('client','note', 'product', 'date_registry')
     list_display_links = ['client']
     list_per_page = 25
     search_fields =  ('client', 'product')
     fieldsets = [('Info commentaire', {'fields': [ 'user', 'product','contenu',  'note','status' ]}),
                    ]
     def client(self, obj):
          return obj.user.username
 

def _register(model, admin_class):
     myadmin.register(model, admin_class)


_register(Category, CategoryAdmin) 
_register(SubCategory, SubCategoryAdmin) 
_register(Variantes, VariantesAdmin) 
_register(Event, EventAdmin) 
_register(Products, ProductsAdmin) 
_register(DescriptionPrecise, DescriptionPreciseAdmin) 
_register(Commentaires, CommentairesAdmin) 

