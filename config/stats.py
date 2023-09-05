import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from django.db.models import Q
from graphql_auth import mutations
import graphql
from django.http import JsonResponse
from graphql import GraphQLError
#from graphene_file_upload.scalars import Upload
from users.models import *
from purchases.models import *
from products.models import *
from banners.models import *
from newsletters.models import *
from users.schema import *
from products.schema import *
from newsletters.schema import Query as NewslettersQuery
from products.schema import Query as productsQuery, Mutation as productsMutation
from purchases.schema import Mutation as purchasesMutation, Query as purchasesQuery
from django.core.exceptions import FieldDoesNotExist
from graphene import relay
from django.db.models import Count, Sum, Q
from datetime import timezone, datetime, timedelta, date
from django.utils import timezone
from django.db.models.functions import Coalesce
import json


today = timezone.now()
yesterday = today - timedelta(2)
year = today.year
month = today.month
day = today.day


def vente_data():
    data_month = []
    for m in range(1, 13):
        total = Commandes.objects.filter(Q(date_registry__year=year, date_registry__month=m)).aggregate(somme_prix=Coalesce(Sum('total_amount'), 0))['somme_prix']
        data_month.append(int(total))
    return data_month
    


today_commandes_count = Commandes.objects.filter(date_registry=date.today()).count()
today_commandes_total = Commandes.objects.filter(date_registry=date.today()).aggregate(somme_prix=Coalesce(Sum('total_amount'), 0))['somme_prix']

month_commandes_count =Commandes.objects.filter(Q(date_registry__year=year, date_registry__month=month)).count() 
month_commandes_total =Commandes.objects.filter(Q(date_registry__year=year, date_registry__month=month)).aggregate(somme_prix=Coalesce(Sum('total_amount'), 0))['somme_prix']

year_commandes_valide_count = Commandes.objects.filter(Q(date_registry__year=year, status=True)).count() 
year_commandes_count = Commandes.objects.filter(Q(date_registry__year=year, status=True)).count() 
year_commandes_total = Commandes.objects.filter(Q(date_registry__year=year, status=True)).aggregate(somme_prix=Coalesce(Sum('total_amount'), 0))['somme_prix']

montant_vente_per_month = vente_data()

produits_count_commandes = [obj for obj in ProduitsCommandes.objects.values('product__name', 'product__price','product__image').annotate(Sum('product__name')).order_by('product__name') if obj['product__name__sum'] >0]

product_count = Products.objects.all().count()
client_count = CustomUser.objects.filter(is_staff=False).count() 
commentaires_count = Commentaires.objects.all().count()
admin_count = CustomUser.objects.filter(is_staff=True).count() 

# Votre JSON en tant que variable
stats_json = {
    "today_commandes_count":today_commandes_count,
    "today_commandes_total": today_commandes_total,
    
    "month_commandes_count": month_commandes_count,
    "month_commandes_total": month_commandes_total,
    
     "year_commandes_valide_count":year_commandes_valide_count,
    "year_commandes_count": year_commandes_count,
     "year_commandes_total": year_commandes_total,
    
    "montant_vente_per_month": montant_vente_per_month,
    "produits_count_commandes": produits_count_commandes,
    
    "product_count":product_count,
    "client_count": client_count,
    
    "commentaires_count": commentaires_count,
    "admin_count": admin_count,
}

class ProduitsCountCommandesType(graphene.ObjectType):
    product__name =graphene.String()
    product__price =graphene.Int()
    product__image = graphene.String()
    product__name__sum = graphene.Int()
# Définissez un type GraphQL pour votre JSON
class StatsType(graphene.ObjectType):
    
    today_commandes_count =graphene.Int()
    today_commandes_total  =graphene.Int()
    month_commandes_count =graphene.Int()
    month_commandes_total =graphene.Int()
    year_commandes_valide_count =graphene.Int()
    year_commandes_count =graphene.Int()
    year_commandes_total  =graphene.Int()
    montant_vente_per_month =graphene.List(graphene.Int) 
    produits_count_commandes  =graphene.List(ProduitsCountCommandesType) 
    product_count =graphene.Int()
    client_count =graphene.Int()
    commentaires_count =graphene.Int()
    admin_count =graphene.Int()
    
