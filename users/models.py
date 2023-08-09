from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.forms import model_to_dict
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import FieldDoesNotExist
#from products.models import Products

from config import settings

class CustomUser(AbstractUser):
    telephone = models.CharField(max_length=30, null=True, blank=True, verbose_name="Téléphone")
    date_naissance = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    abonnes_newsletters = models.BooleanField(default=False)
    
    USERNAME_FIELD = "username"  # e.g: "username", "email"
    EMAIL_FIELD = "email"
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-id']

    def __str__(self):
        return f"{self.get_full_name()}"
    
'''class FavoriteProducts(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, verbose_name="client")
    product = models.ForeignKey(Products,  null=True, blank=True, on_delete=models.CASCADE, verbose_name="Produit")
     
    date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    status = models.BooleanField(default=False, verbose_name='Etat')
     
    class Meta:
        verbose_name = "Produit favoris"
        verbose_name_plural = "Produits favoris"
        ordering = ['-id']'''

