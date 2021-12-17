from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


from .forms import CustomUserCreationForm, LoginForm

# Create your views here.


def register(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            try:
                user.save()
                messages.success(request, 'Conta criada com sucesso!')
                login(request, user)
                return redirect('home')
            except:
                messages.error(request, 'Usuário já cadastrado')
                context = {'form': form}
                return render(request, 'users/register.html', context)
        else:
            messages.error(request, 'Confira seus dados')
            context = {'form': form}
            return render(request, 'users/register.html', context)

    context = {'form': form}
    return render(request, 'users/register.html', context)


def login_page(request):
    url = 'users/login.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        context = {'form': form}

        try:
            user = User.objects.get(username=request.POST['username'])
        except:
            messages.error(request, 'Usuário não encontrado')
            return render(request, url, context)

        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nome de usuário ou senha incorretos')
            return render(request, url, context)

    form = LoginForm()
    context = {'form': form}
    return render(request, url, context)


def logout_user(request):
    logout(request)
    return redirect('login')
