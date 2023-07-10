# Generated by Django 3.0.14 on 2023-07-09 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commandes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank=True, max_length=200, null=True, verbose_name='reference commande')),
                ('date_registry', models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('status', models.BooleanField(default=False, verbose_name='Etat')),
            ],
            options={
                'verbose_name': 'Commande',
                'verbose_name_plural': 'Commandes',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ProduitsCommandes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_product', models.CharField(blank=True, max_length=200, null=True, verbose_name='prix produit')),
                ('date_registry', models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('status', models.BooleanField(default=False, verbose_name='Etat')),
                ('commande', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='purchases.Commandes', verbose_name='commande concerné')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Products', verbose_name='Produit')),
            ],
            options={
                'verbose_name': 'Produit Commandé',
                'verbose_name_plural': 'Produits Commandés',
                'ordering': ['-id'],
            },
        ),
    ]
