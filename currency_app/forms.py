from django import forms
from currency_app.models import Bank, Rate, ContactUs


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = (
            'name',
            'url',
        )


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = (
            'moneytype',
            'sale',
            'buy',
            'source',
        )


class ContactUsCreateForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = (
            'email_from',
            'subject',
            'message',
        )

    #                               Do when any View is called anywhere
    # def save(self, commit =True):
    #     print('here\n'*10)
    #     return super().save(commit)
