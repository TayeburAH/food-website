from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


# class Pizza(models.Model):
#     name = models.CharField(max_length=200)
#     price_s = models.DecimalField(max_digits=4, decimal_places=2)
#     price_m = models.DecimalField(max_digits=4, decimal_places=2)
#     price_l = models.DecimalField(max_digits=4, decimal_places=2)
#     pimage = models.URLField()
#
#     def __str__(self):
#         return self.name
#
#
# class Burger(models.Model):
#     name = models.CharField(max_length=200)
#     price_m = models.DecimalField(max_digits=4, decimal_places=2)
#     price_l = models.DecimalField(max_digits=4, decimal_places=2)
#     bimage = models.URLField()
#
#     def __str__(self):
#         return self.name
#
#
# class FrenchFry(models.Model):
#     name = models.CharField(max_length=200)
#     price_s = models.DecimalField(max_digits=4, decimal_places=2)
#     price_m = models.DecimalField(max_digits=4, decimal_places=2)
#     price_l = models.DecimalField(max_digits=4, decimal_places=2)
#     fimage = models.URLField()
#
#     def __str__(self):
#         return self.name
#

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    pimage = models.URLField()

    def __str__(self):
        return self.name


class Info(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=2, null=True)
    price = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return self.product.name

    def product_size(self):
        return self.size

    def product_price(self):
        return self.price

    class Meta:
        verbose_name_plural = 'Info'



