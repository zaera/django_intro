from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from currency_app.models import Rate, Bank, ContactUs
from api.serializers import RateSerializer, BankSerializer, ContactUsSerializer # BankDetailsSerializer, RateDetailsSerializer,
from currency_app import choices
from api.filters import RateFilter
import django_filters
from django_filters import rest_framework as filters
from api.paginations import RateResultsSetPagination
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
    queryset = Rate.objects.all()
    # pagination_class = RateResultsSetPagination
    serializer_class = RateSerializer
    filterset_class = RateFilter
    filter_backends = (
        filters.DjangoFilterBackend,
    )

    # def get_serializer_class(self):
    #     if 'pk' in self.kwargs:
    #         return RateDetailsSerializer
    #     return RateSerializer


class BankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    filterset_class = RateFilter
    # def get_serializer_class(self):
    #     if 'pk' in self.kwargs:
    #         return BankDetailsSerializer
    #     return BankSerializer


class RateChoicesView(APIView):
    def get(self, request, format=None):
        return Response(choices.RATE_TYPE_CHOICES)


class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
