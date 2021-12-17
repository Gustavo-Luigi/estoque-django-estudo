from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
        labels = {
            'username': 'Nome de usuário',
            'email': 'E-mail',
            'username': 'Nome de usuário',
            'password1': 'Senha',
            'password2': 'Confirme sua senha'
        }

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        labels = {
            'username': 'Nome de usuário',
            'password': 'Senha',
        }