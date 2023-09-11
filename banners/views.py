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

