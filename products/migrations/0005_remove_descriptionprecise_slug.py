# Generated by Django 3.2.5 on 2023-09-15 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_variantes_reference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='descriptionprecise',
            name='slug',
        ),
    ]
