from django.db import models

# Create your models here.
class ContactUs(models.Model):
    email_from = models.EmailField(max_length=254)
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=500)
