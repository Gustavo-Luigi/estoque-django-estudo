# Generated by Django 4.0 on 2021-12-14 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_alter_stock_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='available',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='desired_amount',
            field=models.IntegerField(blank=True),
        ),
    ]