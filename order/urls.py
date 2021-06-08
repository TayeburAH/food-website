from django.urls import path, reverse
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart_operation/', views.cart_operation, name='cart_operation'),
    # path('minus_cart/', views.minus_cart, name='minus_cart'),
    # path('remove_cart/', views.remove_cart, name='remove_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_tracker/', views.order_tracker, name='order_tracker'),

]
