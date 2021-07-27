from django.conf.urls import url
from django.urls import path, re_path
from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('profile/', views.Profile.as_view(), name='profile'),
    path('password/', views.ChangePassword.as_view(), name='change-password'),
    # path('signup/', views.SignUp.as_view(), name='signup'),
    # path('activate/account/<uuid:activation_key>/', views.Activate.as_view(), name='activate'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate')
]
