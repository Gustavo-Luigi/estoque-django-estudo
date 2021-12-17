# Generated by Django 4.0 on 2021-12-14 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0014_alter_user_email'),
        ('products', '0017_alter_category_belongs_to_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='belongs_to',
            field=models.ForeignKey(auto_created=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.AlterField(
            model_name='category',
            name='default_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
