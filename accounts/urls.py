from django.urls import path
from accounts.views import Profile, ChangePassword, SignUp


app_name = 'accounts'

urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('password/', ChangePassword.as_view(), name='change-password'),
    path('signup/', SignUp.as_view(), name='signup'),
]
