import django_filters
from currency_app.models import Rate, ContactUs


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'sale': ('lt', 'lte', 'gt', 'gte', 'iexact'),
            'buy': ('lt', 'lte', 'gt', 'gte', 'iexact'),
            'moneytype': ('in',),
            'created': ('date', 'lte', 'gte'),
        }


class ContactUsFilter(django_filters.FilterSet):

    class Meta:
        model = ContactUs
        fields = {
            'email_from': ('iexact',),
            'created': ('date', 'lte', 'gte'),
        }
