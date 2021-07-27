from django import forms
from accounts.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
import os
from currency_app.tasks import send_reg_mail
from django.utils.http import urlsafe_base64_encode
from accounts.tokens import account_activation_token
from django.utils.encoding import force_bytes


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Retype password')
    username = forms.CharField(label='Username')

    class Meta:
        model = User
        fields = (
            'email',
            'username',
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
                raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # instance.username = self.cleaned_data['email']
        # instance.username = str(uuid.uuid4())
        # instance.password = self.cleaned_data['password1']
        instance.username = self.cleaned_data['username']
        instance.is_active = False
        instance.set_password(self.cleaned_data['password1'])

        if commit:
            instance.save()
        body = f"""
        Activate Your Account:
        {os.environ.get('DOMAIN')}{reverse('accounts:activate', args=(
            urlsafe_base64_encode(force_bytes(instance.pk)),
            account_activation_token.make_token(instance)
        ))}
        """
        send_reg_mail.delay(body, instance.email)
        return instance
