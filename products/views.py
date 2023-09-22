from django.shortcuts import render
from django.db.models import Count, Sum
import json
from datetime import timezone, datetime, timedelta

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
from .models import *
from users.models import *
# Create your views here.

@method_decorator(csrf_exempt)
def stock_produits(request):

    data = {}
    
    try:
        action = request.POST['action']
        
        if action == 'list':
            data =[]
            data1 =[obj for obj in Products.objects.all().select_related('variantes').values('id','name','variantes__id', 'variantes__reference', 'variantes__name','price', 'variantes__quantite_en_stock', 'variantes__date_modification','sub_category')]
            for obj in data1:
                img = Image.objects.filter(product__id=obj['id']).first()
                obj['img']= img.image.url
                data.append(obj) 
        elif action == 'details':
           
           pass
            
        elif action == 'delete':
            obj = Products.objects.get(pk=request.POST['id'])
            obj.delete()
        else:
            data['error'] = 'Pas de données'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


@csrf_exempt
def ajouter_stock(request):
    message = ''
    success = False
    data = None
    if request.method == 'POST':

        quantite =int( json.loads(request.body.decode('utf-8')).get('quantite'))
        id_variante = json.loads(request.body.decode('utf-8')).get('id')
        
                
        if quantite:
            t = Variantes.objects.get(id=id_variante)
            t.quantite_en_stock += quantite # change field
            t.save() 

            
            message = 'quantité ajouter avec success !'
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

@csrf_exempt
def details_stock(request):
    message = ''
    success = False
    data = None
    if request.method == 'POST':

        variante =int( json.loads(request.body.decode('utf-8')).get('variante'))
        id = json.loads(request.body.decode('utf-8')).get('id')
        print(variante)
                
        if id and variante:
            data =[]
            td = Products.objects.prefetch_related('description_precise').prefetch_related('images').get(variantes__id=variante)
            tx = Products.objects.get(variantes__id=variante).select_related('variantes').prefetch_related('images').values('id','name','sub_category','extras', 'price','prix_promo', 'description','variantes__id', 'variantes__reference', 'variantes__name', 'variantes__quantite_en_stock', 'variantes__date_modification')
            data1 =Products.objects.get(id=id, variantes__id=variante).select_related('variantes').values('id','name','sub_category','extras', 'price','prix_promo', 'description','variantes__id', 'variantes__reference', 'variantes__name', 'variantes__quantite_en_stock', 'variantes__date_modification')
            for obj in data1:
                img =[obj.image.url for obj in Image.objects.get(product__id=obj['id'])]
                obj['img']=img
                data.append(obj) 

        return JsonResponse(data, safe=False)

    else:
        message = 'Erreur: Requête non autorisée !'
        data = {
            'message': message,
            'success': success
        }

    return JsonResponse(data, safe=False)