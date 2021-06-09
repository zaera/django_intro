from django import forms
from currency_app.models import Bank


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = (
            'name',
            'url',
        )
