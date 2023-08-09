import graphene
import graphql_auth
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from graphql import GraphQLError
from .models import *
from django.contrib.auth import authenticate


REGISTER_MUTATION_FIELDS = [
    ('email', graphene.String(required=True)),
    ('first_name', graphene.String(required=True)),
    ('last_name', graphene.String(required=True)),
    ('date_naissance', graphene.String(required=True)),
    ('abonnes_newsletters', graphene.Boolean()),
    ('password', graphene.String(required=True)),
]

class CustomUserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
class ListUsersQuery(graphene.ObjectType):
    ListUsers = graphene.List(CustomUserType)

    def resolve_list_users(self, info):
        # Récupérez la liste des utilisateurs de votre source de données (par exemple, base de données)
        ListUsers = CustomUser.objects.all()
        return ListUsers
class UserInput(graphene.InputObjectType):
     email = graphene.String(required=True)
     firstname = graphene.String(required=True)
     lastname = graphene.String(required=True)
     date_naissance = graphene.Date(required=True)
     abonnes_newsletters = graphene.Boolean(required=True)
     password = graphene.String(required=True)
     
class CreateUser(graphene.Mutation):
     class Arguments:
          input = UserInput(required=True)
          
     user = graphene.Field(CustomUserType)
     success = graphene.Boolean()
     setpassword = graphene.String()
     
     def mutate(self, info, input):
          
          email = input.email
          firstname = input.firstname
          lastname = input.lastname
          date_naissance = input.date_naissance
          abonnes_newsletters = input.abonnes_newsletters
          username = input.email
          password = input.password
          # Check if email is already used
          if CustomUser.objects.filter(email=email).exists():
               raise GraphQLError('Cet e-mail est déjà utilisé par un autre utilisateur.')

          user = CustomUser(
               username=username,
               email=email,
               first_name=firstname,
               last_name=lastname,
               date_naissance=date_naissance,
               abonnes_newsletters=abonnes_newsletters,
          )
          user.set_password(password)
          user.save()
          return CreateUser(user=user, success=True, setpassword=password)
          
class CustomRegister(mutations.Register):
     class Arguments:
        pass

     @classmethod
     def perform_mutate(cls, form, info):
          email = form.cleaned_data.get('email')
          firstname = form.cleaned_data.get('first_name')
          lastname = form.cleaned_data.get('last_name')
          date_naissance = form.cleaned_data.get('date_naissance')
          abonnes_newsletters = form.cleaned_data.get('abonnes_newsletters')
          password = form.cleaned_data.get('password1')
          username = email + 'compte'
          print(email)
          user = CustomUser.objects.create_user(
               username=username,
               email=email,
               firstname=firstname,
               lastname=lastname,
               date_naissance=date_naissance,
               abonnes_newsletters=True,
               password=password
          )

          return CustomRegister(user=user)

class YourInputObjectType(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)

class AuthToken(graphene.ObjectType):
    token = graphene.String()
    user = graphene.Field(graphene.NonNull(graphene.String))
    
class AddFavorite(graphene.Mutation):
    user = graphene.Field(CustomUserType)

    class Arguments:
        product_id = graphene.Int()

    def mutate(self, info, product_id):
        user = info.context.user.username
        if not user.is_authenticated:
            raise Exception('User not authenticated')

        product = Products.objects.get(pk=product_id)
        user, created = CustomUser.objects.get_or_create(username=user)
        user.favorite_products.add(product)
        user.save()
        
        return AddFavorite(user=user)
   
class AuthMutation(graphene.ObjectType):
     add_favorite = AddFavorite.Field()
     register = CreateUser.Field()
     verify_account = mutations.VerifyAccount.Field()
     resend_activation_email = mutations.ResendActivationEmail.Field()
     send_password_reset_email = mutations.SendPasswordResetEmail.Field()
     password_reset = mutations.PasswordReset.Field()
     #password_set = mutations.PasswordSet.Field()
     password_change = mutations.PasswordChange.Field()
     archive_account = mutations.ArchiveAccount.Field()
     delete_account = mutations.DeleteAccount.Field()
     update_account = mutations.UpdateAccount.Field()
     send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
     verify_secondary_email = mutations.VerifySecondaryEmail.Field()
     swap_emails = mutations.SwapEmails.Field()

     # django-graphql-jwt authentication
     # with some extra features
     login = mutations.ObtainJSONWebToken.Field()
     logout = mutations.RevokeToken.Field()
     verify_token = mutations.VerifyToken.Field()
     refresh_token = mutations.RefreshToken.Field()
     
     #login = graphene.Field(AuthToken, credentials=YourInputObjectType(required=True))

     def resolve_token_auth(self, info, credentials):
          email = credentials.email
          password = credentials.password

          user = authenticate(email=email, password=password)

          if user is None:
               raise GraphQLError('Invalid email or password.')

          token = graphql_auth.shortcuts.get_token(user)

          return AuthToken(token=token, user=user)




