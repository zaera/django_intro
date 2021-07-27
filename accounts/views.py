import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, CreateView, RedirectView
from accounts.models import User
from accounts.forms import SignUpForm
# from annoying.functions import get_object_or_None
# from django.contrib import messages
from currency_app.tasks import send_reg_mail
from django.utils.encoding import force_text
# from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


# class Activate(RedirectView):
#     pattern_name = 'index'
#
#     def get_redirect_url(self, *args, **kwargs):
#         activation_key = kwargs.pop('activation_key')
#         # messages.warning(self.request,'Your account is already activated.')
#         user = get_object_or_None(
#             User.objects.only('is_active'), username=activation_key)
#         if user:
#             if user.is_active:
#                 messages.warning(
#                     self.request, 'Your account is already activated.')
#             else:
#                 messages.info(
#                     self.request, 'Thanks for activating your account.')
#                 user.is_active = True
#                 user.username = user.email
#                 user.save(update_fields=('is_active', 'username', ))
#
#         response = super().get_redirect_url(*args, **kwargs)
#         return response


# class SignUp(CreateView):
#     model = User
#     template_name = 'signup.html'
#     form_class = SignUpForm
#
#     def form_valid(self, form):
#         messages.warning(self.request, 'Check for the email with activation link.')
#         return super().form_valid(form)
#
#     success_url = reverse_lazy('index')


class ChangePassword(PasswordChangeView):
    queryset = User.objects.all()
    template_name = 'change_password.html'
    success_url = reverse_lazy('index')
    fields = (
        'password',
    )

    def get_object(self, queryset=None):
        return self.request.user


class Profile(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    template_name = 'profile.html'
    success_url = reverse_lazy('index')
    fields = (
        'first_name',
        'last_name',
    )

    # Alterbative way(not preferable)
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(pk=self.request.user.pk)
    #     return queryset

    def get_object(self, queryset=None):
        return self.request.user


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            message = render_to_string('account_activation_sent.html', {
                'user': user.username,
                'domain': os.environ.get('DOMAIN'),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_reg_mail.delay(message, user.email)
            messages.info(request, 'Please check email to confirm your registration')
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, template_name='account_activation_sent.html')


def activate(request, uidb64, token):

    print(urlsafe_base64_decode(uidb64))
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Account is confirmed')
        return redirect('index')
    else:
        messages.warning(request, 'The confirmation link was invalid')
        return redirect('index')
