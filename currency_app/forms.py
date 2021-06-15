from django import forms
from currency_app.models import Bank, Rate


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
