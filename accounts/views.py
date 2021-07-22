from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy

from django.views.generic import UpdateView
from accounts.models import User


class Profile(UpdateView):
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