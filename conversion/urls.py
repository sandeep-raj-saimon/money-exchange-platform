from django.urls import path
from django.contrib import admin
from .admin import CurrencyConverterAdmin
from currency.models import *
from .views import *

currency_converter_admin = CurrencyConverterAdmin(Currency, admin.site)

urlpatterns = [
    path('currency/', currency_converter_admin.admin_site.admin_view(currency_converter_admin.convert_currency), name='currency_converter'),
    path('', ConvertAmountView.as_view())
]