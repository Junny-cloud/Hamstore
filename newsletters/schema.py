import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import graphql
from graphql import GraphQLError

from .models import *

class MailingInput(graphene.InputObjectType):
    objet_mail = graphene.String(required=True)
    contenu = graphene.String(required=True)
    

class NewslettersType(DjangoObjectType):
     class Meta:
          model = Newsletters

class MailingType(DjangoObjectType):
     class Meta:
          model = Mailing
class Query(graphene.ObjectType):
    
    newsletters = graphene.List(NewslettersType)
    newsletter = graphene.Field(NewslettersType, id=graphene.Int(required=True))
    
    def resolve_newsletters(self, info):
        return Newsletters.objects.all()
    
    def resolve_newsletter(self, info, id):
        return Newsletters.objects.get(id=id)
    
class CreateNewsletters(graphene.Mutation):
     class Arguments:
          email = graphene.String(required=True)
          
          newsletters = graphene.Field(NewslettersType)

     def mutate(self, info, email):
          newsletters = Newsletters(email=email,)
          newsletters.save()
          return CreateNewsletters(newsletters=newsletters)

class CreateMailing(graphene.Mutation):
     class Arguments:
          objet_mail = graphene.String(required=True)
          contenu = graphene.String(required=True)
          
          mailing = graphene.Field(MailingType)

     def mutate(self, info, contenu, objet_mail):
          mailing = Mailing(objet_mail=objet_mail, contenu=contenu)
          mailing.save()
          return CreateMailing(mailing=mailing)

class UpdateMailing(graphene.Mutation):
    class Arguments:
        mailing_id = graphene.ID(required=True)
        mailing_data = MailingInput(required=True)

    mailing = graphene.Field(MailingType)

    @staticmethod
    def mutate(root, info, mailing_id, mailing_data=None):
        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            raise Exception("mailing not found")

        mailing.objet_mail = mailing_data.objet_mail
        mailing.contenu = mailing_data.contenu
        mailing.save()

        return UpdateMailing(mailing=mailing)

class DeleteNewsletters(graphene.Mutation):
     class Arguments:
          newsletters_id = graphene.ID(required=True)

     success = graphene.Boolean()

     @staticmethod
     def mutate(root, info, newsletters_id):
          try:
               newsletters = Newsletters.objects.get(pk=newsletters_id)
          except Newsletters.DoesNotExist:
               raise Exception("newsletters not found")

          newsletters.delete()

          return DeleteNewsletters(success=True)

class DeleteMailing(graphene.Mutation):
     class Arguments:
          mailing_id = graphene.ID(required=True)

     success = graphene.Boolean()

     @staticmethod
     def mutate(root, info, mailing_id):
          try:
               mailing = Mailing.objects.get(pk=mailing_id)
          except Mailing.DoesNotExist:
               raise Exception("mailing not found")

          mailing.delete()

          return DeleteMailing(success=True)

