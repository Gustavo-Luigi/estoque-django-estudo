# Generated by Django 4.0 on 2021-12-14 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='belongs_to',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='product',
        ),
    ]