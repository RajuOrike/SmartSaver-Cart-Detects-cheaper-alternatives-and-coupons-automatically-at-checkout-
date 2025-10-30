from django.contrib import admin
from .models import Product, Coupon

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'price', 'created_at')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'discount_amount', 'min_purchase', 'valid_till', 'applicable_store', 'active')
