# Generated by Django 3.1.3 on 2023-07-28 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0005_auto_20230717_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandes',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
        migrations.AddField(
            model_name='produitscommandes',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
