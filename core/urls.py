from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # search & coupons
    path('search/', views.search_product, name='search_product'),
    path("apply-coupon-single/", views.apply_coupon_single, name="apply_coupon_single"),
    #path('apply-coupon/', views.apply_coupon, name='apply_coupon'),

    # ✅ Add this line:
    path('search/', views.search_product, name='search'),
    path('checkout/', views.checkout_simulate, name='checkout_simulate'),
]
