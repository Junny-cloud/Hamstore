from django.contrib.admin import AdminSite
from django.contrib import admin

class MyAdminSite(AdminSite):
    # Personnalisation de l'option app_index_template
    index_template = 'admin/config/app_index.html'


admin.site = MyAdminSite()

myadmin = admin.site