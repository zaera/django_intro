import uuid
from django import forms
from accounts.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
import os
from currency_app.tasks import send_reg_mail


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password')
    password2 = forms.CharField(label='Retype password')

    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2',
        )
        labels = {
            'email': mark_safe('&nbsp;&nbsp;E-mail'),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['password1'] != cleaned_data['password2']:
                #self.add_error('password1', 'Passwords do not match.')
                raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # instance.username = self.cleaned_data['email']
        instance.username = str(uuid.uuid4())
        instance.is_active = False
        # instance.password = self.cleaned_data['password1']
        # instance.set_password(self.cleaned_data['password1'])

        if commit:
            instance.save()

        body = f"""
        Activate Your Account
        {os.environ.get('DOMAIN')}

        """
        send_reg_mail.delay(body, instance.email)
        return instance

    #{reverse('account:activate-account', args=(instance.username,))}