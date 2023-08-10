from django.db import models
import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import graphql
from django.core.exceptions import FieldDoesNotExist
from graphene import relay
from graphql import GraphQLError
from .models import *
from products.models import *
from django.contrib.auth.models import User


class CommandesType(DjangoObjectType):
    class Meta:
        model = Commandes
        fields = "__all__"
        
class CommandesFilterInput(graphene.InputObjectType):
    # Ajoutez les champs que vous souhaitez filtrer
    date_commande = graphene.Date()
    user = graphene.ID()
    skip = graphene.Int()

class FavoriteProductsType(DjangoObjectType):
    class Meta:
        model = FavoriteProducts
        fields = '__all__' 
        


class ProduitsCommandesType(DjangoObjectType):
    class Meta:
        model = ProduitsCommandes
        fields = "__all__"
        
class CommandesListType(graphene.ObjectType):
    total_count = graphene.Int()
    commandes = graphene.List(CommandesType) 

class Query(graphene.ObjectType):
    
    commandes = graphene.List(CommandesType, filter=CommandesFilterInput())
    commande = graphene.Field(CommandesType, reference=graphene.String(required=True))
    
    produitscommandes = graphene.List(ProduitsCommandesType)
    produitscommande = graphene.Field(ProduitsCommandesType, id=graphene.ID(required=True))
    
    def resolve_commandes(self, info, filter=None):
        commandes = Commandes.objects.all().order_by('-id')
        total_count = commandes.count()
        
        if filter:
            first = 15
            if filter.skip is None:
                filter.skip=0

            if filter.skip >0:
                filter.skip-=1

            filter.skip =filter.skip*15
            if filter.date_commande is not None:
                commandes = commandes.filter(date_commande=filter.date_commande)
            if filter.user is not None:
                commandes = commandes.filter(user__pk=filter.user)

            
            total_count = commandes.count()  # Obtenir le nombre total de commandes    
            if filter.skip:
                commandes = commandes[filter.skip:]
            else :
                filter.skip =0
                commandes = commandes[filter.skip:]

            if first:
                commandes = commandes[:first]
              
        return CommandesListType(total_count=total_count, commandes=commandes)
        
    
    def resolve_commande(self, info, reference):
        return Commandes.objects.get(reference=reference)
    
    def resolve_produitscommandes(self, info):
        return ProduitsCommandes.objects.all()
    
    def resolve_produitscommande(self, info, slug):
        return ProduitsCommandes.objects.get(id=id)
    
class ProductsCommandesInput(graphene.InputObjectType):
    produit_slug = graphene.String(required=True)
    quantite = graphene.Int(required=True)
    variantes = graphene.List(graphene.ID)


class CreateCommande(graphene.Mutation):
    class Arguments:
        products_commandes = graphene.List(ProductsCommandesInput)
        
    commande = graphene.Field(CommandesType)

    def mutate(self, info, products_commandes):
        user = info.context.user
        commande = Commandes.objects.create(user=user)
        
        total_amount = 0
        
        for ligne in products_commandes:
            produit = Products.objects.get(slug=ligne.produit_slug)
            quantite = ligne.quantite or 1
            
            # Obtenir les variantes à partir des identifiants fournis
            variantes = []
            for variante_id in ligne.variantes:
                variante = Variantes.objects.get(pk=variante_id)
                variantes.append(variante)
            price = 10.00
            if produit.event:
                
                if produit.prix_promo:
                    
                    price = produit.prix_promo 
                else:
                    price=10.00
            else:
                price = produit.price

            ProduitsCommandes.objects.create(
                commande=commande,
                product=produit,
                quantity=quantite,
                price_unitaire=price,
                subtotal=price * quantite,
            )
            total_amount += price * quantite
        
        commande.total_amount = total_amount
        commande.save()
        
        return CreateCommande(commande=commande)


'''class CommandesInput(graphene.InputObjectType):
    status = graphene.Boolean(required=True)
    
class CreateCommandes(graphene.Mutation):
    class Arguments:
        reference = graphene.String(required=True)
        client = graphene.Int(required=True)

    commandes = graphene.Field(CommandesType)

    def mutate(self, info, reference, client):
        commandes = Category(reference=reference, client=client)
        commandes.save()
        return CreateCommandes(commandes=commandes)
    
class UpdateCommandes(graphene.Mutation):
    class Arguments:
        commandes_id = graphene.ID(required=True)
        commandes_data = CommandesInput(required=True)

    commandes = graphene.Field(CommandesType)

    @staticmethod
    def mutate(root, info, commandes_id, commandes_data=None):
        try:
            commandes = Commandes.objects.get(pk=commandes_id)
        except Commandes.DoesNotExist:
            raise Exception("Commandes not found")

        commandes.status = commandes_data.status
        commandes.save()

        return UpdateCommandes(commandes=commandes)
    

class DeleteCommandes(graphene.Mutation):
    class Arguments:
        commandes_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, commandes_id):
        try:
            commandes = Commandes.objects.get(pk=commandes_id)
        except Commandes.DoesNotExist:
            raise Exception("Subcategory not found")

        commandes.delete()

        return DeleteCommandes(success=True)'''

class AddFavorite(graphene.Mutation):
    favoris_product = graphene.Field(FavoriteProductsType)

    class Arguments:
        product_id = graphene.Int()

    def mutate(self, info, product_id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('User not authenticated')

        product = Products.objects.get(pk=product_id)
        favoris_product, created = FavoriteProducts.objects.get_or_create(user=user, product=product)
        favoris_product.save()
        
        return AddFavorite(user=user)
        
class Mutation(graphene.ObjectType):
    create_commandes = CreateCommande.Field()
    add_favorite =AddFavorite.Field()
    
    
#schema = graphene.Schema(query=Query, mutation=Mutation)