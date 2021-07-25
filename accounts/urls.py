from django.urls import path
from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('profile/', views.Profile.as_view(), name='profile'),
    path('password/', views.ChangePassword.as_view(), name='change-password'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]
