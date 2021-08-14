from rest_framework import serializers
from currency_app.models import Rate, Bank, ContactUs
from currency_app.tasks import send_mail_in_bckg


class BankInnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = (
            'id',
            'name',
        )


class RateSerializer(serializers.ModelSerializer):
    bank_obj = BankInnerSerializer(read_only=True, source='bank')

    class Meta:
        model = Rate
        fields = (
            'id',
            'sale',
            'buy',
            'bank',
            'created',
            'moneytype',
            'bank_obj',
        )
        extra_kwargs = {
            'security_question': {'write_only': True},
        }


class RateReverseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'sale',
            'buy',
        )


class BankSerializer(serializers.ModelSerializer):
    rate_set = RateReverseSerializer(many=True)
    # rate_set is automaticaly generetaed name for foreign key. because there was no related name set up

    class Meta:
        model = Bank
        fields = (
            'id',
            'name',
            'code_name',
            'url',
            'origin_url',
            'rate_set',
        )


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

    def create(self, validated_data):
        send_mail_in_bckg.delay(validated_data['subject'], validated_data['email_from'])
        return ContactUs.objects.create(**validated_data)

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
