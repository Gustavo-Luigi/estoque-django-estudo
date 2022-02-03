from django.db.models.query_utils import Q
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from commons.utils import get_pagination
from products.utils import search_products
from transaction.models import Cart
from transaction.utils import finish_purchase, finish_sale, generate_purchase_cart_form, generate_sale_cart_form, get_average_ticket, get_carts_total_value, get_last_month_carts, get_last_month_transactions, get_sold_products_from_carts, get_top_seller, get_total_transaction_value, remove_from_purchase_cart, remove_from_sale_cart, save_purchase_to_cart, save_sale_to_cart, sum_carts_product_quantity


# Create your views here.
@login_required(login_url='login')
def sales_index(request):
    sales = get_last_month_transactions(request, is_sale=True)
    carts = get_last_month_carts(request, is_sale=True)

    sold_products = get_sold_products_from_carts(carts)
    top_seller = get_top_seller(sold_products)
    total_value = get_total_transaction_value(sales)
    total_sales = sales.count()
    average_ticket = get_average_ticket(total_sales, total_value)

    context = {
        'total_sales': total_sales,
        'total_value': total_value,
        'top_seller': top_seller,
        'total_sold': len(sold_products),
        'average_ticket': round(average_ticket, 2)
    }
    return render(request, 'transaction/sales-index.html', context)


@login_required(login_url='login')
def sell(request):
    url = 'transaction/product-list.html'

    products = search_products(request)
    selected_page, page_range = get_pagination(request, products, 10)

    context = {'products': selected_page,
               'page_range': page_range, 'is_sale': True}

    if request.method == 'POST':
        form = generate_sale_cart_form(request, url, context)

        if form.is_valid():
            save_sale_to_cart(request, form)
        else:
            messages.error(
                request, 'Algo deu errado, verifique os dados preenchidos!')

    return render(request, url, context)


@login_required(login_url='login')
def sale_cart(request):
    url = 'transaction/cart.html'
    carts = Cart.objects.all().filter(Q(belongs_to=request.user)
                                      & Q(active=True) & Q(is_sale=True))

    total_value = get_carts_total_value(carts)

    if request.method == 'POST':
        is_canceling_product = request.POST.get('cancel_product', False)

        if is_canceling_product:
            remove_from_sale_cart(request)
            return redirect('sale-cart')
        elif request.POST['finish-sale']:
            finish_sale(request, carts)
            return redirect('sell')

    context = {'carts': carts, 'total_value': total_value, 'is_sale': True}
    return render(request, url, context)


@login_required(login_url='login')
def purchases_index(request):
    purchases = get_last_month_transactions(request, is_sale=False)
    carts = get_last_month_carts(request, is_sale=False)

    total_value = get_total_transaction_value(purchases)
    sold_products = sum_carts_product_quantity(carts)

    total_sales = purchases.count()

    context = {
        'total_sales': total_sales,
        'total_value': total_value,
        'total_sold': sold_products,
    }
    return render(request, 'transaction/purchases-index.html', context)


@login_required(login_url='login')
def buy(request):
    url = 'transaction/product-list.html'
    is_for_sale = False

    products = search_products(request)
    selected_page, page_range = get_pagination(request, products, 10)

    context = {'products': selected_page,
               'page_range': page_range,
               'is_for_sale': is_for_sale}

    if request.method == 'POST':
        form = generate_purchase_cart_form(request, url, context)

        if form.is_valid():
            save_purchase_to_cart(request, form)
        else:
            messages.error(
                request, 'Algo deu errado, verifique os dados preenchidos!')

    return render(request, url, context)


@login_required(login_url='login')
def buy_cart(request):
    url = 'transaction/cart.html'
    carts = Cart.objects.all().filter(Q(belongs_to=request.user)
                                      & Q(active=True) & Q(is_sale=False))

    total_value = get_carts_total_value(carts)

    if request.method == 'POST':
        is_canceling_product = request.POST.get('cancel_product', False)

        if is_canceling_product:
            remove_from_purchase_cart(request)
            return redirect('buy-cart')
        elif request.POST['finish-sale']:
            finish_purchase(request, carts)
            return redirect('buy')

    context = {'carts': carts, 'total_value': total_value}
    return render(request, url, context)
