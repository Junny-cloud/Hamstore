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
from users.models import *

# Email
from django.core.mail import  EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
import string


User = get_user_model()

    
class Commandes(models.Model):
     reference = models.CharField(max_length=12, unique=True, verbose_name="reference commande")
     products = models.ManyToManyField(Products, through='ProduitsCommandes')
     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="client")
     total_amount = models.PositiveIntegerField(default=0, verbose_name="prix commande")
     date_commande = models.DateField(auto_now_add=True)
     etat_commande = models.CharField(max_length=200, default="En cours",null=True, blank=True, verbose_name="etat de la commande")
     date_registry = models.DateTimeField(default=timezone.now,verbose_name="Date d'enregistrement")
     date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
     status = models.BooleanField(default=False, verbose_name='Etat')
     
     class Meta:
          verbose_name = "Commande"
          verbose_name_plural = "Commandes"
          ordering = ['-id']
          
     def save(self, *args, **kwargs):
          if not self.reference:
               # Générer un code unique aléatoire de 8 caractères
               unique_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
               # Assurez-vous que le code généré est vraiment unique
               while Commandes.objects.filter(reference=unique_code).exists():
                    unique_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
               self.reference = unique_code
          super().save(*args, **kwargs)
        
     def __str__(self):
          return f"Commande #{self.reference} - {self.user.last_name}"
   
 

class ProduitsCommandes(models.Model):
     commande = models.ForeignKey(Commandes, null=True, blank=True, on_delete=models.CASCADE, verbose_name="commande concerné")
     product = models.ForeignKey(Products,  null=True, blank=True, on_delete=models.CASCADE, verbose_name="Produit")
     variante = models.ForeignKey(Variantes,  null=True, blank=True, on_delete=models.CASCADE, verbose_name="variante choisie")
     price_unitaire = models.PositiveIntegerField(default=0, verbose_name="prix produit")
     quantity = models.PositiveIntegerField(default=1)
     subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name="Total du produit")
     
     date_registry = models.DateTimeField(auto_now_add=True,verbose_name="Date d'enregistrement")
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
    
  
#@receiver(post_save, sender=Commandes)

'''def envoie_de_mail_commande(sender, created, instance, **kwargs):
     if instance.pk and instance._state.fields_changed:
          
           # SEND MAIL CONFIG
          html_content = render_to_string('purchases/email_commande.html', {
          'title': 'Commande de produits',
          'nom_entreprise': 'Athehams',
          'obj': instance,
          'link': 'http://127.0.0.1:8000/admin/',
          #'link': 'http://athehams.com',
          })
          text_content = strip_tags(html_content)
          
          subject = "NOUVELLE COMMANDE"
          recipient_list =[obj['email'] for obj in CustomUser.objects.values('email').filter(is_superuser=True)]
          from_email ='contact@athehams.com'
          send_mail(
               subject,
               'Commandes Boutique',
               from_email,
               recipient_list,
               fail_silently=False,
               html_message=text_content,
          )
          
          # ----------------- NEW EMAIL SENDER -----------------------------
          link = "https://athehams.com"
          subject = "NOUVELLE COMMANDE"
          recipient_list =[obj['email'] for obj in CustomUser.objects.values('email').filter(is_superuser=True)]
          produits_commandes =[]
          montant_livraison="2.000"
          data1 = [ obj for obj in ProduitsCommandes.objects.filter(commande=instance).values('quantity', 'subtotal', 'price_unitaire', 'variante__name', 'variante__reference', 'product__name', 'product','commande__id')]
          for obj in data1:
               print(obj)
               img = Image.objects.filter(product=obj['product']).first()
               
               obj['image']= img.image.url
               produits_commandes.append(obj)
               
          from_email ='contact@athehams.com'
          context = {
            "link": link,
            "produits_commandes":produits_commandes,
            "instance":instance,
            "montant_livraison":montant_livraison,
          }
            
          #print(my_recipient)
          html_message = render_to_string("purchases/email.html", context=context)
          plain_message = strip_tags(html_message)

          message = EmailMultiAlternatives(
               subject = subject, 
               body = plain_message,
               from_email = from_email ,
               to= ['junioressoh98@gmail.com',]
          )

          message.attach_alternative(html_message, "text/html")
          message.send()
          print('ok message envoyé')'''

       
          
 