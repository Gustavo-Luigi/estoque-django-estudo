# Generated by Django 4.0 on 2021-12-14 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_category_default_cost_alter_category_belongs_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_for_sale',
            field=models.BooleanField(default=True),
        ),
    ]