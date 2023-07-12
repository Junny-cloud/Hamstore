import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import graphql
from graphql import GraphQLError
#from graphene_file_upload.scalars import Upload
from users.models import *
from purchases.models import *
from products.models import *
from banners.models import *
from newsletters.models import *
from users.schema import *
from products.schema import *
from django.core.exceptions import FieldDoesNotExist
class Query(UserQuery, MeQuery, ListUsersQuery,graphene.ObjectType):
    
    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.Int(required=True))

    subcategories = graphene.List(SubCategoryType)
    subcategory = graphene.Field(SubCategoryType, id=graphene.Int(required=True))

    products = graphene.List(ProductType, category_id=graphene.Int(), min_price=graphene.Float(), max_price=graphene.Float())
    product = graphene.Field(ProductType, id=graphene.Int(required=True))

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_category(self, info, id):
        return Category.objects.get(id=id)

    def resolve_subcategories(self, info):
        return SubCategory.objects.all()

    def resolve_subcategory(self, info, id):
        return SubCategory.objects.get(id=id)

    def resolve_products(self, info, category_id=None, min_price=None, max_price=None):
        products = Products.objects.all()

        if category_id:
            products = products.filter(subcategory__category_id=category_id)

        if min_price is not None:
            products = products.filter(price__gte=min_price)

        if max_price is not None:
            products = products.filter(price__lte=max_price)

        return products

    def resolve_product(self, info, id):
        return Products.objects.get(id=id)


class Mutation(AuthMutation, graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()

    create_subcategory = CreateSubCategory.Field()
    update_subcategory = UpdateSubcategory.Field()
    delete_subcategory = DeleteSubcategory.Field()

    '''create_product = CreateProduct.Field()
    add_product_images = AddProductImages.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()'''


schema = graphene.Schema(query=Query, mutation=Mutation)
