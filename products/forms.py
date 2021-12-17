from django import forms
from django.forms import fields

from products.models import Category, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'cost',
            'category',
            'is_for_sale'
        ]
        labels = {
            'name': 'Nome',
            'price': 'Preço',
            'cost': 'Custo',
            'category': 'Categoria',
            'is_for_sale': 'É produto para venda'
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
            'default_price',
            'default_cost'
        ]
        labels = {
            'name': 'Nome da categoria:',
            'default_price': 'Preço padrão:',
            'default_cost': 'Custo padrão:'
        }
