# Generated by Django 3.2 on 2023-08-09 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('banners', '0002_banners_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='banners',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Administrateur'),
        ),
    ]
