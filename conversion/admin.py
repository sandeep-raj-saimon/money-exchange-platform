from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from currency.models import * 
from decimal import Decimal
from exchange.models import *

class CurrencyConverterAdmin(admin.ModelAdmin):
    change_list_template = "admin/currency_converter.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(self.convert_currency), name='currency_converter'),
        ]
        print('custom_urls', custom_urls)
        return custom_urls + urls

    def convert_currency(self, request):
        print("here")
        currencies = Currency.objects.all()
        if request.method == 'POST':
            try:
                source_currency_code = request.POST.get('source_currency')
                target_currency_code = request.POST.get('target_currency')
                amount = request.POST.get('amount')

                source_currency = Currency.objects.get(code=source_currency_code)
                target_currency = Currency.objects.get(code=target_currency_code)

                exchange_rate = CurrencyExchangeRate.objects.filter(
                    source_currency=source_currency,
                    exchanged_currency=target_currency
                ).latest('valuation_date')

                converted_amount = Decimal(amount) * exchange_rate.rate_value

                return render(request, 'admin/currency_converter.html', {
                    'converted_amount': converted_amount,
                    'source_currency': source_currency,
                    'target_currency': target_currency,
                    'amount': amount,
                    'currencies': currencies
                })
            except Exception as e:
                print({ "msg": f"CurrencyConverterAdmin failed due to {e}"})
                return render(request, 'admin/currency_converter.html', {
                    'currencies': currencies,
                    'exception': 'Exchange rate is not present'
                })

        else:
            return render(request, 'admin/currency_converter.html', {
                'currencies': currencies, 
            })

admin.site.register(Currency, CurrencyConverterAdmin)
