from django.urls import path
from currency_app.views import (
                                Ratelist,
                                rate_edit,
                                rate_delete_single,
                                BankList,
                                BankCreate,
                                BankReadSingle,
                                BankUpdateSingle,
                                BankDeleteSingle,
                                contact_us_list,
                                contact_us_delete,
                                ContactUsCreate,
                                )

app_name = 'currency_app'

urlpatterns = [
    path('rate/list/', Ratelist.as_view(), name='rate-list'),
    path('rate/edit/<int:pk>/<m>/<s>/<b>/<src>/', rate_edit, name='rate-edit'),
    path('rate/delete_single/<int:pk>/', rate_delete_single, name='rate_delete_single'),
    path('bank/list/', BankList.as_view(), name='bank-list'),
    path('bank/create/', BankCreate.as_view(), name='bank-create'),
    path('bank/read_single/<int:pk>/', BankReadSingle.as_view(), name='bank-read-single'),
    path('bank/edit/<int:pk>/', BankUpdateSingle.as_view(), name='bank-update-single'),
    path('bank/delete_single/<int:pk>/', BankDeleteSingle.as_view(), name='bank-delete-single'),
    path('сontact_us/create/', ContactUsCreate.as_view(), name='contact_us_create'),
    path('сontact_us/list/', contact_us_list, name='contact_us_list'),
    path('сontact_us/delete_single/<int:pk>/', contact_us_delete, name='contact_us_delete'),
]
