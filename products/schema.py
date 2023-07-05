import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
import graphql
from graphql import GraphQLError

from .models import *

class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = "__all__"

class CommentairesType(DjangoObjectType):
    class Meta:
        model = Commentaires
        fields = "__all__"
        

class Query(graphene.ObjectType):
    events = graphene.List(EventType)
    event = graphene.Field(EventType, id=graphene.Int(required=True))

    commentaires = graphene.List(CommentairesType)
    commentaire = graphene.Field(CommentairesType, id=graphene.Int(required=True))
    
    def resolve_events(self, info):
        return Event.objects.all()

    def resolve_event(self, info, id):
        return Event.objects.get(id=id)
    
    def resolve_commentaires(self, info):
        return Commentaires.objects.all()

    def resolve_commentaire(self, info, id):
        return Commentaires.objects.get(id=id)
    

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
    
class DeleteCommentaires(graphene.Mutation):
    class Arguments:
        commentaires_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate(root, info, commentaires_id):
        try:
            commentaires = Commentaires.objects.get(pk=commentaires_id)
        except Commentaires.DoesNotExist:
            raise Exception(" commentaires not found")

        commentaires.delete()

        return DeleteCommentaires(success=True)
    
