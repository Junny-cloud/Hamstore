# Generated by Django 3.2.5 on 2023-09-15 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20230912_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variantes',
            name='reference',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True),
        ),
    ]
