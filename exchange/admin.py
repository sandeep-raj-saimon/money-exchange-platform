from django.contrib import admin
from .models import *
# Register your models here.

class CurrencyExchangeRaterAdmin(admin.ModelAdmin):
    list_display = ('source_currency', 'exchanged_currency', 'provider', 'valuation_date', 'rate_value')

admin.site.register(CurrencyExchangeRate, CurrencyExchangeRaterAdmin)