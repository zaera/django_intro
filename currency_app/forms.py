from django import forms
from currency_app.models import Bank, ContactUs


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = (
            'name',
            'url',
        )


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = (
            'email_from',
            'subject',
            'message',
        )
