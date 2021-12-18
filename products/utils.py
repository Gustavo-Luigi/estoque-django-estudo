from django.contrib import messages
from django.db.models.query_utils import Q
from django.shortcuts import redirect

from stock.forms import StockForm

from .models import Category, Product
from .forms import ProductForm

def search_products(request):
    if request.GET.get('search') is None:
        products = Product.objects.all().filter(
            belongs_to=request.user, is_for_sale=True).order_by('name')
    else:
        products = Product.objects.all().filter(Q(belongs_to=request.user) & Q(
            name__icontains=request.GET['search']) & Q(is_for_sale=True)).order_by('name')
    
    return products

def generate_product_form(request, instance=None):
    undefined_category, created = Category.objects.get_or_create(name='Indefinido')

    selected_category_form = request.POST.get('category', undefined_category.id)
    try:
        selected_category = Category.objects.get(id=selected_category_form)
    except:
        messages.error(request, 'Categoria inválida')
        return redirect('insert-product')

    if selected_category.belongs_to != request.user and selected_category.belongs_to != None:
        messages.error(request, 'Categoria inválida')
        return redirect('insert-product')

    if request.POST['price'] == '':
        price = selected_category.default_price
    else:
        price = request.POST['price']

    if request.POST['cost'] == '':
        cost = selected_category.default_cost
    else:
        cost = request.POST['cost']

    is_for_sale = request.POST.get('is_for_sale', False)

    if instance:
        return ProductForm({
        'name': request.POST['name'],
        'price': price,
        'cost': cost,
        'category': request.POST['category'],
        'is_for_sale': is_for_sale,
    }, instance=instance)

    return ProductForm({
        'name': request.POST['name'],
        'price': price,
        'cost': cost,
        'category': request.POST['category'],
        'is_for_sale': is_for_sale,
    })

def generate_stock_form(request, instance=None):
    if request.POST['available'] == '':
            available = 0
    else:
        available = request.POST['available']

    if request.POST['desired_amount'] == '':
        desired_amount = 0
    else:
        desired_amount = request.POST['desired_amount']

    if instance:
        return StockForm({
            'available': available,
            'desired_amount': desired_amount,
        }, instance=instance)

    return StockForm({
            'available': available,
            'desired_amount': desired_amount,
        })

def save_product(request, product_form, stock_form):
    product = product_form.save(commit=False)
    product.belongs_to = request.user
    stock = stock_form.save(commit=False)
    product.stock = stock
    stock.save()
    product.save()

def get_total_sell_value(products):
    total_value_for_sale = 0
    for product in products:
        total_value_for_sale += (product.price * product.stock.available)
    
    return total_value_for_sale

def get_average_profit(products):
    total_profit = 0

    for product in products:
        total_profit += product.profit

    if len(products) != 0:
        average_profit = total_profit / len(products)
    else:
        average_profit = 0
    
    return round(average_profit, 2)