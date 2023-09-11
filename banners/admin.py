from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html

class BannersAdmin(admin.ModelAdmin):
    change_list_template = "admin/banners/list_banners.html"

    def ma_page_link(self):
        link = reverse("/")
        return format_html(f'<a href="{link}">test banners</a>')

    ma_page_link.short_description = "Lien vers ma page personnalisée"

admin.site.register(Banners, BannersAdmin)