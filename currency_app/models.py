from django.db import models
# Create your models here.


class Rate(models.Model):
    moneytype = models.CharField(max_length=5)
    sale = models.DecimalField(max_digits=5, decimal_places=2)
    buy = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=64)


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=254)
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    #                               Do when any class called anywhere

    # def save(self, *args, **kwargs):
    #     print('here\n' * 10)
    #     return super().save(*args, **kwargs)


class Bank(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
