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

# @classmethod
#     def create_random_rate(cls):
#         import random
#         cls.objects.create(
#             currency=random.choice([1, 2]),
#             buy=random.randint(20, 30),
#             sale=random.randint(20, 30),
#             source=random.choice([1, 2]),
#         )
