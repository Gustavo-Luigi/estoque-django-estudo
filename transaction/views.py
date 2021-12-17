from typing import Counter
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone


from products.models import Product
from transaction.models import Cart, SiteTransaction
from transaction.utils import get_last_month_transactions
from .forms import CartForm


# Create your views here.
def sales_index(request):
    today = timezone.now()
    last_mont = (today - timezone.timedelta(days=30))

    sales = get_last_month_transactions(request, is_sale=True)
    carts = Cart.objects.all().filter(belongs_to=request.user, closed_at__lte=today,
                                      closed_at__gte=last_mont, is_sale=True)

    total_value = 0
    sold_products = []

    for cart in carts:
        for product in range(cart.quantity):
            sold_products.append(cart.product.name)

    if len(sold_products) > 0:
        top_seller = Counter(sold_products).most_common()[0][0]
    else:
        top_seller = ''
        

    for sale in sales:
        total_value += sale.total_value

    total_sales = sales.count()

    if total_sales > 0:
        average_ticket = total_value / total_sales
    else:
        average_ticket = 0

    context = {
        'total_sales': total_sales,
        'total_value': total_value,
        'top_seller': top_seller,
        'total_sold': len(sold_products),
        'average_ticket': round(average_ticket, 2)
    }
    return render(request, 'transaction/sales-index.html', context)


def sell(request):
    url = 'transaction/product-list.html'

    if request.GET.get('search') is None:
        products = Product.objects.all().filter(
            belongs_to=request.user, is_for_sale=True).order_by('name')
    else:
        products = Product.objects.all().filter(Q(belongs_to=request.user) & Q(
            name__icontains=request.GET['search']) & Q(is_for_sale=True)).order_by('name')

    paginated_products = Paginator(products, 10)

    if request.GET.get('pagina') is None:
        requested_page = 1
    else:
        requested_page = request.GET.get('pagina')

    selected_page = paginated_products.get_page(requested_page)
    page_range = range(1, paginated_products.num_pages + 1)

    context = {'products': selected_page,
               'page_range': page_range, 'is_sale': True}

    if request.method == 'POST':
        selected_product = Product.objects.get(
            id=request.POST['selected_product'])

        if not request.POST['product_quantity'].strip(' '):
            quantity = 1
        else:
            quantity = float(request.POST['product_quantity'])

        if float(quantity) < 1:
            messages.error(
                request, 'Quantidade inválida, produto não adicionado ao carrinho!')
            return render(request, url, context)
        elif float(quantity) > selected_product.stock.available:
            messages.error(
                request, 'Quantidade indisponível em estoque, produto não adicionado ao carrinho!')
            return render(request, url, context)

        form = CartForm({
            'product': request.POST['selected_product'],
            'quantity': quantity
        })

        if form.is_valid():
            cart = form.save(commit=False)
            cart.belongs_to = request.user
            cart.total_price = cart.product.price * cart.quantity
            cart.save()
            selected_product.stock.available -= quantity
            selected_product.stock.save()
            messages.success(
                request, f'{cart.product.name} ({cart.quantity}) foi adicionado ao carrinho com sucesso!')
        else:
            messages.error(
                request, 'Algo deu errado, verifique os dados preenchidos!')

    return render(request, url, context)


def sale_cart(request):
    url = 'transaction/cart.html'
    carts = Cart.objects.all().filter(Q(belongs_to=request.user)
                                      & Q(active=True) & Q(is_sale=True))

    total_value = 0

    for cart in carts:
        total_value += cart.total_price

    if request.method == 'POST':
        is_canceling_product = request.POST.get('cancel_product', False)

        if is_canceling_product:
            cart_to_remove = Cart.objects.get(
                id=request.POST['cancel_product'])
            cart_to_remove.product.stock.available += cart_to_remove.quantity
            cart_to_remove.product.stock.save()
            cart_to_remove.delete()
            messages.success(
                request, f'{cart_to_remove.product.name} removido com sucesso!')
            return redirect('sale-cart')
        elif request.POST['finish-sale']:
            transaction = SiteTransaction.objects.create(
                total_value=total_value,
                is_sale=True,
                belongs_to=request.user
            )

            for cart in carts:
                cart.cart_from = transaction
                cart.active = False
                cart.closed_at = timezone.now()
                cart.save()

            messages.success(request, 'Venda realizada com sucesso!')
            return redirect('sell')

    context = {'carts': carts, 'total_value': total_value, 'is_sale': True}
    return render(request, url, context)


def purchases_index(request):
    today = timezone.now()
    last_mont = (today - timezone.timedelta(days=30))

    purchases = SiteTransaction.objects.all().filter(closed_at__lte=today,
                                                 closed_at__gte=last_mont, is_sale=False)
    carts = Cart.objects.all().filter(closed_at__lte=today,
                                      closed_at__gte=last_mont, is_sale=False)

    total_value = 0
    sold_products = 0

    for cart in carts:
        sold_products += cart.quantity

    for purchase in purchases:
        total_value += purchase.total_value

    total_sales = purchases.count()

    context = {
        'total_sales': total_sales,
        'total_value': total_value,
        'total_sold': sold_products,
    }
    return render(request, 'transaction/purchases-index.html', context)


def buy(request):
    url = 'transaction/product-list.html'
    is_for_sale = False

    if request.GET.get('search') is None:
        products = Product.objects.all().filter(
            belongs_to=request.user).order_by('name')
    else:
        products = Product.objects.all().filter(Q(belongs_to=request.user) & Q(
            name__icontains=request.GET['search'])).order_by('name')

    paginated_products = Paginator(products, 10)

    if request.GET.get('pagina') is None:
        requested_page = 1
    else:
        requested_page = request.GET.get('pagina')

    selected_page = paginated_products.get_page(requested_page)
    page_range = range(1, paginated_products.num_pages + 1)

    context = {'products': selected_page, 'page_range': page_range, 'is_for_sale': is_for_sale}

    if request.method == 'POST':
        selected_product = Product.objects.get(
            id=request.POST['selected_product'])

        if not request.POST['product_quantity'].strip(' '):
            quantity = 1
        else:
            quantity = float(request.POST['product_quantity'])

        if float(quantity) < 1:
            messages.error(
                request, 'Quantidade inválida, produto não adicionado ao carrinho!')
            return render(request, url, context)

        form = CartForm({
            'product': request.POST['selected_product'],
            'quantity': quantity
        })

        if form.is_valid():
            cart = form.save(commit=False)
            cart.belongs_to = request.user
            cart.total_price = cart.product.cost * cart.quantity
            cart.is_sale = False
            cart.save()
            messages.success(
                request, f'{cart.product.name} ({cart.quantity}) foi adicionado ao carrinho com sucesso!')
        else:
            messages.error(
                request, 'Algo deu errado, verifique os dados preenchidos!')

    return render(request, url, context)


def buy_cart(request):
    url = 'transaction/cart.html'
    carts = Cart.objects.all().filter(Q(belongs_to=request.user)
                                      & Q(active=True) & Q(is_sale=False))

    total_value = 0

    for cart in carts:
        total_value += cart.total_price

    if request.method == 'POST':
        is_canceling_product = request.POST.get('cancel_product', False)

        if is_canceling_product:
            cart_to_remove = Cart.objects.get(id=request.POST['cancel_product'])
            cart_to_remove.delete()
            messages.success(
                request, f'{cart_to_remove.product.name} removido com sucesso!')
            return redirect('buy-cart')
        elif request.POST['finish-sale']:
            transaction = SiteTransaction.objects.create(
                total_value=total_value,
                is_sale=False,
                belongs_to=request.user
            )

            for cart in carts:
                product = cart.product
                product.stock.available += cart.quantity
                cart.cart_from = transaction
                cart.active = False
                cart.closed_at = timezone.now()
                product.stock.save()
                cart.save()

            messages.success(request, 'Compra realizada com sucesso!')
            return redirect('buy')

    context = {'carts': carts, 'total_value': total_value}
    return render(request, url, context)
