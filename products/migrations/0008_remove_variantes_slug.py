# Generated by Django 3.2.5 on 2023-08-03 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_event_subtitle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variantes',
            name='slug',
        ),
    ]