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

User = settings.AUTH_USER_MODEL

# CUSTOM IMAGE CATEGORIES AND PRODUITS

def taille_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 1
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("La taille maximale de l'image doit être inférieure ou égale à %sMB" % str(megabyte_limit))

def image_categories(instance, filename): 
    fpath = pathlib.Path(filename)
    new_fname = str(instance.nom)
    return f"categories_images/{new_fname}{fpath.suffix}" 

def image_produits(instance, filename): 
    fpath = pathlib.Path(filename)
    new_fname = str(instance.nom)
    return f"produits_images/{new_fname}{fpath.suffix}"

def image_evenements(instance, filename): 
    fpath = pathlib.Path(filename)
    new_fname = str(instance.titre)
    return f"evenements_images/{new_fname}{fpath.suffix}" 



class Categories(models.Model):
     nom = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nom categorie")
     image = models.ImageField(upload_to=image_categories, validators=[taille_image], null=True, blank=True, verbose_name="Image")

     date_enregistrement = models.DateTimeField(default=timezone.now, verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True)
     
     class Meta:
          verbose_name = "Categorie"
          verbose_name_plural = "Categories"
          ordering = ['-id']

     def __str__(self):
          return f"{self.nom}"
     
class SousCategories(models.Model):
     nom = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nom sous-categorie")
     categorie = models.ForeignKey(Categories, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Nom categorie")

     date_enregistrement = models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True)
     
     class Meta:
          verbose_name = "Sous Categorie"
          verbose_name_plural = "Sous Categories"
          ordering = ['-id']

     def __str__(self):
          return f"{self.nom}"

     pass

class Evenements(models.Model):
     titre = models.CharField(max_length=200, null=True, blank=True, verbose_name="titre evenement")
     date_limite = models.DateField( null=True, blank=True, verbose_name="date fin evenement")
     contenu = models.TextField( null=True, blank=True, verbose_name="description evenement")
     images = models.ImageField(upload_to=image_evenements, null=True, blank=True, verbose_name="Image")

     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Administrateur")
     date_enregistrement = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True, verbose_name='Etat')

     class Meta:
          verbose_name = "Evenement"
          verbose_name_plural = "Evenements"
          ordering = ['-id']

     def __str__(self):
          return f"{self.titre}"

class Produits(models.Model):
     nom = models.CharField(max_length=200, null=True, blank=True, verbose_name="Nom produit")
     categorie = models.ForeignKey(Categories, null=True, blank=False, on_delete=models.CASCADE, verbose_name="Nom categorie")
     sous_categorie = models.ForeignKey(SousCategories, null=True, blank=False, on_delete=models.CASCADE, verbose_name="Nom sous categorie")
     extras = models.CharField(max_length=200, null=True, blank=True, verbose_name="Extras")
     evenement = models.ForeignKey(Evenements, null=True, blank=False, on_delete=models.CASCADE, verbose_name="Evenement")
     prix = models.IntegerField( null=True, blank=True, verbose_name="Prix")
     prix_promo = models.IntegerField( null=True, blank=True, verbose_name="Prix evenement")
     images = models.ImageField(upload_to=image_produits, null=True, blank=True, verbose_name="Image")
     description = models.TextField( null=True, blank=True, verbose_name="description produit")
     description_precise = models.TextField( null=True, blank=True, verbose_name="description precise")

     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Administrateur")
     date_enregistrement = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True, verbose_name='Etat')
     
     class Meta:
          verbose_name = "Produit"
          verbose_name_plural = "Produits"
          ordering = ['-id']

     def __str__(self):
          return f"{self.nom}"
     
     def get_image(self):
          if self.images:
               return f'{settings.MEDIA_URL}{self.images}'
          return f'{settings.STATIC_URL}images/equ_image.png'
     pass

class Commentaires(models.Model):
     contenu = models.TextField( null=True, blank=True, verbose_name="description evenement")
     note = models.IntegerField( null=True, blank=True, verbose_name="Note produit")
     produit = models.ForeignKey(Produits , null=True, blank=False, on_delete=models.CASCADE, verbose_name="produit concerne")

     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Administrateur")
     date_enregistrement = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True, verbose_name='Etat')

     class Meta:
          verbose_name = "Commentaire"
          verbose_name_plural = "Commentaires"
          ordering = ['-id']

     def __str__(self):
          return f"{self.contenu}"
     pass


