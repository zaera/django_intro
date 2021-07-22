from django.contrib import admin
from .models import Rate, Bank, ContactUs, Analytics
from accounts.models import User
from rangefilter.filters import DateTimeRangeFilter
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class UserResource(resources.ModelResource):

    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin):
    list_display = ('username', 'password', 'first_name', 'last_name',)
    resource_class = UserResource


class AnalyticsResource(resources.ModelResource):

    class Meta:
        model = Analytics


class AnalyticsAdmin(ImportExportModelAdmin):
    list_display = ('path', 'counter', 'request_method', 'status_code')
    resource_class = AnalyticsResource


class RateResource(resources.ModelResource):

    class Meta:
        model = Rate


class RateAdmin(ImportExportModelAdmin):
    list_display = ('moneytype', 'sale', 'buy', 'created', 'bank')
    list_filter = ('moneytype', ('created', DateTimeRangeFilter), 'bank')
    search_fields = ('bank', 'moneytype', 'sale', 'buy',)
    resource_class = RateResource


class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'origin_url', 'code_name')
    list_filter = ('name',)
    search_fields = ('name', 'url',)


class ContactUsResource(resources.ModelResource):

    class Meta:
        model = ContactUs


class ContactUsAdmin(ImportExportModelAdmin):
    list_display = ('email_from', 'subject', 'message', 'created')
    list_filter = ('created', ('created', DateTimeRangeFilter))
    search_fields = ('message', 'subject')
    readonly_fields = ('email_from', 'subject', 'message', 'created')
    resource_class = ContactUsResource

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(User, UserAdmin)

admin.site.register(Analytics, AnalyticsAdmin)

admin.site.register(Rate, RateAdmin)

admin.site.register(Bank, BankAdmin)

admin.site.register(ContactUs, ContactUsAdmin)
