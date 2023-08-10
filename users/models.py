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