from django.urls import path
from .views import *

app_name = 'products'
urlpatterns = [
     
     path('stock_produits/', stock_produits, name='stock_produits'),
     path('ajouter_stock', ajouter_stock, name='ajouter_stock'),
     path('details/', details_stock, name='details'),
     
]