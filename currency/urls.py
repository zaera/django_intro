from currency_app.views import index_page

from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', index_page, name='index'),
    path('currency/', include('currency_app.urls')),
]
