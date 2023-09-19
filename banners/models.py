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
from products.models import *

User = settings.AUTH_USER_MODEL

def taille_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 1
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("La taille maximale de l'image doit être inférieure ou égale à %sMB" % str(megabyte_limit))

def image_banners(instance, filename): 
    fpath = pathlib.Path(filename)
    new_fname = str(instance.title)
    return f"banners_images/{new_fname}{fpath.suffix}" 


class Banners(models.Model):
     title = models.CharField(max_length=200, null=True, blank=True, verbose_name="titre banner")
     slug = models.SlugField(unique=True, null=True)
     sub_title = models.CharField(max_length=200, null=True, blank=True, verbose_name="sous titre banner")
     description = models.TextField( null=True, blank=True, verbose_name="description evenement")
     images = models.ImageField(upload_to=image_banners, null=True, blank=True, verbose_name="Image")
     event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Evenement")

     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Administrateur")
     date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True, verbose_name='Etat')

     class Meta:
          verbose_name = "Banner"
          verbose_name_plural = "Banners"
          ordering = ['-id']

     def __str__(self):
          return f"{self.title}"
