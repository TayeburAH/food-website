from django.db import models
from django.conf import settings
from food.models import Product
from account.models import Customer
from .utils import unique_order_id_generator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal
from datetime import datetime

# Create your models here.


STATUS_CHOICE = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
    ('Processing', 'Processing'),
    ('Pending', 'Pending'),
)


class OrderPlaced(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    # if customer is deleted, his order will not
    # After the first cart is completed,
    # same user can have many Cart
    order_date = models.DateTimeField(null=True)
    # default=datetime.now
    total_quantity = models.PositiveIntegerField(null=True)
    status = models.CharField(max_length=14, choices=STATUS_CHOICE, default='Not confirmed')
    total = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    cancel_reason = models.CharField(max_length=200, null=True, blank=True)
    order_id = models.CharField(max_length=120, blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    cash = models.CharField(null=True, max_length=10)

    def __str__(self):
        return self.customer.first_name

    def name(self):
        return self.customer.first_name + ' ' + self.customer.last_name

    def order_status(self):
        return self.status

    def ordered_date(self):
        return self.order_date

    def save(self, *args, **kwargs):
        self.shipping_cost = Decimal(4.05)
        self.total = sum([i.sub_total for i in self.cartitems_set.all()], self.shipping_cost)
        super(OrderPlaced, self).save(*args, **kwargs)

    @property
    def total_cost(self):
        return self.total


def multiply_universal(item1, item2):
    return round(float(item1) * float(item2), 2)


class CartItems(models.Model):
    orderplaced = models.ForeignKey(OrderPlaced, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=2, null=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    sub_total = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    # Order.objects.get(Q(user= request.user) & Q$(status='Pending')).cartitem_set.all()

    def __str__(self):
        return self.orderplaced.customer.first_name

    def amount(self):
        return self.quantity

    def name_of_food(self):
        return self.product.name

    def price_of_food(self):
        return self.price

    def food_size(self):
        return self.size

    def save(self, *args, **kwargs):
        self.sub_total = multiply_universal(self.price, self.quantity)
        super(CartItems, self).save(*args, **kwargs)


@receiver(pre_save, sender=OrderPlaced)
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
