from django.contrib import admin
from .models import Rate, Bank, ContactUs
from rangefilter.filters import DateTimeRangeFilter
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class RateResource(resources.ModelResource):

    class Meta:
        model = Rate


class RateAdmin(ImportExportModelAdmin):
    list_display = ('moneytype', 'sale', 'buy', 'created', 'source')
    list_filter = ('moneytype', ('created', DateTimeRangeFilter), 'source')
    search_fields = ('source', 'moneytype', 'sale', 'buy',)
    resource_class = RateResource


admin.site.register(Rate, RateAdmin)


class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    list_filter = ('name',)
    search_fields = ('name', 'url',)


admin.site.register(Bank, BankAdmin)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('email_from', 'subject', 'message', 'created')
    list_filter = ('created', ('created', DateTimeRangeFilter))
    search_fields = ('message', 'subject')
    readonly_fields = ('email_from', 'subject', 'message', 'created')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(ContactUs, ContactUsAdmin)
