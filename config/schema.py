import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import graphql
from graphql import GraphQLError
from users.models import *
from purchases.models import *
from products.models import *
from banners.models import *
from newsletters.models import *

# ---------------  APP PRODUITS  -----------------------
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class SubCategoryType(DjangoObjectType):
    class Meta:
        model = SubCategory

        
class ImageType(DjangoObjectType):
    class Meta:
        model = Image

class ProductType(DjangoObjectType):
    class Meta:
        model = Products

    images = graphene.List(ImageType)

    def resolve_images(self, info):
        return self.images.all()




class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    
    # django-graphql-jwt authentication
    # with some extra features
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    
    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.Int(required=True))
    subcategories = graphene.List(SubCategoryType)
    subcategory = graphene.Field(SubCategoryType, id=graphene.Int(required=True))
    products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.Int(required=True))

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_category(self, info, id):
        return Category.objects.get(id=id)

    def resolve_subcategories(self, info):
        return SubCategory.objects.all()

    def resolve_subcategory(self, info, id):
        return SubCategory.objects.get(id=id)

    def resolve_products(self, info):
        return Products.objects.all()

    def resolve_product(self, info, id):
        return Products.objects.get(id=id)

class CreateSubCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        category_id = graphene.Int(required=True)

    subcategory = graphene.Field(SubCategoryType)

    def mutate(self, info, name, category_id):
        category = Category.objects.get(id=category_id)
        subcategory = SubCategory(name=name, category=category)
        subcategory.save()
        return CreateSubCategory(subcategory=subcategory)
    
    
class Mutation(AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
