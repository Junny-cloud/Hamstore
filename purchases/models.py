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

class Commandes(models.Model):
     reference = models.CharField(max_length=200, null=True, blank=True, verbose_name="reference commande")
     client = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, verbose_name="client")
     
     date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=False, verbose_name='Etat')
     
     class Meta:
          verbose_name = "Commande"
          verbose_name_plural = "Commandes"
          ordering = ['-id']

     def __str__(self):
          return f"{self.reference}"
    

class ProduitsCommandes(models.Model):
     commande = models.ForeignKey(Commandes, null=True, blank=True, on_delete=models.CASCADE, verbose_name="commande concerné")
     product = models.ForeignKey(Products, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Produit")
     price_product = models.CharField(max_length=200, null=True, blank=True, verbose_name="prix produit")

     date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=False, verbose_name='Etat')
     
     class Meta:
          verbose_name = "Produit Commandé"
          verbose_name_plural = "Produits Commandés"
          ordering = ['-id']

     def __str__(self):
          return f"{self.product}"
     pass


