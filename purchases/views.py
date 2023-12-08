from django.shortcuts import render
from django.db.models import Count, Sum
import json
from datetime import timezone, datetime, timedelta
import json
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, View, TemplateView
from bootstrap_modal_forms.generic import BSModalCreateView,BSModalUpdateView,BSModalDeleteView, BSModalReadView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_POST
import requests
import hashlib
import hmac
from .forms import *
from .models import *
from users.models import *
# Create your views here.

@method_decorator(csrf_exempt)
def commandes(request):

     data = {}
     
     try:
          action = request.POST['action']
          if action == 'list':
               data =[]
               data1 = [obj for obj in Commandes.objects.all().values('id','reference','user__id', 'user__last_name', 'user__first_name','user__telephone', 'user__email','total_amount', 'etat_commande','date_registry') ]
               for obj in data1:
                    dx= obj['user__last_name'] + ' '+ obj['user__first_name']
                    tel = obj['user__email']
                    if  obj['user__telephone'] :
                         tel = obj['user__telephone'] + ' '+ obj['user__email']
                    obj['info']= {'nom_prenom':dx, 'contact':tel, 'id':obj['id'], 'etat_commande':obj['etat_commande']}
                    data.append(obj) 

          elif action == 'update':

               obj = Commandes.objects.get(pk=request.POST['id'])
               form = CommandesForm(request.POST, instance=obj)
               if form.is_valid():
                    form.save()
               else:
                    data['error'] = form.errors
                    form = CommandesForm()

          elif action == 'details':
               data = [obj for obj in ProduitsCommandes.objects.filter(commande=request.POST['id']).values('product__name', 'product__price', 'quantity', 'variante__name', 'price_unitaire','variante__reference','subtotal')]
                
          elif action == 'delete':
               obj = Commandes.objects.get(pk=request.POST['id'])
               obj.delete()
          else:
               data['error'] = 'Pas de données'
     except Exception as e:
          data['error'] = str(e)
     return JsonResponse(data, safe=False)


@csrf_exempt
def valider_commande_produit(request):
     message = ''
     success = False
     data = None
     if request.method == 'POST':

          validation = json.loads(request.body.decode('utf-8')).get('valider')
          id_commande = json.loads(request.body.decode('utf-8')).get('id')
          
                    
          if validation:
               t = Commandes.objects.get(id=id_commande)
               t.etat_commande = validation # change field
               t.save() 

               if validation =="Valider":

                    all_products = ProduitsCommandes.objects.filter(commande=t).values('id','product__id', 'variante__id', 'variante__quantite_en_stock','quantity')
                    for obj in all_products:
                         df = Variantes.objects.get(id=int(obj['variante__id']))
                         df.quantite_en_stock = int(df.quantite_en_stock) - int(obj['quantity'])
                         
                         df.save()
                         
                         print(df.quantite_en_stock)
               
               message = 'demande bien enregistré !'
               success = True

          data = {
               'message': message,
               'success': success
          }

          return JsonResponse(data, safe=False)

     else:
          message = 'Erreur: Requête non autorisée !'
          data = {
               'message': message,
               'success': success
          }

     return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt)
def transactions(request):

     data = {}
     
     try:
          action = request.POST['action']
          if action == 'list':
              
               data = [obj for obj in Transactions.objects.all().values('id','transaction_id','commande__reference', 'amount', 'currency','payment_method', 'metadata','operator_id', 'payment_date','status') ]
               
          elif action == 'delete':
               obj = Transactions.objects.get(pk=request.POST['id'])
               obj.delete()
          else:
               data['error'] = 'Pas de données'
     except Exception as e:
          data['error'] = str(e)
     return JsonResponse(data, safe=False)



          
# Dans views.py de votre application Django



# Remplacez ces valeurs par celles de votre application
api_key = "41958300655256ed137035.56828933"
site_id = "5865789"
api_secret = "154549357365525d660d2e50.97252741"

verification_url = "https://api-checkout.cinetpay.com/v2/payment/check"

@csrf_exempt  # Permet les requêtes POST sans CSRF token
@require_POST  # Assure que la vue n'accepte que les requêtes POST
def cinetpay_notification(request):
     try:
          # Vérifiez la signature
          '''received_signature = request.headers.get('x-token')
          expected_signature = verify_cinetpay_signature(request.body.decode('utf-8'))

          if received_signature != expected_signature:
               return JsonResponse({"error": "Invalid signature"}, status=401)'''

          # Récupérez les données de la requête
          cpm_trans_id = request.POST.get('cpm_trans_id')
          cpm_site_id = request.POST.get('cpm_site_id')
          cpm_trans_date = request.POST.get('cpm_trans_date')
          # Ajoutez d'autres paramètres selon vos besoins

          # Vérifiez le statut dans votre base de données
          # Si le statut est déjà à succès, ne faites rien
          # Sinon, effectuez une vérification de transaction avec CinetPay
          # et mettez à jour le statut dans votre base de données

          # Exemple de vérification de transaction
          verification_data = {
               "apikey": api_key,
               "site_id": site_id,
               "transaction_id": cpm_trans_id
          }

          verification_response = requests.post(verification_url, json=verification_data)
          verification_result = verification_response.json()

          # Mettez à jour votre base de données en fonction de la réponse de CinetPay
          print(verification_result)
          transaction = Transactions.objects.all().first()
          # Livrez le service si le paiement est réussi
          if verification_result.get("code") == "00":
               transaction_data = verification_result.get("data")
               try:
                    transaction = Transactions.objects.get(transaction_id=cpm_trans_id)
               except Transactions.DoesNotExist:
                    raise Exception("La transaction initiée n'existe pas")
               
               amount = transaction_data['amount'] 
               currency = transaction_data['currency']
               status = transaction_data['status']
               payment_method = transaction_data['payment_method']
               description = transaction_data['description']
               metadata = transaction_data['metadata']
               operator_id = transaction_data['operator_id']
               payment_date = transaction_data['payment_date']
               
               if amount is not None:
                    transaction.amount = amount
               if currency is not None:
                    transaction.currency = currency
               if status is not None:
                    transaction.status = status
               if payment_method is not None:
                    transaction.payment_method = payment_method
               if description is not None:
                    transaction.description = description
               if metadata is not None:
                    transaction.metadata = metadata
               if operator_id is not None:
                    transaction.operator_id = operator_id
               if payment_date is not None:
                    transaction.payment_date = payment_date

               transaction.save()
          elif  verification_result.get("code")=="627":
               transaction_data = verification_result.get("data")
               try:
                    transaction = Transactions.objects.get(transaction_id=cpm_trans_id)
               except Transactions.DoesNotExist:
                    raise Exception("La transaction initiée n'existe pas")
               
               amount = transaction_data['amount'] 
               currency = transaction_data['currency']
               status = transaction_data['status']
               payment_method = transaction_data['payment_method']
               description = transaction_data['description']
               metadata = transaction_data['metadata']
               operator_id = transaction_data['operator_id']
               payment_date = transaction_data['payment_date']
               
               if amount is not None:
                    transaction.amount = amount
               if currency is not None:
                    transaction.currency = currency
               if status is not None:
                    transaction.status = status
               if payment_method is not None:
                    transaction.payment_method = payment_method
               if description is not None:
                    transaction.description = description
               if metadata is not None:
                    transaction.metadata = metadata
               if operator_id is not None:
                    transaction.operator_id = operator_id
               if payment_date is not None:
                    transaction.payment_date = payment_date

               transaction.save()
               
               # Livrez le service et mettez à jour votre base de données

          return JsonResponse({"success": True}, status=200)

     except Exception as e:
          return JsonResponse({"error": str(e)}, status=500)

def verify_cinetpay_signature(data):
    # Assurez-vous d'utiliser la clé secrète que vous avez configurée avec CinetPay
    secret_key = api_secret.encode('utf-8')
    signature = hmac.new(secret_key, data.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature
