from django.db.models.query_utils import Q

from .models import Product

def search_products(request):
    if request.GET.get('search') is None:
        products = Product.objects.all().filter(
            belongs_to=request.user, is_for_sale=True).order_by('name')
    else:
        products = Product.objects.all().filter(Q(belongs_to=request.user) & Q(
            name__icontains=request.GET['search']) & Q(is_for_sale=True)).order_by('name')
    
    return products