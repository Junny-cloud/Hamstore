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
from users.models import *
from users.schema import renvoyer_user, jwt_payload


class CommandesType(DjangoObjectType):
    class Meta:
        model = Commandes
        fields = "__all__"
        
class CommandesFilterInput(graphene.InputObjectType):
    # Ajoutez les champs que vous souhaitez filtrer
    date_commande = graphene.Date()
    user = graphene.ID()
    page = graphene.Int()

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
    
    commandes = graphene.Field(CommandesListType, filter=CommandesFilterInput())
    commande = graphene.Field(CommandesType, reference=graphene.String(required=True))
    
    produitscommandes = graphene.List(ProduitsCommandesType)
    produitscommande = graphene.Field(ProduitsCommandesType, id=graphene.ID(required=True))
    
    def resolve_commandes(self, info, filter=None):
        commandes = Commandes.objects.all()
        total_count = commandes.count()
        
        if filter:
            first = 15
            if filter.page is None:
                filter.page=0

            if filter.page >0:
                filter.page-=1

            filter.page =filter.page*15
            if filter.date_commande is not None:
                commandes = commandes.filter(date_commande=filter.date_commande)
            if filter.user is not None:
                commandes = commandes.filter(user__pk=filter.user)

            
            total_count = commandes.count()  # Obtenir le nombre total de commandes    
            if filter.page:
                commandes = commandes[filter.page:]
            else :
                filter.page =0
                commandes = commandes[filter.page:]

            if first:
                commandes = commandes[:first]
              
        return  CommandesListType(total_count=total_count, commandes=commandes)
        
    
    def resolve_commande(self, info, reference):
        return Commandes.objects.get(reference=reference)
    
    def resolve_produitscommandes(self, info):
        return ProduitsCommandes.objects.all()
    
    def resolve_produitscommande(self, info, slug):
        return ProduitsCommandes.objects.get(id=id)
    
class ProductsCommandesInput(graphene.InputObjectType):
    produit_slug = graphene.String(required=True)
    quantite = graphene.Int(required=True)
    variante_id = graphene.Int()
    


class CreateCommande(graphene.Mutation):
    class Arguments:
        products_commandes = graphene.List(ProductsCommandesInput)

    commande = graphene.Field(CommandesType)

    def mutate(self, info, products_commandes):
        request = info.context.META
        user_id = renvoyer_user(request)
        user = CustomUser.objects.get(id=user_id)
        commande = Commandes.objects.create(user=user)
        
        total_amount = 0
        
        for ligne in products_commandes:
            produit = Products.objects.get(slug=ligne.produit_slug)
            quantite = ligne.quantite or 1
            
           
            price = 10
            if produit.event:
                
                if produit.prix_promo:
                    
                    price = produit.prix_promo 
                else:
                    price=10
            else:
                price = produit.price
            variante = Variantes.objects.get(pk=ligne.variante_id)
            variante_name =variante.name
            ProduitsCommandes.objects.create(
                commande=commande,
                product=produit,
                quantity=quantite,
                price_unitaire=price,
                subtotal=price * quantite,
                variante = variante_name
            )
            total_amount += price * quantite
        
        commande.total_amount = total_amount
        commande.save()
        
        return CreateCommande(commande=commande)

class DeleteCommande(graphene.Mutation):
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

        return DeleteCommande(success=True)

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
    

'''

class AddFavoris(graphene.Mutation):
    favoris_product = graphene.Field(FavoriteProductsType)

    class Arguments:
        product_id = graphene.Int(required=True)
        

    def mutate(self, info, product_id):
        request = info.context.META
        user_id =renvoyer_user(request)
        user = CustomUser.objects.get(id=user_id)
        if not user:
            raise Exception('Veillez vous connecter')

        product = Products.objects.get(pk=product_id)
        favoris_product, created = FavoriteProducts.objects.get_or_create(user=user, product=product)
        favoris_product.save()
        
        return AddFavoris(favoris_product=favoris_product)
    
class DeleteFavoris(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, product_id):
        request = info.context.META
        user_id = renvoyer_user(request)
        try:
            favoris_product = FavoriteProducts.objects.get(product__id=product_id, user__id =user_id)
        except FavoriteProducts.DoesNotExist:
            raise Exception("produit favoris n'existe pas")

        favoris_product.delete()

        return DeleteFavoris(success=True)  

class Mutation(graphene.ObjectType):
    create_commande = CreateCommande.Field()
    delete_commande = DeleteCommande.Field()

    add_favoris = AddFavoris.Field()
    delete_favoris = DeleteFavoris.Field()
    
    
#schema = graphene.Schema(query=Query, mutation=Mutation)