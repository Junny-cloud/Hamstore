# Generated by Django 3.2.5 on 2023-07-28 10:55

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20230717_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variantes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nom sous-categorie')),
                ('date_registry', models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('status', models.BooleanField(default=True, verbose_name='Etat')),
            ],
            options={
                'verbose_name': 'Variante',
                'verbose_name_plural': 'Variantes',
                'ordering': ['-id'],
            },
        ),
        migrations.AlterField(
            model_name='event',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to=products.models.image_evenements, verbose_name='images'),
        ),
        migrations.AddField(
            model_name='products',
            name='variantes',
            field=models.ManyToManyField(blank=True, to='products.Variantes', verbose_name='les variantes'),
        ),
    ]
