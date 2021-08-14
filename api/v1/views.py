# from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAdminUser
from api.v1.throttles import AnonUserRateThrottle
from currency_app.models import Rate, Bank, ContactUs
from api.v1.serializers import RateSerializer, BankSerializer, ContactUsSerializer
from currency_app import choices
from api.v1.filters import RateFilter, ContactUsFilter
from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filters
# class RateList(generics.ListCreateAPIView):
#     queryset = Rate.objects.all()
#     serializer_class = RateSerializer
#     # permission_classes = [IsAdminUser]
#
#
# class RateDetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Rate.objects.all()
#     serializer_class = RateSerializer
#
#
# class BankList(generics.ListCreateAPIView):
#     queryset = Bank.objects.all()
#     serializer_class = BankSerializer


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all().prefetch_related('bank').order_by('-created')
    # pagination_class = RateResultsSetPagination
    serializer_class = RateSerializer
    filterset_class = RateFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    ordering_fields = ['id', 'created', 'moneytype', 'sale', 'buy']
    throttle_classes = [AnonUserRateThrottle]

    # def get_serializer_class(self):
    #     if 'pk' in self.kwargs:
    #         return RateDetailsSerializer
    #     return RateSerializer


class BankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bank.objects.prefetch_related('rate_set').order_by('name')
    serializer_class = BankSerializer
    throttle_classes = [AnonUserRateThrottle]

    # def dispatch(self, *args, **kwargs):
    #     response = super().dispatch(*args, **kwargs)
    #     # For debugging purposes only.
    #     from django.db import connection
    #     print('# of Queries: {}'.format(len(connection.queries)))
    #     return response
    # # def get_serializer_class(self):
    # #     if 'pk' in self.kwargs:
    # #         return BankDetailsSerializer
    # #     return BankSerializer


class RateChoicesView(APIView):
    def get(self, request, format=None): # noqa
        return Response(choices.RATE_TYPE_CHOICES)

    throttle_classes = [AnonUserRateThrottle]


class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    filterset_class = ContactUsFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
    )
    ordering_fields = [
        'email_from',
        'created',
    ]
    search_fields = ['subject', 'message']
    throttle_classes = [AnonUserRateThrottle]
