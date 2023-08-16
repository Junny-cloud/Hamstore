# Generated by Django 3.2.5 on 2023-08-05 03:13

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20230804_1543'),
        ('purchases', '0003_auto_20230710_1340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commandes',
            old_name='client',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='produitscommandes',
            name='price_product',
        ),
        migrations.AddField(
            model_name='commandes',
            name='date_commande',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commandes',
            name='products',
            field=models.ManyToManyField(through='purchases.ProduitsCommandes', to='products.Products'),
        ),
        migrations.AddField(
            model_name='commandes',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='produitscommandes',
            name='price_unitaire',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='prix produit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produitscommandes',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='produitscommandes',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total du produit'),
        ),
        migrations.AddField(
            model_name='produitscommandes',
            name='variante',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='variante choisie'),
        ),
        migrations.AlterField(
            model_name='commandes',
            name='reference',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='reference commande'),
        ),
    ]