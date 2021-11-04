from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Merchants(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    city_id = models.IntegerField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Create your models here.
class Products(models.Model):
    merchant = models.ForeignKey(Merchants, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(default=None, null=True)
    price = models.BigIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Create your models here.
class Payments(models.Model):
    method = models.CharField(max_length=50)
    payment_identifier = models.CharField(max_length=50)  # For eg. VA Number
    sub_total = models.PositiveBigIntegerField(default=0)
    tax = models.PositiveBigIntegerField(default=0)
    TYPE_CHOICE = (
        (0, 'waiting'),
        (1, 'paid'),
        (2, 'expire'),
    )
    status = models.IntegerField(default=0, choices=TYPE_CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    paid_at = models.DateTimeField(default=None, null=True)


# Create your models here.
class Orders(models.Model):
    payment = models.ForeignKey(Payments, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Create your models here.
class OrderProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    total_price = models.PositiveBigIntegerField(default=0)
