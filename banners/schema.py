import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import graphql
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload
from .model import *
from products.models import *

class BannersInput(graphene.InputObjectType):
     title = graphene.String(required=True)
     sub_title = graphene.String(required=True)
     description = graphene.String(required=True)
     category_id = graphene.ID(required=True)
     images = graphene.String()

class BannersType(DjangoObjectType):
    class Meta:
        model = Banners
        fields = ("id", "title", "description", "sub_title", "category","images")

class CreateBanners(graphene.Mutation):
     class Arguments:
          title = graphene.String(required=True)
          sub_title = graphene.String(required=True)
          description = graphene.String(required=True)
          category_id = graphene.Int(required=True)
          images = graphene.String()

     banners = graphene.Field(CategoryType)

     def mutate(self, info, title, sub_title, description, category_id, images):
          category = Category.objects.get(id=category_id)
          banners = Banners(title=title, sub_title=sub_title, description=description, category=category,images=images)
          banners.save()
          return CreateBanners(banners=banners)

class UpdateBanners(graphene.Mutation):
     class Arguments:
          banners_id = graphene.ID(required=True)
          banners_data = BannersInput(required=True)

     banners = graphene.Field(BannersType)

     @staticmethod
     def mutate(root, info, banners_id, banners_data=None):
          try:
                    category = Category.objects.get(pk=banners_data.category_id)
                    banners = Banners.objects.get(pk=banners_id)
          except Banners.DoesNotExist:
                    raise Exception("Banners not found")

          banners.title = banners_data.title
          banners.sub_title = banners_data.sub_title
          banners.description = banners_data.description
          banners.category = banners_data.category
          banners.images = banners_data.images
          banners.save()

          return UpdateBanners(banners=banners)

'''class DeleteBanners(graphene.Mutation):
     class Arguments:
          banners_id = graphene.ID(required=True)

     success = graphene.Boolean()

     @staticmethod
     def mutate(root, info, banners_id):
          try:
               banners = Banners.objects.get(pk=banners_id)
          except Banners.DoesNotExist:
               raise Exception("banners not found")

          banners.delete()

          return DeleteBanners(success=True)'''