import json

from rest_framework import serializers
from currency_app.models import Rate, Bank, ContactUs
from currency_app.tasks import send_mail_in_bckg


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'


# class RateDetailsSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Rate
#         fields = (
#             'id',
#             'sale',
#             'buy',
#             'bank',
#             'created',
#             'moneytype',
#         )


class BankSerializer(serializers.ModelSerializer):
    rates_set = serializers.SerializerMethodField('rates')

    def rates(self, obj):
        rate_queryset = Rate.objects.prefetch_related('bank').filter(bank=obj.id)
        rates_set_list = []
        for rate in rate_queryset:
            rates_set_list.append(
                {
                    'id': rate.id,
                    'sale': rate.sale,
                    'buy': rate.buy,
                }
            )
        return rates_set_list

    class Meta:
        model = Bank
        fields = (
            'id',
            'name',
            'code_name',
            'url',
            'origin_url',
            'rates_set',
        )


# class BankDetailsSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Bank
#         fields = (
#             'id',
#             'name',
#             'code_name',
#             'url',
#             'origin_url',
#         )


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

    def create(self, validated_data):
        send_mail_in_bckg.delay(validated_data['subject'],  validated_data['email_from'])
        return ContactUs.objects.create(**validated_data)

