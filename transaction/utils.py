from django.utils import timezone
from transaction.models import Cart, SiteTransaction


def get_today_and_last_month():
    today = timezone.now()
    last_month = (today - timezone.timedelta(days=30))
    return today, last_month


def get_last_month_transactions(request, is_sale=True):
    today, last_month = get_today_and_last_month()

    fetched_transactions = SiteTransaction.objects.all().filter(belongs_to=request.user,
        closed_at__lte=today, closed_at__gte=last_month, is_sale=is_sale)
    
    return fetched_transactions


def get_last_month_carts(request, is_sale=True):
    today, last_month = get_today_and_last_month
    return Cart.objects.all().filter(belongs_to=request.user, closed_at__lte=today, closed_at__gte=last_month, is_sale=is_sale)
