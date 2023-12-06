from django.urls import path
from .views import *

app_name = 'purchases'
urlpatterns = [
     
     path('list_commandes/', commandes, name='list_commandes'),
     path('valider_commande', valider_commande_produit, name='valider_commande'),
     path('list_transactions/', transactions, name='list_transactions'),
     path('cinetpay-notification/', cinetpay_notification, name='cinetpay_notification'),
     
]