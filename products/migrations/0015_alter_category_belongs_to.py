# Generated by Django 4.0 on 2021-12-14 02:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0014_alter_user_email'),
        ('products', '0014_alter_category_belongs_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='belongs_to',
            field=models.ForeignKey(auto_created=True, blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
