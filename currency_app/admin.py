from django.contrib import admin
from .models import Rate, Bank, ContactUs
# Register your models here.


class RateAdmin(admin.ModelAdmin):
    list_display = ('moneytype', 'sale', 'buy', 'created', 'source')
    list_filter = ('moneytype', 'created', 'source')


admin.site.register(Rate, RateAdmin)


class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    list_filter = ('name',)


admin.site.register(Bank, BankAdmin)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('email_from', 'subject', 'message', 'created')
    list_filter = ('created',)


admin.site.register(ContactUs, ContactUsAdmin)
