# Generated by Django 4.0 on 2021-12-14 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0013_alter_user_email'),
        ('products', '0010_product_stock_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='default_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='belongs_to',
            field=models.ForeignKey(auto_created=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
