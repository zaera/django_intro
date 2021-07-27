from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView
from accounts.models import User
from accounts.forms import SignUpForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from accounts.tokens import account_activation_token
from django.contrib.auth import login
from django.shortcuts import redirect


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


class SignUp(CreateView):
    model = User
    template_name = 'signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        messages.info(self.request, 'Please check email to confirm your registration')
        return super().form_valid(form)

    success_url = reverse_lazy('index')


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

    # Alternative way(not preferable)
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(pk=self.request.user.pk)
    #     return queryset

    def get_object(self, queryset=None):
        return self.request.user


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Account is confirmed')
            return redirect('index')
        else:
            messages.success(request, 'Account already confirmed')
            return redirect('index')
    else:
        messages.warning(request, 'The confirmation link was invalid')
        return redirect('index')
