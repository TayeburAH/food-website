from django.contrib import admin
from .models import *


# Register your models here.
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'order_status', 'ordered_date']


admin.site.register(OrderPlaced, OrderPlacedAdmin)




@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name_of_food', 'amount', 'food_size', 'price_of_food']
