from django.db import models
import pathlib
import uuid
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
from django.contrib.auth import get_user_model


User = get_user_model()

    
class Commandes(models.Model):
     reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="reference commande")
     products = models.ManyToManyField(Products, through='ProduitsCommandes')
     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="client")
     total_amount = models.PositiveIntegerField(default=0, verbose_name="prix commande")
     date_commande = models.DateField(auto_now_add=True)
     
     date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=False, verbose_name='Etat')
     
     class Meta:
          verbose_name = "Commande"
          verbose_name_plural = "Commandes"
          ordering = ['-id']
        
     def __str__(self):
          return f"Commande #{self.reference} - {self.user.last_name}"
   
 

class ProduitsCommandes(models.Model):
     commande = models.ForeignKey(Commandes, null=True, blank=True, on_delete=models.CASCADE, verbose_name="commande concerné")
     product = models.ForeignKey(Products,  null=True, blank=True, on_delete=models.CASCADE, verbose_name="Produit")
     variante = models.CharField(max_length=200, null=True, blank=True, verbose_name="variante choisie")
     price_unitaire = models.PositiveIntegerField(default=0, verbose_name="prix produit")
     quantity = models.PositiveIntegerField(default=1)
     subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name="Total du produit")
     
     date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=False, verbose_name='Etat')
     
     class Meta:
          verbose_name = "Produit Commandé"
          verbose_name_plural = "Produits Commandés"
          ordering = ['-id']

     '''def save(self, *args, **kwargs):
          
          if self.product.event:
               self.subtotal = self.product.prix_promo * self.quantity
          else:
               self.subtotal = self.product.price * self.quantity
          super(ProduitsCommandes, self).save(*args, **kwargs)'''

     def __str__(self):
          return f"{self.quantity} x {self.product.name} (commande #{self.commande.reference})"


class FavoriteProducts(models.Model):
    #info = models.CharField(max_length=200, null=True, blank=True, verbose_name="info")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="client")
    product = models.ForeignKey(Products,  null=True, blank=True, on_delete=models.CASCADE, verbose_name="Produit")
     
    date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    status = models.BooleanField(default=False, verbose_name='Etat')
     
    class Meta:
        verbose_name = "Produit favoris"
        verbose_name_plural = "Produits favoris"
        ordering = ['-id']