# Generated by Django 4.0 on 2021-12-14 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_remove_sitetransaction_discount_percentage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='is_sale',
            field=models.BooleanField(auto_created=True, default=True),
        ),
        migrations.AlterField(
            model_name='sitetransactiontype',
            name='type_name',
            field=models.CharField(db_index=True, max_length=45),
        ),
    ]
