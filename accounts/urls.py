from django.urls import path
from accounts.views import Profile


app_name = 'accounts'

urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
]
