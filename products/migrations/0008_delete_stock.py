# Generated by Django 4.0 on 2021-12-11 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_price'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Stock',
        ),
    ]