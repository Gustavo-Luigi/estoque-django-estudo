from typing import Counter
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from products.models import Product
from transaction.forms import CartForm
from transaction.models import Cart, SiteTransaction


def get_today_and_last_month():
    today = timezone.now()
    last_month = (today - timezone.timedelta(days=30))
    return today, last_month


def get_last_month_transactions(request, is_sale=True):
    today, last_month = get_today_and_last_month()

    return SiteTransaction.objects.all().filter(belongs_to=request.user,
                                                closed_at__lte=today, closed_at__gte=last_month, is_sale=is_sale)


def get_last_month_carts(request, is_sale=True):
    today, last_month = get_today_and_last_month()
    return Cart.objects.all().filter(belongs_to=request.user, closed_at__lte=today, closed_at__gte=last_month, is_sale=is_sale)


def get_sold_products_from_carts(carts):
    sold_products = []
    for cart in carts:
        for product in range(cart.quantity):
            sold_products.append(cart.product.name)

    return sold_products


def get_top_seller(sold_products):
    if len(sold_products) > 0:
        top_seller = Counter(sold_products).most_common()[0][0]
    else:
        top_seller = ''

    return top_seller


def get_total_transaction_value(transactions):
    total_value = 0

    for transaction in transactions:
        total_value += transaction.total_value

    return total_value


def get_average_ticket(number_of_transactions, total_transaction_value):
    if number_of_transactions > 0:
        average_ticket = total_transaction_value / number_of_transactions
    else:
        average_ticket = 0
    
    return average_ticket

def generate_sale_cart_form(request, url, context):
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

    return CartForm({
        'product': request.POST['selected_product'],
        'quantity': quantity
    })

def get_carts_total_value(carts):
    total_value = 0

    for cart in carts:
        total_value += cart.total_price
    
    return total_value

def save_sale_to_cart(request, cart_form):
    cart = cart_form.save(commit=False)
    cart.belongs_to = request.user
    cart.total_price = cart.product.price * cart.quantity
    cart.save()
    cart.product.stock.available -= cart.quantity
    cart.product.stock.save()
    messages.success(
                request, f'{cart.product.name} ({cart.quantity}) foi adicionado ao carrinho com sucesso!')

def remove_from_sale_cart(request):
    cart_to_remove = Cart.objects.get(
                id=request.POST['cancel_product'])
    cart_to_remove.product.stock.available += cart_to_remove.quantity
    cart_to_remove.product.stock.save()
    cart_to_remove.delete()
    messages.success(
        request, f'{cart_to_remove.product.name} removido com sucesso!')

def finish_sale(request, carts):
    transaction_value = get_carts_total_value(carts)
    transaction = SiteTransaction.objects.create(
                total_value=transaction_value,
                is_sale=True,
                belongs_to=request.user
            )

    for cart in carts:
        cart.cart_from = transaction
        cart.active = False
        cart.closed_at = timezone.now()
        cart.save()

    messages.success(request, 'Venda realizada com sucesso!')

def sum_carts_product_quantity(carts):
    quantity = 0

    for cart in carts:
        quantity += cart.quantity

def generate_purchase_cart_form(request, url, context):
    if not request.POST['product_quantity'].strip(' '):
            quantity = 1
    else:
            quantity = float(request.POST['product_quantity'])

    if float(quantity) < 1:
        messages.error(
            request, 'Quantidade inválida, produto não adicionado ao carrinho!')
        return render(request, url, context)

    return CartForm({
        'product': request.POST['selected_product'],
        'quantity': quantity
    })

def save_purchase_to_cart(request, purchase_form):
    cart = purchase_form.save(commit=False)
    cart.belongs_to = request.user
    cart.total_price = cart.product.cost * cart.quantity
    cart.is_sale = False
    cart.save()
    messages.success(
        request, f'{cart.product.name} ({cart.quantity}) foi adicionado ao carrinho com sucesso!')

def remove_from_purchase_cart(request):
    cart_to_remove = Cart.objects.get(
                id=request.POST['cancel_product'])
    cart_to_remove.delete()
    messages.success(
        request, f'{cart_to_remove.product.name} removido com sucesso!')

def finish_purchase(request, carts):
    transaction_value = get_carts_total_value(carts)

    transaction = SiteTransaction.objects.create(
            total_value=transaction_value,
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