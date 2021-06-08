from django.contrib import admin
from django.urls import path
from currency_app.views import (
                                rate_list,
                                rate_single,
                                rate_delete_single,
                                bank_list,
                                bank_single,
                                bank_delete_single,
                                index_page,
                                )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('currency/rate/list/', rate_list),
    path('currency/rate/single/<int:pk>/', rate_single),
    path('currency/rate/delete_single/<int:pk>/', rate_delete_single),
    path('currency/bank/list/', bank_list),
    path('currency/bank/single/<int:pk>/', bank_single),
    path('currency/bank/delete_single/<int:pk>/', bank_delete_single),
]
