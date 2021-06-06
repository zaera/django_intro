"""currency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from currency_app.views import hello_world, index_page, rate_list,\
    rate_single, rate_delete_single, bank_list, bank_single, bank_delete_single

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('hello_world/', hello_world),
    path('currency/rate/list/', rate_list),
    path('currency/rate/single/<int:pk>/', rate_single),
    path('currency/rate/delete_single/<int:pk>/', rate_delete_single),
    path('currency/bank/list/', bank_list),
    path('currency/bank/single/<int:pk>/', bank_single),
    path('currency/bank/delete_single/<int:pk>/', bank_delete_single),
]
