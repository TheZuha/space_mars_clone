from _ast import Store

from django.db import models
from django.conf import settings



# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    count_sell = models.BigIntegerField()
    avatar = models.ImageField(upload_to='images/')
    banner = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Shops(models.Model):
    WORK_TIMES = (
        ('10:00-20:00', '10:00-20:00'),
        ('09:00-19:00', '09:00-19:00'),
        ('08:00-18:00', '08:00-18:00')
    )
    address = models.CharField(max_length=255, unique=True)
    work_time = models.CharField(max_length=255, choices=WORK_TIMES)
    phone = models.CharField(max_length=255, unique=True)
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address



class Products(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    full_description = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='category')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField()
    aksiya = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    store_name = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='stores')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Products, through='CartItem', related_name='carts')

    def __str__(self):
        return f'{self.product.name} ({self.quantity} ta)'

    def total_price(self):
        return self.product.price * self.quantity

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


