import django_filters
from django.forms import DateInput
from currency_app.models import Rate


class RateFilter(django_filters.FilterSet):

    created_gte = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        field_name='created', lookup_expr='date__gte',
    )
    created_lte = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        field_name='created', lookup_expr='date__lte',
    )

    class Meta:
        model = Rate
        fields = {
            'sale': ('exact', 'lte'),
            'buy': ('exact', 'lte'),
        }
