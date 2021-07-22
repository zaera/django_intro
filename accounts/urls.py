from django.conf.urls import url
from django.urls import path
from accounts import views
from accounts.views import Profile


app_name = 'accounts'

urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    url(r'^password/$', views.changepassword, name='change-password'),
]
