from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from commons.utils import get_pagination
from products.forms import CategoryForm, ProductForm
from products.models import Category, Product
from products.utils import generate_product_form, generate_stock_form, get_average_profit, get_total_sell_value, save_product
from stock.forms import StockForm

# Create your views here.


@login_required(login_url='login')
def index(request):
    products_for_sale = Product.objects.all().filter(
        Q(belongs_to=request.user) & Q(is_for_sale=True))
    utility_count = Product.objects.all().filter(
        Q(belongs_to=request.user) & Q(is_for_sale=False)).count()

    total_value_for_sale = get_total_sell_value(products_for_sale)
    average_profit = get_average_profit(products_for_sale)

    context = {
        'for_sale_count': products_for_sale.count(),
        'utility_count': utility_count,
        'total_value_for_sale': total_value_for_sale,
        'average_profit': average_profit
    }

    return render(request, 'products/index.html', context)


@login_required(login_url='login')
def insert_product(request):
    url = 'products/insert-product.html'
    undefined_category, created = Category.objects.get_or_create(
        name='Indefinido')
    categories = Category.objects.all().filter(
        Q(belongs_to=request.user) | Q(belongs_to=None))

    if request.method == 'POST':
        product_form = generate_product_form(request)
        stock_form = generate_stock_form(request)

        if product_form.is_valid() and stock_form.is_valid:
            save_product(request, product_form, stock_form)
            return redirect('products')
        else:
            context = {
                'productForm': product_form,
                'stockForm': stock_form,
                'categories': categories
            }
            return render(request, url, context)

    product_form = ProductForm()
    stock_form = StockForm()
    context = {
        'productForm': product_form,
        'stockForm': stock_form,
        'categories': categories
    }
    return render(request, url, context)


@login_required(login_url='login')
def edit_product(request, pk):
    url = 'products/edit-product.html'

    try:
        product_to_edit = Product.objects.get(id=pk)
    except:
        messages.error(request, 'Produto inválido')

    if product_to_edit.belongs_to != request.user:
        return redirect('insert-product')

    categories = Category.objects.all().filter(
        Q(belongs_to=request.user) | Q(belongs_to=None))

    if request.method == 'POST':
        productForm = generate_product_form(request, product_to_edit)
        stockForm = generate_stock_form(request, product_to_edit.stock)

        if productForm.is_valid() and stockForm.is_valid:
            productForm.save()
            stockForm.save()
            return redirect('products')
        else:
            context = {
                'productForm': productForm,
                'stockForm': stockForm,
                'categories': categories
            }
            return render(request, url, context)

    productForm = ProductForm(instance=product_to_edit)
    stockForm = StockForm(instance=product_to_edit.stock)

    context = {
        'productForm': productForm,
        'stockForm': stockForm,
        'categories': categories,
    }
    return render(request, url, context)


@login_required(login_url='login')
def insert_category(request):
    url = 'products/insert-category.html'

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            category.belongs_to = request.user
            category.save()
            return redirect('products')
        else:
            context = {'form': form}
            return render(request, url, context)

    form = CategoryForm()
    context = {'form': form}
    return render(request, url, context)


@login_required(login_url='login')
def edit_category(request, pk):
    url = 'products/edit-category.html'
    category_to_edit = Category.objects.get(id=pk)

    if category_to_edit.belongs_to != request.user:
        return redirect('insert-category')

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category_to_edit)
        apply_to_all = request.POST.get('apply_to_all', False)

        if form.is_valid():
            category = form.save(commit=False)

            if apply_to_all:
                products = Product.objects.all().filter(category=category)
                for product in products:
                    product.price = category.default_price
                    product.cost = category.default_cost
                    product.save()

            category.save()
            return redirect('products')
        else:
            context = {'form': form}
            return render(request, url, context)

    form = CategoryForm(instance=category_to_edit)
    context = {'form': form}
    return render(request, url, context)


@login_required(login_url='login')
def product_list(request):
    products = Product.objects.all().filter(
        belongs_to=request.user).order_by('name')
    selected_page, page_range = get_pagination(request, products, 10)

    context = {
        'products': selected_page,
        'page_range': page_range
    }
    return render(request, 'products/product-list.html', context)


@login_required(login_url='login')
def utility_list(request):
    products = Product.objects.all().filter(
        Q(belongs_to=request.user) & Q(is_for_sale=False)).order_by('name')

    selected_page, page_range = get_pagination(request, products, 10)

    context = {
        'products': selected_page,
        'page_range': page_range
    }
    return render(request, 'products/utility-list.html', context)


@login_required(login_url='login')
def categories(request):
    category_list = Category.objects.all().filter(belongs_to=request.user)
    selected_page, page_range = get_pagination(request, category_list, 10)

    context = {'category_list': selected_page, 'page_range': page_range}
    return render(request, 'products/category-list.html', context)
