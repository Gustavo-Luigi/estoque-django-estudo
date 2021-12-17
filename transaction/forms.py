from django import forms

from transaction.models import Cart

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = [
            'product',
            'quantity'
        ]
