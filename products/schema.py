import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import graphql
from users.models import *
from django.contrib.auth.models import User
from graphql import GraphQLError
from graphene import relay
from .models import *
from graphql_auth.decorators import login_required
from graphql_jwt.utils import get_payload
from users.models import *
from users.schema import  renvoyer_user, jwt_payload
# ---------------  APP PRODUITS  -----------------------
<<<<<<< HEAD
=======
class CommentsFilterInput(graphene.InputObjectType):
    # Ajoutez les champs que vous souhaitez filtrer
    client = graphene.ID()
    note = graphene.Int()
    slug_product = graphene.String()
    page = graphene.Int()

>>>>>>> junny-branch
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "image", "slug")

class SubCategoryType(DjangoObjectType):
    class Meta:
        model = SubCategory
        
class VariantesType(DjangoObjectType):
    class Meta:
        model = Variantes
        fields = "__all__"
   
class DescriptionPreciseType(DjangoObjectType):
    class Meta:
        model = DescriptionPrecise
        fields = "__all__"
       
class ImageType(DjangoObjectType):
    class Meta:
        model = Image

class ProductType(DjangoObjectType):
    class Meta:
        model = Products
        

    images = graphene.List(ImageType)

    def resolve_images(self, info):
        return self.images.all()



class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = "__all__"
  
        
class CommentairesType(DjangoObjectType):
    class Meta:
        model = Commentaires
        fields = "__all__"
        

class Query(graphene.ObjectType):
    
    variantes = graphene.List(VariantesType)
    variante = graphene.Field(VariantesType, id=graphene.Int(required=True))
    
    events = graphene.List(EventType)
    event = graphene.Field(EventType, slug=graphene.String(required=True))

<<<<<<< HEAD
    commentaires = graphene.List(CommentairesType)
=======
    commentaires_by_filter = graphene.Field(CommentairesListType, filter=CommentsFilterInput())
>>>>>>> junny-branch
    commentaire = graphene.Field(CommentairesType, id=graphene.Int(required=True))
    
    def resolve_variantes(self, info):
        return Variantes.objects.all()

    def resolve_variante(self, info, id):
        return Variantes.objects.get(id=id)
    
    
    def resolve_events(self, info):
        return Event.objects.all()

    def resolve_event(self, info, slug):
        return Event.objects.get(slug=slug)
    
    def resolve_commentaires(self, info):
        return Commentaires.objects.all()

    def resolve_commentaire(self, info, id):
        return Commentaires.objects.get(id=id)
    
<<<<<<< HEAD
=======
    def resolve_commentaires_by_filter(self, info, filter=None):
        commentaires = Commentaires.objects.all().order_by('-id')
        total_count = commentaires.count()
        
        if filter:
            first = 15
            if filter.page is None:
                filter.page=0

            if filter.page >0:
                filter.page-=1

            filter.page =filter.page*15
            if filter.slug_product is not None:
                commentaires = commentaires.filter(product__slug=filter.slug_product)
            if filter.client is not None:
                commentaires = commentaires.filter(user__pk=filter.client)

            if filter.note is not None:
                commentaires = commentaires.filter(note=filter.note)
                
            total_count = commentaires.count()  # Obtenir le nombre total de produits    
            if filter.page:
                commentaires = commentaires[filter.page:]
            else :
                filter.page =0
                commentaires = commentaires[filter.page:]

            if first:
                commentaires = commentaires[:first]
              
        

        return CommentairesListType(total_count=total_count, commentaires=commentaires)
    
>>>>>>> junny-branch
# ------------------- CATEGORY CRUD ---------------------
class CategoryInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    image = graphene.String()
    
class CreateCategory(graphene.Mutation):
    class Arguments:
        category_data = CategoryInput(required=True)

    category = graphene.Field(CategoryType)
    success = graphene.Boolean()
    
    @staticmethod
    def mutate(self, info, category_data):
        
        name = category_data.name
        image = category_data.image
        category = Category(name=name, image=image)
        category.save()
        return CreateCategory( success=True,category=category)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        category_data = CategoryInput(required=True)

    category = graphene.Field(CategoryType)

    def mutate(self, info, id, category_data=None):
        try:
            category = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            raise Exception("La catégorie spécifiée n'existe pas")
        
        name = category_data.name
        image = category_data.image
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
            subcategory = SubCategory.objects.get(pk=subcategory_id)
        except SubCategory.DoesNotExist:
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
            subcategory = SubCategory.objects.get(pk=subcategory_id)
        except SubCategory.DoesNotExist:
            raise Exception("Subcategory not found")

        subcategory.delete()

        return DeleteSubcategory(success=True)

# -------------------------- VARAINTES CRUD -----------------------------
class VariantesInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    
class CreateVariantes(graphene.Mutation):
    class Arguments:
        variantes_data = VariantesInput(required=True)

    variantes = graphene.Field(VariantesType)
    success = graphene.Boolean()
    
    @staticmethod
    def mutate(self, info, variantes_data):
        
        name = variantes_data.name
        variantes= Category(name=name)
        variantes.save()
        return CreateVariantes( success=True,variantes=variantes)

class UpdateVariantes(graphene.Mutation):
    class Arguments:
        variantes_id = graphene.ID(required=True)
        variantes_data = VariantesInput(required=True)

    variantes = graphene.Field(VariantesType)

    @staticmethod
    def mutate(root, info, variantes_id, variantes_data=None):
        try:
            variantes = Variantes.objects.get(pk=variantes_id)
        except Variantes.DoesNotExist:
            raise Exception("variantes not found")

        variantes.name = variantes_data.name
        variantes.save()

        return UpdateVariantes(variantes=variantes)

class DeleteVariantes(graphene.Mutation):
    class Arguments:
        variantes_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, variantes_id):
        try:
            variantes = Variantes.objects.get(pk=variantes_id)
        except Variantes.DoesNotExist:
            raise Exception("variantes not found")

        variantes.delete()

        return DeleteVariantes(success=True)

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
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
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


class CreateEvent(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        date_limite=graphene.Date(required=True)
        contenu=graphene.String(required=True)
        images = graphene.String()

    events = graphene.Field(EventType)

    def mutate(self, info, title, date_limite, contenu, images):
        events = Event(title=title, date_limite=date_limite, contenu=contenu, images=images)
        events.save()
        return CreateEvent(events=events)

# --------------- COMMENTAIRE CRUD MUTATIONS ------------------------------
class UpdateCommentInput(graphene.InputObjectType):
    comment_id = graphene.Int()
    note = graphene.Int()
    contenu=graphene.String()

<<<<<<< HEAD
class CreateCommentaires(graphene.Mutation):
    class Arguments:
        product_id = graphene.Int(required=True)
        note =graphene.Int()
        contenu=graphene.String(required=True)
        user_id = graphene.Int(required=True)

    commentaires = graphene.Field(CommentairesType)

    def mutate(self, info, product_id, note, contenu, user_id):
        product = Products.objects.get(id=product_id)
        user = CustomUser.objects.get(id=user_id)
        commentaires = Commentaires(product=product, note=note, contenu=contenu, user=user)
        commentaires.save()
        return CreateCommentaires(commentaires=commentaires)
=======
class CreateCommentInput(graphene.InputObjectType):
    product_id = graphene.Int(required=True)
    note = graphene.Int()
    contenu=graphene.String()
>>>>>>> junny-branch
    
    
class CreateComment(graphene.Mutation):
    class Arguments:
        comment_input = CreateCommentInput(required=True)

    success = graphene.Boolean()
    comments = graphene.Field(CommentairesType)

    def mutate(self, info, comment_input):
        request = info.context.META
        user_id =renvoyer_user(request)

        user = CustomUser.objects.get(id=user_id)
        contenu = comment_input.contenu
        note = comment_input.note
        product = Products.objects.get(pk=comment_input.product_id)
        comments = Commentaires(product=product, note=note, contenu=contenu, client=user)
        comments.save()
        return CreateComment(success=True, comments=comments)
    
class DeleteComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, comment_id):
        try:
            comment = Commentaires.objects.get(id=comment_id)
        except Commentaires.DoesNotExist:
            raise Exception(" commentaires not found")

        comment.delete()

        return DeleteComment(success=True)
    
<<<<<<< HEAD
=======
class UpdateComment(graphene.Mutation):
    class Arguments:
        comment_input = UpdateCommentInput(required=True)

    success = graphene.Boolean()
    comments = graphene.Field(CommentairesType)

    @staticmethod
    def mutate(self, info, comment_input):
        
        try:
            comments = Commentaires.objects.get(id=comment_input.comment_id)
        except Commentaires.DoesNotExist:
            raise Exception("vous ne pouvez pas modifier ce commentaire")

        comments.contenu = comment_input.contenu
        comments.note = comment_input.note
        comments.save()

        return UpdateComment(success=True, comments=comments)

           


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()
    update_comment = UpdateComment.Field()
    
   
>>>>>>> junny-branch
