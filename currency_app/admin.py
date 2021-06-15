from django.contrib import admin
from .models import Rate, Bank, ContactUs
# Register your models here.


class RateAdmin(admin.ModelAdmin):
    list_display = ('moneytype', 'sale', 'buy', 'created', 'source')


admin.site.register(Rate, RateAdmin)


class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


admin.site.register(Bank, BankAdmin)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('email_from', 'subject', 'message', 'created')


admin.site.register(ContactUs, ContactUsAdmin)
