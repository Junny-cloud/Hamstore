from django.db import models
import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import graphql
from graphql import GraphQLError
from .models import *
from products.models import *
from django.contrib.auth.models import User

class CommandesFilterInput(graphene.InputObjectType):
    # Ajoutez les champs que vous souhaitez filtrer
    date_commande = graphene.Date()
    user = graphene.ID()


class CommandesType(DjangoObjectType):
    class Meta:
        model = Commandes
        fields = "__all__"

class ProduitsCommandesType(DjangoObjectType):
    class Meta:
        model = ProduitsCommandes
        fields = "__all__"
        

class Query(graphene.ObjectType):
    
    commandes = graphene.List(CommandesType)
    commande = graphene.Field(CommandesType, reference=graphene.String(required=True))
    
    produitscommandes = graphene.List(ProduitsCommandesType)
    produitscommande = graphene.Field(ProduitsCommandesType, id=graphene.ID(required=True))
    
    def resolve_commandes(self, info):
        return Commandes.objects.all()
    
    def resolve_commande(self, info, reference):
        return Commandes.objects.get(reference=reference)
    
    def resolve_produitscommandes(self, info):
        return ProduitsCommandes.objects.all()
    
    def resolve_produitscommande(self, info, slug):
        return ProduitsCommandes.objects.get(id=id)
    
class ProductsCommandesInput(graphene.InputObjectType):
    produit_id = graphene.ID()
    quantite = graphene.Int()
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
            produit = Products.objects.get(pk=ligne.produit_id)
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
    
class Mutation(graphene.ObjectType):
    create_commandes = CreateCommande.Field()
    
    
#schema = graphene.Schema(query=Query, mutation=Mutation)