from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'product_size', 'product_price']
