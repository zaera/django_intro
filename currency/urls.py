from django.conf.urls import url

import currency.settings
from currency_app.views import index_page
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index_page, name='index'),
    path('currency/', include('currency_app.urls')),
    path('accounts/', include('accounts.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    url('^', include('django.contrib.auth.urls')),
    path('api/v1/', include('api.v1.urls')),
    # path('api/rates/', RateList.as_view()),
    # path('api/rates/<int:pk>', RateDetails.as_view()),
    # path('api/banks/', BankList.as_view()),
]

if currency.settings.DEBUG:
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)), )
