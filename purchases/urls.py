from django.urls import path
from .views import *

app_name = 'purchases'
urlpatterns = [
     
     path('list_commandes/', commandes, name='list_commandes'),
     
]