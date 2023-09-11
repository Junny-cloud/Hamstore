from django.urls import path
from .views import *

urlpatterns = [
    path('', BannerView.as_view(), name='list_banners'),
]