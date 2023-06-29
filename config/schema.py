import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import graphql
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload
from users.models import *
from purchases.models import *
from products.models import *
from banners.models import *
from newsletters.models import *

# ---------------  APP PRODUITS  -----------------------
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "image")

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
        products = Product.objects.all()

        if category_id:
            products = products.filter(subcategory__category_id=category_id)

        if min_price is not None:
            products = products.filter(price__gte=min_price)

        if max_price is not None:
            products = products.filter(price__lte=max_price)

        return products

    def resolve_product(self, info, id):
        return Products.objects.get(id=id)

# ------------------- CATEGORY CRUD ---------------------
class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        image = Upload()

    category = graphene.Field(CategoryType)

    def mutate(self, info, name, image):
        category = Category(name=name, image=image)
        category.save()
        return CreateCategory(category=category)

class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        image = graphene.String()

    category = graphene.Field(CategoryType)

    def mutate(self, info, id, name=None, image=None):
        try:
            category = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            raise Exception("La catégorie spécifiée n'existe pas")

        if name is not None:
            category.name = name
        if image is not None:
            category.image = image

        category.save()
        return UpdateCategory(category=category)

class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            category = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            raise Exception("La catégorie spécifiée n'existe pas")

        category.delete()
        return DeleteCategory(success=True)


# ------------------- SUBCATEGORY CRUD ---------------------
class SubcategoryInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    category_id = graphene.ID(required=True)

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

class UpdateSubcategory(graphene.Mutation):
    class Arguments:
        subcategory_id = graphene.ID(required=True)
        subcategory_data = SubcategoryInput(required=True)

    subcategory = graphene.Field(SubCategoryType)

    @staticmethod
    def mutate(root, info, subcategory_id, subcategory_data=None):
        try:
            subcategory = Subcategory.objects.get(pk=subcategory_id)
        except Subcategory.DoesNotExist:
            raise Exception("Subcategory not found")

        subcategory.name = subcategory_data.name
        subcategory.save()

        return UpdateSubcategory(subcategory=subcategory)

class DeleteSubcategory(graphene.Mutation):
    class Arguments:
        subcategory_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, subcategory_id):
        try:
            subcategory = Subcategory.objects.get(pk=subcategory_id)
        except Subcategory.DoesNotExist:
            raise Exception("Subcategory not found")

        subcategory.delete()

        return DeleteSubcategory(success=True)

#------------------ PRODUCTS CRUD ------------------------
'''class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    extras = graphene.String(required=True)
    price = graphene.Float(required=True)
    sub_category = graphene.ID(required=True)
    description = graphene.String(required=True)
    description_precise = graphene.String(required=True)
    images = graphene.List(Scalar, required=False)

class CreateProduct(graphene.Mutation):
    class Arguments:
        product_data = ProductInput(required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, product_data):
        name = product_data.name
        description = product_data.description
        price = product_data.price
        category_id = product_data.category

        # Créez le produit dans la base de données avec les données fournies
        product = Product(name=name, description=description, price=price, category_id=category_id)
        product.save()

        # Récupérez l'ID du produit créé
        product_id = product.id

        # Importez les images du produit via la mutation `addProductImages`
        images = product_data.images
        if images:
            for image in images:
                add_product_image(product_id, image)

        return CreateProduct(product=product)

class AddProductImages(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        images = graphene.List(graphene.String, required=True)

    product = graphene.Field(ProductType)

    def mutate(self, info, product_id, images):
        product = Product.objects.get(id=product_id)
        for image in images:
            product.images.create(image=image)
        return AddProductImages(product=product)  

class DeleteProduct(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            success = True
        except Product.DoesNotExist:
            raise GraphQLError("Invalid product ID.")
        
        return DeleteProduct(success=success)
'''
class UpdateProduct(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        price = graphene.Float()
        category = graphene.ID()

    product = graphene.Field(ProductType)

    @staticmethod
    def mutate(root, info, product_id, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise GraphQLError("Invalid product ID.")

        # Mettez à jour les champs spécifiés dans les arguments kwargs
        for field, value in kwargs.items():
            if value is not None:
                setattr(product, field, value)
        try:
            product.full_clean()
            product.save()
        except ValidationError as e:
            raise GraphQLError(f"Validation error: {str(e)}")

        return UpdateProduct(product=product)


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
