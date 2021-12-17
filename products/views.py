from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


from products.forms import CategoryForm, ProductForm
from products.models import Category, Product
from stock.forms import StockForm

# Create your views here.


def index(request):
    products_for_sale = Product.objects.all().filter(Q(belongs_to=request.user) & Q(is_for_sale=True))
    for_sale_count = products_for_sale.count()
    utility_count = Product.objects.all().filter(Q(belongs_to=request.user) & Q(is_for_sale=False)).count()

    total_value_for_sale = 0
    total_profit_for_sale = 0

    for product in products_for_sale:
        total_value_for_sale += (product.price * product.stock.available)
        total_profit_for_sale += product.profit

    if for_sale_count != 0:
        average_profit = total_profit_for_sale / for_sale_count
    else:
      average_profit = 0

    context = {
        'for_sale_count': for_sale_count,
        'utility_count': utility_count,
        'total_value_for_sale': total_value_for_sale,
        'average_profit': average_profit
    }

    return render(request, 'products/index.html', context)


def insert_product(request):
    url = 'products/insert-product.html'
    undefined_category, created = Category.objects.get_or_create(name='Indefinido')
    categories = Category.objects.all().filter(
        Q(belongs_to=request.user) | Q(belongs_to=None))

    if request.method == 'POST':
        selected_category_form = request.POST.get('category', undefined_category.id)
        # if request.POST['category'] == '':
        #     selected_category = Category.objects.get_or_create('indefinido')
        # else:
        #     selected_category = Category.objects.get(
        #         id=request.POST['category'])
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

        if request.POST['available'] == '':
            available = 0
        else:
            available = request.POST['available']

        if request.POST['desired_amount'] == '':
            desired_amount = 0
        else:
            desired_amount = request.POST['desired_amount']

        is_for_sale = request.POST.get('is_for_sale', False)

        productForm = ProductForm({
            'name': request.POST['name'],
            'price': price,
            'cost': cost,
            'category': request.POST['category'],
            'is_for_sale': is_for_sale,
        })

        stockForm = StockForm({
            'available': available,
            'desired_amount': desired_amount,
        })

        if productForm.is_valid() and stockForm.is_valid:
            product = productForm.save(commit=False)
            product.belongs_to = request.user
            stock = stockForm.save(commit=False)
            product.stock = stock
            stock.save()
            product.save()
            return redirect('products')
        else:
            context = {
                'productForm': productForm,
                'stockForm': stockForm,
                'categories': categories
            }
            return render(request, url, context)

    productForm = ProductForm()
    stockForm = StockForm()
    context = {
        'productForm': productForm,
        'stockForm': stockForm,
        'categories': categories
    }
    return render(request, url, context)


def edit_product(request, pk):
    url = 'products/edit-product.html'

    try:
        product_to_edit = Product.objects.get(id=pk)
        if product_to_edit.belongs_to != request.user:
            raise
    except:
        messages.error(request, 'Produto inválido')

    if product_to_edit.belongs_to != request.user:
        return redirect('insert-product')

    categories = Category.objects.all().filter(
        Q(belongs_to=request.user) | Q(belongs_to=None))

    if request.method == 'POST':
        if request.POST['category'] == '':
            selected_category = Category.objects.get(id=1)
        else:
            selected_category = Category.objects.get(
                id=request.POST['category'])

        if request.POST['price'] == '':
            price = selected_category.default_price
        else:
            price = request.POST['price']

        if request.POST['cost'] == '':
            cost = selected_category.default_cost
        else:
            cost = request.POST['cost']

        if request.POST['available'] == '':
            available = 0
        else:
            available = request.POST['available']

        if request.POST['desired_amount'] == '':
            desired_amount = 0
        else:
            desired_amount = request.POST['desired_amount']

        is_for_sale = request.POST.get('is_for_sale', False)

        productForm = ProductForm({
            'id': pk,
            'name': request.POST['name'],
            'price': price,
            'cost': cost,
            'category': request.POST['category'],
            'is_for_sale': is_for_sale
        },
            instance=product_to_edit)

        stockForm = StockForm({
            'available': available,
            'desired_amount': desired_amount,
        }, instance=product_to_edit.stock)

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


def product_list(request):
    products = Product.objects.all().filter(belongs_to=request.user)
    paginated_products = Paginator(products, 10)

    if request.GET.get('pagina') is None:
        requested_page = 1
    else:
        requested_page = request.GET.get('pagina')

    selected_page = paginated_products.get_page(requested_page)
    page_range = range(1, paginated_products.num_pages + 1)

    context = {
        'products': selected_page,
        'page_range': page_range
    }
    return render(request, 'products/product-list.html', context)


def utility_list(request):
    products = Product.objects.all().filter(
        Q(belongs_to=request.user) & Q(is_for_sale=False))
    paginated_products = Paginator(products, 10)

    if request.GET.get('pagina') is None:
        requested_page = 1
    else:
        requested_page = request.GET.get('pagina')

    selected_page = paginated_products.get_page(requested_page)
    page_range = range(1, paginated_products.num_pages + 1)

    context = {
        'products': selected_page,
        'page_range': page_range
    }
    return render(request, 'products/utility-list.html', context)


def categories(request):
    category_list = Category.objects.all().filter(belongs_to=request.user)
    paginated_categories = Paginator(category_list, 10)

    if request.GET.get('pagina') is None:
        requested_page = 1
    else:
        requested_page = request.GET.get('pagina')

    selected_page = paginated_categories.get_page(requested_page)
    page_range = range(1, paginated_categories.num_pages + 1)

    context = {'category_list': selected_page, 'page_range': page_range}
    return render(request, 'products/category-list.html', context)
