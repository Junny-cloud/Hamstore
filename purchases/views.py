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
                    obj['info']= {'nom_prenom':dx, 'contact':tel}
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
               data = [obj for obj in ProduitsCommandes.objects.filter(commande=request.POST['id']).values('product__name', 'product__price', 'quantity', 'variante__name', 'subtotal')]
                
          elif action == 'delete':
               obj = Commandes.objects.get(pk=request.POST['id'])
               obj.delete()
          else:
               data['error'] = 'Pas de données'
     except Exception as e:
          data['error'] = str(e)
     return JsonResponse(data, safe=False)
