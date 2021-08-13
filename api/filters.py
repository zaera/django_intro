import django_filters
from django_filters import rest_framework as filters
from currency_app.models import Rate


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = {
            'sale': ('lt', 'lte', 'gt', 'gte', 'exact'),
            'buy': ('lt', 'lte', 'gt', 'gte', 'exact'),
            'moneytype': ('in',)
        }
