from django.db import models
import pathlib
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.db import transaction
from django.utils.text import slugify 
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import *
from django.core.exceptions import FieldDoesNotExist
from django.dispatch import receiver
import os
import requests

User = settings.AUTH_USER_MODEL

# CUSTOM IMAGE CATEGORIES AND PRODUITS

def taille_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 1
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("La taille maximale de l'image doit être inférieure ou égale à %sMB" % str(megabyte_limit))

def image_categories(instance, filename): 
    fpath = pathlib.Path(filename)
    new_fname = str(instance.name)
    return f"categories_images/{new_fname}{fpath.suffix}" 

def image_produits(instance, filename): 
    fpath = pathlib.Path(filename)
    #new_fname = str(instance.name)
    #return f"produits_images/{new_fname}{fpath.suffix}"
    return f"produits_images/{fpath.suffix}"

def image_evenements(instance, filename): 
    fpath = pathlib.Path(filename)
    new_fname = str(instance.title)
    return f"evenements_images/{new_fname}{fpath.suffix}" 



class Category(models.Model):
     name = models.CharField(max_length=200, null=True, unique=True,blank=True, verbose_name="Nom categorie")
     slug = models.SlugField(unique=True, null=True)
     image = models.ImageField(upload_to=image_categories, validators=[taille_image], null=True, blank=True, verbose_name="Image")
     
     date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True, verbose_name='Etat')
     
     class Meta:
          verbose_name = "Categorie"
          verbose_name_plural = "Categories"
          ordering = ['-id']

     def __str__(self):
          return f"{self.name}"
     
     def save(self, *args, **kwargs):
        # Générer le slug à partir du nom de la catégorie avant de sauvegarder
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
     
class SubCategory(models.Model):
     name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nom sous-categorie")
     slug = models.SlugField(unique=True, null=True)
     category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Nom categorie")

     date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True, verbose_name='Etat')
     
     class Meta:
          verbose_name = "Sous Categorie"
          verbose_name_plural = "Sous Categories"
          ordering = ['-id']

     def __str__(self):
          return f"{self.name}"
     
     def save(self, *args, **kwargs):
        # Générer le slug à partir du nom de la catégorie avant de sauvegarder
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

     
class Variantes(models.Model):
     name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nom sous-categorie")

     date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True, verbose_name='Etat')
     
     class Meta:
          verbose_name = "Variante"
          verbose_name_plural = "Variantes"
          ordering = ['-id']

     def __str__(self):
          return f"{self.name}"
     

class Event(models.Model):
     
     title = models.CharField(max_length=200, null=True, blank=True, verbose_name="titre evenement")
     subtitle = models.CharField(max_length=200, null=True, blank=True, verbose_name="sous titre evenement")
     slug = models.SlugField(unique=True, null=True)
     date_limite = models.DateField( null=True, blank=True, verbose_name="date fin evenement")
     contenu = models.TextField( null=True, blank=True, verbose_name="description evenement")
     images = models.ImageField(upload_to=image_evenements, null=True, blank=True, verbose_name="images")

     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Administrateur")
     date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True, verbose_name='Etat')

     class Meta:
          verbose_name = "Evenement"
          verbose_name_plural = "Evenements"
          ordering = ['-id']

     def __str__(self):
          return f"{self.title}"
     
     def save(self, *args, **kwargs):
        # Générer le slug à partir du nom de la catégorie avant de sauvegarder
        self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

class Products(models.Model):
     name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nom produit")
     slug = models.SlugField(unique=True, null=True)
     sub_category = models.ForeignKey(SubCategory, null=True, blank=False, on_delete=models.CASCADE, verbose_name="Nom sous categorie")
     extras = models.CharField(max_length=200, null=True, blank=True, verbose_name="Extras")
     event = models.ForeignKey(Event,default='', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Evenement")
     price = models.IntegerField( null=True, blank=True, verbose_name="Prix")
     prix_promo = models.IntegerField( null=True, blank=True, verbose_name="Prix evenement")
     images = models.ManyToManyField('Image')
     description = models.TextField( null=True, blank=True, verbose_name="description produit")
     description_precise = models.TextField( null=True, blank=True, verbose_name="description precise")
     variantes = models.ManyToManyField(Variantes, blank=True, verbose_name="les variantes")

     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Administrateur")
     date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True, verbose_name='Etat')
     
     class Meta:
          verbose_name = "Produit"
          verbose_name_plural = "Produits"
          ordering = ['-id']

     def __str__(self):
          return f"{self.name}"
     
     def save(self, *args, **kwargs):
        # Générer le slug à partir du nom de la catégorie avant de sauvegarder
        self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)
     
def product_image_path(instance, filename):
    # Construction du chemin de destination des images
    # Utilisez le nom du produit pour renommer le fichier
    base_filename, extension = os.path.splitext(filename)
    product_name = instance.product.name
    new_filename = f"{product_name}{extension}"
    return os.path.join('produits_images/', new_filename) 

class Image(models.Model):

     product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Image produit")
     image = models.ImageField(upload_to=product_image_path, validators=[taille_image], null=True, blank=True, verbose_name="Image")

     def __str__(self):
          return self.image.name
   
@receiver(models.signals.pre_save, sender=Image)
def auto_rename_image(sender, instance, **kwargs):
    if instance.pk:
        # L'image existe déjà, récupère le nom du fichier actuel
        current_image = Image.objects.get(pk=instance.pk)
        if current_image.image != instance.image:
            # L'image a été modifiée, supprime l'ancien fichier
            current_image.image.delete(False)

@receiver(models.signals.post_delete, sender=Image)
def auto_delete_image(sender, instance, **kwargs):
    # Supprime le fichier d'image lorsque l'objet Image est supprimé
    instance.image.delete(False)


class Commentaires(models.Model):
     contenu = models.TextField( null=True, blank=True, verbose_name="description evenement")
     note = models.IntegerField( null=True, blank=True, verbose_name="Note produit")
     product = models.ForeignKey(Products , null=True, blank=False, on_delete=models.CASCADE, verbose_name="produit concerne")

     user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, verbose_name="client")
     date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True, verbose_name='Etat')

     class Meta:
          verbose_name = "Commentaire"
          verbose_name_plural = "Commentaires"
          ordering = ['-id']

     def __str__(self):
          return f"{self.contenu}"
     
     



