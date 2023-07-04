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
    commande = graphene.Field(CommandesType, id=graphene.Int(required=True))
    
    produitscommandes = graphene.List(ProduitsCommandesType)
    produitscommande = graphene.Field(ProduitsCommandesType, id=graphene.Int(required=True))
    
    def resolve_commandes(self, info):
        return Commandes.objects.all()
    
    def resolve_commande(self, info, id):
        return Commandes.objects.get(id=id)
    
    def resolve_produitscommandes(self, info):
        return ProduitsCommandes.objects.all()
    
    def resolve_produitscommande(self, info, id):
        return ProduitsCommandes.objects.get(id=id)
    

class CommandesInput(graphene.InputObjectType):
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

        return DeleteCommandes(success=True)
    
class Mutation(graphene.ObjectType):
    create_commandes = CreateCommandes.Field()
    update_commandes = UpdateCommandes.Field()
    delete_commandes = DeleteCommandes.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)