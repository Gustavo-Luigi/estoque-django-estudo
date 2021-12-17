from django.db import models
from django.db.models.fields import IntegerField


# Create your models here.
class Stock(models.Model):
    available = IntegerField(blank=True)
    desired_amount = IntegerField(blank=True)

    def __str__(self):
        return self.product.name

    def calculate_availability(self):
        if self.desired_amount > 0:
            return (self.available / self.desired_amount) * 100
        
        return 100

    @property
    def availability(self):
        if self.desired_amount > 0:
            availability = self.calculate_availability()
            if availability <= 10:
                return 'low'

            if availability <= 25:
                return 'medium'

            return 'high'