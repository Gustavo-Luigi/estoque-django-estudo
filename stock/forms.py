from django import forms


from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model= Stock
        fields = [
            'available',
            'desired_amount'
        ]
        labels = {
            'available': 'Disponível em estoque',
            'desired_amount': 'Estoque desejado'
        }