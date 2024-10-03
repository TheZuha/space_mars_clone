from django.contrib.auth.models import AbstractUser
from django.db import models

from olma_market.models import Shops


# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=13, unique=True, null=True, blank=True)

    def set_password(self, raw_password):
        super().set_password(raw_password)

    def __str__(self):
        return self.username


class Orders(models.Model):
    order_id = models.BigIntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.BigIntegerField()
    payment_type = models.CharField(max_length=50)
    date_of_delivery = models.DateTimeField(null=True, blank=True)
    shop_id = models.ForeignKey('olma_market.Shops', on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)