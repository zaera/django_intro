from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf import settings
from currency_app.views import (
                                rate_list,
                                rate_edit,
                                rate_delete_single,
                                bank_list,
                                bank_edit,
                                bank_delete,
                                index_page,
                                contact_us_list,
                                contact_us_delete,
                                )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('currency/rate/list/', rate_list),
    path('currency/rate/edit/<int:pk>/<m>/<s>/<b>/<src>/', rate_edit),
    path('currency/rate/delete_single/<int:pk>/', rate_delete_single),
    path('currency/bank/list/', bank_list),
    path('currency/bank/edit/<int:pk>/<npk>/<upk>/', bank_edit),
    path('currency/bank/delete_single/<int:pk>/', bank_delete),
    path('currency/сontact_us/list/', contact_us_list),
    path('currency/сontact_us/delete_single/<int:pk>/', contact_us_delete),
    path('__debug__/', include(debug_toolbar.urls)),
]
