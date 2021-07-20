from django.db import models
from currency_app import choices


class Bank(models.Model):
    name = models.CharField(max_length=64)
    code_name = models.CharField(max_length=64, unique=True)
    url = models.URLField()
    origin_url = models.URLField()


class Rate(models.Model):
    moneytype = models.PositiveSmallIntegerField(choices=choices.RATE_TYPE_CHOICES)
    sale = models.DecimalField(max_digits=5, decimal_places=2)
    buy = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Rate id: {self.id}'


class ContactUs(models.Model):
    email_from = models.EmailField(max_length=254)
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)


class Analytics(models.Model):
    path = models.CharField(max_length=255)
    counter = models.PositiveBigIntegerField()
    request_method = models.PositiveSmallIntegerField(choices=choices.REQUEST_METHOD_CHOICES)
    status_code = models.CharField(max_length=3)

    class Meta:
        unique_together = [
            ['path', 'request_method']
        ]
