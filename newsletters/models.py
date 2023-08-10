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

class Newsletters(models.Model):
     email = models.EmailField(max_length=200, null=True, blank=True, verbose_name="email abonnees")
     
     date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True, verbose_name='Etat')
     
     class Meta:
          verbose_name = "Email"
          verbose_name_plural = "Emails"
          ordering = ['-id']

     def __str__(self):
          return f"{self.email}"
     

class Mailing(models.Model):
     objet_mail = models.CharField(max_length=200, null=True, blank=True, verbose_name="Objet du mail")
     contenu = models.TextField( null=True, blank=True, verbose_name="contenu mail")
     
     date_registry = models.DateTimeField( auto_now_add=True,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=True, verbose_name='Etat')
     
     class Meta:
          verbose_name = "Message"
          verbose_name_plural = "Messages"
          ordering = ['-id']

     def __str__(self):
          return f"{self.objet_mail}"
     pass


