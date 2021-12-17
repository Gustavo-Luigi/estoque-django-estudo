from django.shortcuts import render

from products.models import Product

# Create your views here.
def index(request):
    products = Product.objects.all().filter(belongs_to=request.user).order_by('stock__available')
    products = sorted(products, key=lambda product: product.stock.calculate_availability())
    context = {'products': products}
    return render(request, 'stock/index.html', context)