import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

from .models import *

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


class CreateUser(graphene.Mutation):
     setmail = graphene.String()
     setpassword = graphene.String()
     class Arguments:

          email = graphene.String(required=True)
          firstname = graphene.String(required=True)
          lastname = graphene.String(required=True)
          date_naissance = graphene.Date(required=True)
          abonnes_newsletters = graphene.Boolean(required=True)
          password = graphene.String(required=True)

     user = graphene.Field(CustomUserType)
     
     
     def mutate(self, info, email, firstname, lastname, date_naissance, abonnes_newsletters, password):

          setmail=email
          setpassword=password
          user = CustomUser(
               username=email,
               email=email,
               first_name=firstname,
               last_name=lastname,
               date_naissance=date_naissance,
               abonnes_newsletters=abonnes_newsletters,
          )
          user.set_password(password)
          user.save()
          return CreateUser(user=user, setmail=setmail, setpassword=setpassword)
          
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

class AuthMutation(graphene.ObjectType):
     register = CreateUser.Field()
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
