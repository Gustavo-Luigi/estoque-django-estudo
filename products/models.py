from django.db import models
from django.db.models.deletion import CASCADE, SET_DEFAULT, SET_NULL
from django.db.models.fields import BooleanField, CharField, DecimalField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.contrib.auth.models import User

from stock.models import Stock

# Create your models here.
class Category(models.Model):
    name = CharField(max_length=45, unique=True, db_index=True)
    default_price = DecimalField(decimal_places=2, max_digits=8, default=0)
    default_cost = DecimalField(decimal_places=2, max_digits=8, default=0)
    belongs_to = ForeignKey(User, on_delete=CASCADE, auto_created=True, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def profit(self):
        if self.default_price is not None and self.default_cost is not None:
            return self.default_price - self.default_cost
        
        return 0


class Product(models.Model):
    name = CharField(max_length=100, unique=True, db_index=True)
    price = DecimalField(decimal_places=2, max_digits=8, blank=True)
    cost = DecimalField(decimal_places=2, max_digits=8, blank=True)
    stock = OneToOneField(Stock, on_delete=SET_NULL, null=True)
    category = ForeignKey(Category, on_delete=SET_DEFAULT, default=1)
    is_for_sale = BooleanField(default=True)
    belongs_to = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.name

    @property
    def profit(self):
        return self.price - self.cost
