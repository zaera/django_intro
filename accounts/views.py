from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView
from accounts.models import User
from accounts.forms import SignUpForm


class SignUp(CreateView):
    model = User
    template_name = 'signup.html'
    success_url = reverse_lazy('index')
    form_class = SignUpForm


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
