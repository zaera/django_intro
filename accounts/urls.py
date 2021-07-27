from django.urls import path
from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('profile/', views.Profile.as_view(), name='profile'),
    path('password/', views.ChangePassword.as_view(), name='change-password'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    # path('activate/account/<uuid:activation_key>/', views.Activate.as_view(), name='activate'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate')
]
