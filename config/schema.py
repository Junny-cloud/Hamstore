import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
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
from products.schema import Query as productsQuery

from django.core.exceptions import FieldDoesNotExist
from graphene import relay

class ProductFilterInput(graphene.InputObjectType):
    # Ajoutez les champs que vous souhaitez filtrer
    priceRange = graphene.List(graphene.String)
    sort_by_price =graphene.String()
    slug_category = graphene.String()
    slug_subcategory = graphene.String()
    slug_event= graphene.String()
    skip = graphene.Int()

class ProductFilterCategoryInput(graphene.InputObjectType):
    # Ajoutez les champs que vous souhaitez filtrer
    slug = graphene.String()

    skip = graphene.Int()

class SubCategoryFilterInput(graphene.InputObjectType):
    # Ajoutez les champs que vous souhaitez filtrer
    slug = graphene.String()

class ProductListType(graphene.ObjectType):
    total_count = graphene.Int()
    products = graphene.List(ProductType) 
    
class Query(UserQuery, MeQuery, productsQuery, graphene.ObjectType):
    
    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, slug=graphene.String(required=True))

    subcategories = graphene.List(SubCategoryType, filter=SubCategoryFilterInput())
    subcategory = graphene.Field(SubCategoryType, slug=graphene.String(required=True))

    products_by_category_slug = graphene.Field(ProductListType, filter=ProductFilterCategoryInput())
    products_by_subcategory_slug= graphene.Field(ProductListType, filter=ProductFilterInput())
    product = graphene.Field(ProductType, slug=graphene.String(required=True))

    def resolve_categories(self, info):
        return Category.objects.all()

    def resolve_category(self, info, slug):
        return Category.objects.get(slug=slug)

    def resolve_subcategories(self, info ,  filter=None):
        subcategories = SubCategory.objects.all()

        if filter:
            if filter.slug is not None:
                subcategories =subcategories.filter(category__slug=filter.slug)



        return subcategories

    def resolve_subcategory(self, info, slug):
        return SubCategory.objects.get(slug=slug)

    def resolve_products_by_category_slug(self, info, filter=None):
        products = Products.objects.all()
        
        if filter:
            first = 15
            if filter.skip is None:
                filter.skip=0
            filter.skip =filter.skip*15
            if filter.slug is not None:
                products = products.filter(sub_category__category__slug=filter.slug)
            
            
            if filter.skip:
                products = products[filter.skip:]
            

            if first:
                products = products[:first]
        total_count = products.count()  # Obtenir le nombre total de produits

        return ProductListType(total_count=total_count, products=products)
    
    def resolve_products_by_subcategory_slug(self, info, filter=None):
        products = Products.objects.all()
        
        if filter:
            first = 15
            if filter.skip is None:
                filter.skip=0

            if filter.skip >0:
                filter.skip-=1

            filter.skip =filter.skip*15
            if filter.slug_category is not None:
                products = products.filter(sub_category__category__slug=filter.slug_category)
            if filter.slug_subcategory is not None:
                products = products.filter(sub_category__slug=filter.slug_subcategory)

            if filter.slug_event is not None:
                products = products.filter(event__slug=filter.slug_event)

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
            else :
                filter.skip =0
                products = products[filter.skip:]

            if first:
                products = products[:first]
              
        total_count = products.count()  # Obtenir le nombre total de produits

        return ProductListType(total_count=total_count, products=products)


    def resolve_product(self, info, slug):
        return Products.objects.get(slug=slug)


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
