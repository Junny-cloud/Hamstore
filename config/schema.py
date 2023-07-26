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
from graphene import relay
class ProductFilterInput(graphene.InputObjectType):
    # Ajoutez les champs que vous souhaitez filtrer
    priceRange = graphene.List(graphene.String)
    sort_by_price =graphene.String()
    category_product = graphene.ID()

    skip = graphene.Int()
    
    
    
class Query(UserQuery, MeQuery, graphene.ObjectType):
    
    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.Int(required=True))

    subcategories = graphene.List(SubCategoryType)
    subcategory = graphene.Field(SubCategoryType, id=graphene.Int(required=True))

    products = graphene.List(ProductType, filter=ProductFilterInput())
    product = graphene.Field(ProductType, id=graphene.Int(required=True))

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_category(self, info, id):
        return Category.objects.get(id=id)

    def resolve_subcategories(self, info):
        return SubCategory.objects.all()

    def resolve_subcategory(self, info, id):
        return SubCategory.objects.get(id=id)

    def resolve_products(self, info, filter=None):
        products = Products.objects.all()
        
        if filter:
            first = 15
            filter.skip =filter.skip*15
            if filter.category_product is not None:
                products = products.filter(sub_category__id=filter.category_product)
            if filter.priceRange:
                tx = products.filter(price=0)
                for obj in filter.priceRange:
                    
                    if obj=='intervale_1' :
                        tx = tx|products.filter(price__range=(0.0, 10000.0))
                    if obj=='intervale_2' :
                        tx = tx|products.filter(price__range=(10001.0, 20000.0))
                    if obj=='intervale_3' :
                        tx = tx|products.filter(price__range=(20001.0, 50000.0))
                    if obj=='intervale_4' :
                        tx = tx|products.filter(price__range=(50001.0, 100000.0))
                    if obj=='intervale_5' :
                        tx = tx|products.filter(price__gte=100001.0)
                products=tx
            if filter.sort_by_price:
                # Trier les produits en fonction du prix dans l'ordre spécifié
                if filter.sort_by_price == "price_desc":
                    products = products.order_by("-price")
                elif filter.sort_by_price == "price_asc":
                    products = products.order_by("price")
                else:
                    products = products.order_by("date_registry")

            if filter.skip:
                products = products[filter.skip:]
            if first:
                products = products[:first]

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
