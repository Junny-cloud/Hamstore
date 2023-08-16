
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

def send_order_email(instance):
    subject = 'Nouvelle commande enregistrée'
    message = f'Une nouvelle commande a été enregistrée :\n\nProduit : {instance.produit.nom}\nQuantité : {instance.quantite}\nDate : {instance.date_commande}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [admin[1] for admin in settings.ADMINS]

    send_mail(subject, message, from_email, recipient_list)
    
def send_order_confirmation_email(instance):
    subject = 'Confirmation de votre commande'
    message = f'Votre commande a été enregistrée avec succès :\n\nProduit : {instance.produit.nom}\nQuantité : {instance.quantite}\nDate : {instance.date_commande}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [instance.client.email]

    send_mail(subject, message, from_email, recipient_list)
    
'''@receiver(post_save, sender=Commandes)
def send_order_notification(sender, instance, created, **kwargs):
    if created:
        send_order_email(instance)  # Envoyer l'e-mail à l'administrateur
        send_order_confirmation_email(instance)  # Envoyer l'e-mail au client'''