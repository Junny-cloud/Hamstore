# Generated by Django 3.2.8 on 2023-07-29 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0006_auto_20230728_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandes',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='produitscommandes',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
