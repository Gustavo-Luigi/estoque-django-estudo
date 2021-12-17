from django.shortcuts import render
from django.utils import timezone

from transaction.models import SiteTransaction

# Create your views here.


def index(request):
    return render(request, 'overview/index.html')
