import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from django.db.models import Q
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
from newsletters.schema import Query as NewslettersQuery
from products.schema import Query as productsQuery, Mutation as productsMutation
from purchases.schema import Mutation as purchasesMutation, Query as purchasesQuery
from banners.schema import  Query as bannersQuery
from django.core.exceptions import FieldDoesNotExist
from graphene import relay
from .stats import *

class ProductFilterInput(graphene.InputObjectType):
    # Ajoutez les champs que vous souhaitez filtrer
    priceRange = graphene.List(graphene.String)
    sort_by_price = graphene.String()
    slug_category = graphene.String()
    slug_subcategory = graphene.String()
    slug_event = graphene.String()
    slug_product = graphene.String()
    page = graphene.Int()

class SearchProductInput(graphene.InputObjectType):
    # Ajoutez les champs que vous souhaitez filtrer
    priceRange = graphene.List(graphene.String)
    sort_by_price = graphene.String()
    slug_category = graphene.String()
    slug_subcategory = graphene.String()
    slug_event = graphene.String()
    search_input = graphene.String()
    page = graphene.Int()

class ProductFilterCategoryInput(graphene.InputObjectType):
    # Ajoutez les champs que vous souhaitez filtrer
    slug = graphene.String()

    page = graphene.Int()

class SubCategoryFilterInput(graphene.InputObjectType):
    # Ajoutez les champs que vous souhaitez filtrer
    slug = graphene.String()

class ProductListType(graphene.ObjectType):
    total_count = graphene.Int()
    products = graphene.List(ProductType) 
    
class Query(UserQuery, MeQuery, productsQuery, purchasesQuery, NewslettersQuery, bannersQuery, graphene.ObjectType):
    user_connected =graphene.Field(CustomUserType, token=graphene.String())
    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, slug=graphene.String(required=True))
    subcategory_group =graphene.List(CategoryType)

    subcategories = graphene.List(SubCategoryType, filter=SubCategoryFilterInput())
    subcategory = graphene.Field(SubCategoryType, slug=graphene.String(required=True))
    subcategory_all = graphene.List(SubCategoryType)

    search_products = graphene.Field(ProductListType, filter=SearchProductInput())
    products_by_category_slug = graphene.Field(ProductListType, filter=ProductFilterCategoryInput())
    products_by_subcategory_slug= graphene.Field(ProductListType, filter=ProductFilterInput())
    product = graphene.Field(ProductType, slug=graphene.String(required=True))
    
    stats = graphene.Field(StatsType)

    def resolve_categories(self, info):
        return Category.objects.all()
    
    def resolve_subcategory_group(self, info):
        return Category.objects.prefetch_related('subcategory_set').all()
    
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
    
    def resolve_subcategory_all(self, info):
        return SubCategory.objects.all()
    
    def resolve_products_by_category_slug(self, info, filter=None):
        products = Products.objects.all()
        total_count = products.count()
        if filter:
            first = 15
            if filter.page is None:
                filter.page=0
            filter.page =filter.page*15
            if filter.slug is not None:
                products = products.filter(sub_category__category__slug=filter.slug)
            
            total_count = products.count()  # Obtenir le nombre total de produits
            if filter.page:
                products = products[filter.page:]
            

            if first:
                products = products[:first]
        

        return ProductListType(total_count=total_count, products=products)
    
    def resolve_products_by_subcategory_slug(self, info, filter=None):
        products = Products.objects.all().order_by('-id')
        total_count = products.count()
        if filter:
            first = 15
            if filter.page is None:
                filter.page=0

            if filter.page >0:
                filter.page-=1

            filter.page =filter.page*15
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

            if filter.slug_product:
                prod_cat =  Products.objects.values('sub_category__slug').filter(slug=filter.slug_product)
                prod_cat=prod_cat[0]['sub_category__slug']
                products = products.filter(Q(sub_category__slug=prod_cat) &  ~Q(slug=filter.slug_product))
                
            total_count = products.count()  # Obtenir le nombre total de produits    
            if filter.page:
                products = products[filter.page:]
            else :
                filter.page =0
                products = products[filter.page:]

            if first:
                products = products[:first]
              
        

        return ProductListType(total_count=total_count, products=products)


    def resolve_product(self, info, slug):
        return Products.objects.get(slug=slug)
    
    def resolve_search_products(self, info, filter=None):
        products = Products.objects.all().order_by('-id')
        total_count = products.count()
        if filter:
            first = 15
            if filter.page is None:
                filter.page=0

            if filter.page >0:
                filter.page-=1

            filter.page =filter.page*15
            if filter.search_input :
                query = filter.search_input
                products = products.filter(
                    Q(name__icontains=query) |
                    Q(sub_category__name__icontains=query) |
                    Q(sub_category__category__name__icontains=query) |
                    Q(description__icontains=query) |
                    Q(description_precise__name__icontains=query)
                ).distinct()
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

           
            total_count = products.count()  # Obtenir le nombre total de produits    
            if filter.page:
                products = products[filter.page:]
            else :
                filter.page =0
                products = products[filter.page:]

            if first:
                products = products[:first]
              
        

        return ProductListType(total_count=total_count, products=products)

    def resolve_user_connected(self, info, token=None):
        request = info.context.META
        user_id =renvoyer_user(request)
        user = CustomUser.objects.get(id=user_id)
        if not user:
            raise Exception('Veillez vous connecter')
        return user
    
    def resolve_stats(self, info):
        return stats_json

    
    


class Mutation(AuthMutation, purchasesMutation, productsMutation, graphene.ObjectType):
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
