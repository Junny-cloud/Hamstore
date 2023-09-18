from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .stats import *
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.admin import AdminSite


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirige vers la page de connexion après la déconnexion

    def get_next_page(self):
        next_page = self.next_page
        if not next_page or not is_safe_url(
            url=next_page,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            next_page = reverse_lazy('login')  # Si l'URL fournie n'est pas valide, redirige vers la page de connexion
        return next_page
    
    
def stats_data(request):
    data = stats_json
    
    return JsonResponse(data=data)
    

def newdashboard(request):
    # Récupérez les données que vous souhaitez afficher
    #mes_donnees = VotreModele.objects.all()  # Remplacez par votre requête de récupération de données

    context = {
        'mes_donnees': "mes donnees",
    }

    return render(request, 'admin/base_site.html', context)






