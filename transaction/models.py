from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import BooleanField, DateTimeField, DecimalField, IntegerField
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from django.utils import timezone


from products.models import Product
# Create your models here.

class SiteTransaction(models.Model):
    closed_at = DateTimeField(default=timezone.now, db_index=True)
    total_value = DecimalField(decimal_places=2, max_digits=8, auto_created=True)
    is_sale = BooleanField(default=True, auto_created=True)
    belongs_to = ForeignKey(User, on_delete=CASCADE)

 
class Cart(models.Model):
    product = ForeignKey(Product, on_delete=SET_NULL, null=True)
    quantity = IntegerField()
    discount = DecimalField(decimal_places=2, max_digits=8, default=0, blank=True)
    total_price = DecimalField(decimal_places=2, max_digits=10, default=0, blank=True)
    active = BooleanField(default=True)
    is_sale = BooleanField(default=True, auto_created=True)
    cart_from = ForeignKey(SiteTransaction, on_delete=CASCADE, null=True, blank=True)
    belongs_to = ForeignKey(User, on_delete=CASCADE)
    closed_at = DateTimeField(null=True, blank=True, db_index=True)


