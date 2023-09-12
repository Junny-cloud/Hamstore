from django.shortcuts import render
from django.views import View

class BannerView(View):
    def get(self, request):
        # Logique de la vue
        context={
            'title':"banners",
            'autre': 'test'
        }
        return render(request, 'banners/list_banners.html', context)
    
def banners(request):
    # Récupérez les données que vous souhaitez afficher
    #mes_donnees = VotreModele.objects.all()  # Remplacez par votre requête de récupération de données

    context = {
        'mes_donnees': "mes donnees",
    }

    return render(request, 'admin/banners/list_banners.html', context)

