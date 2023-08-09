# Generated by Django 3.2.8 on 2023-08-05 02:27

import banners.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='titre banner')),
                ('slug', models.SlugField(null=True, unique=True)),
                ('sub_title', models.CharField(blank=True, max_length=200, null=True, verbose_name='sous titre banner')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description evenement')),
                ('images', models.ImageField(blank=True, null=True, upload_to=banners.models.image_banners, verbose_name='Image')),
                ('date_registry', models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('status', models.BooleanField(default=True, verbose_name='Etat')),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
                'ordering': ['-id'],
            },
        ),
    ]
