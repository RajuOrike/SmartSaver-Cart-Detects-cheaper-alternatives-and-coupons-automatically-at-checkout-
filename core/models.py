from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=255)
    store = models.CharField(max_length=100)
    price = models.FloatField()
    product_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.store}) - {self.price}"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(default=0)
    discount_amount = models.FloatField(default=0.0)
    min_purchase = models.FloatField(default=0.0)
    valid_till = models.DateField()
    applicable_store = models.CharField(max_length=100, blank=True)  # empty means all stores
    active = models.BooleanField(default=True)

    def is_valid(self, cart_total, store_name=None):
        from django.utils import timezone
        today = timezone.now().date()
        if not self.active: 
            return False
        if self.valid_till < today:
            return False
        if cart_total < self.min_purchase:
            return False
        if self.applicable_store and store_name and self.applicable_store.lower() != store_name.lower():
            return False
        return True

    def apply_discount(self, amount):
        # percent takes precedence if >0
        if self.discount_percent:
            return amount * (100 - self.discount_percent) / 100.0
        return max(0.0, amount - self.discount_amount)

    def __str__(self):
        return f"{self.code} (Active: {self.active})"
