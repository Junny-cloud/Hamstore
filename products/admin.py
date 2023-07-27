from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
     list_display = ('images_view','name', 'date_registry', 'status')
     list_filter = ('image','name', 'date_registry', 'status')
     list_display_links = ['name']
     search_fields =  ('name',)
     fieldsets = [('Info Categorie', {'fields': [ 'name' ]}),
                    ('Visuel', {'fields': ['image', 'status']})
                    ]
     
     def images_view(self, obj):
          return mark_safe('<img src="{url}" style="height:50px; width:100px">'.format(url=obj.image.url)) 

class SubCategoryAdmin(admin.ModelAdmin):
     list_display = ('images_view','name', 'category', 'date_registry','status')
     list_filter =('name', 'category', 'date_registry','status')
     search_fields =  ('name', 'category', 'date_registry','status')
     list_display_links = ['name']
     fieldsets = [('Info sous Categorie', {'fields': [ 'name', 'category', 'status']}),  ]

     def images_view(self, obj):
          return mark_safe('<img src="{url}" style="height:50px; width:100px">'.format(url=obj.category.image.url)) 

class VariantesAdmin(admin.ModelAdmin):
     list_display = ('name', 'date_registry','status')
     list_filter = ('name', 'date_registry','status')
     search_fields =  ('name', 'date_registry','status')
     list_display_links = ['name']
     fieldsets = [('Info Variantes', {'fields': [ 'name', 'status']}),  ]

class EventAdmin(admin.ModelAdmin):
     list_display = ('images_view','title', 'date_limite', 'user','status')
     list_filter =('title', 'date_limite', 'user','status')
     search_fields =  ('title', 'date_limite', 'user')
     list_display_links = ['title']
     fieldsets = [('Info sous Categorie', {'fields': [ 'title', 'contenu', 'date_limite']}),
                    ('Visuel', {'fields': ['images', 'status']})
                    ]

     def images_view(self, obj):
          return mark_safe('<img src="{url}" style="height:50px; width:100px">'.format(url=obj.images.url)) 

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

     list_display = ('display_first_image','name','sub_category', 'extras','price', 'prix_promo','date_registry','status')
     list_filter = ('sub_category', 'name','price', 'prix_promo','event')
     search_fields =  ('sub_category','name', 'price', 'prix_promo','event')
     list_display_links = ['name']
     fieldsets = [
          ('Info Produit', {'fields': [ 'name', 'sub_category', 'extras']}),
          ('Info Prix', {'fields': ['price', 'prix_promo', 'event']}),
          ('Info Details', {'fields': [ 'variantes','description', 'description_precise', 'status']})
                    ]

     '''def images_view(self, obj):
          return mark_safe('<img src="{url}" style="height:50px; width:100px">'.format(url=obj.images.url)) '''


class CommentairesAdmin(admin.ModelAdmin):
     list_display = ('user','contenu','note', 'product', 'status','date_registry')
     list_filter = ('user','note', 'product', 'date_registry')
     list_display_links = ['user']
     search_fields =  ('user', 'product')
     fieldsets = [('Info commentaire', {'fields': [ 'user', 'product','contenu', 'note','status' ]}),
                    ]
 

def _register(model, admin_class):
     admin.site.register(model, admin_class)


_register(Category, CategoryAdmin) 
_register(SubCategory, SubCategoryAdmin) 
_register(Variantes, VariantesAdmin) 
_register(Event, EventAdmin) 
_register(Products, ProductsAdmin) 


