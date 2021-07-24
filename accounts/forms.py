import uuid

from django import forms
from accounts.models import User


class SignUpForm(forms.ModelForm):

    password1 = forms.CharField()
    passwordd = forms.CharField()

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.username = str(uuid.uuid4())
        instance.is_active = False

        if commit:
            instance.save()

        return instance

