from celery import shared_task
from .models import CurrencyExchangeRate
from .exchangeRateView import ExchangeRateProvider
from currency.models import Currency
from provider.models import Provider
from datetime import date
import aiohttp
import asyncio
from exchange.utils import save_exchange_rates, fetch_rate, date_range

@shared_task
def fetch_daily_exchange_rates():
    providers = Provider.objects.all()
    for provider in providers:
        currencies = Currency.objects.all()
        exchange_provider = ExchangeRateProvider().get_adapter(provider_name=provider.name)

        for source_currency in currencies:
            for exchanged_currency in currencies:
                if source_currency != exchanged_currency:
                    rate_data = exchange_provider.get_exchange_rate(source_currency.code, exchanged_currency.code, start_date=date.today().strftime('%Y-%m-%d'), end_date=date.today().strftime('%Y-%m-%d'))
                    if rate_data:
                        CurrencyExchangeRate.objects.update_or_create(
                            source_currency=source_currency,
                            exchanged_currency=exchanged_currency,
                            valuation_date=date.today().strftime('%Y-%m-%d'),
                            rate_value=rate_data[date.today().strftime('%Y-%m-%d')][exchanged_currency.code],
                            provider=provider
                        )
                        pass
                    else:
                        print({ "msg": f"exchange rate was not available for source currency {source_currency.code} and exchange currency {exchanged_currency.code}"})

@shared_task
async def load_historical_data(start_date, end_date):
    currencies = ['USD', 'INR']
    async with aiohttp.ClientSession() as session:
        for source_currency in currencies:
            for exchanged_currency in currencies:
                if source_currency != exchanged_currency:

                    rate_data = await fetch_rate(session, source_currency, exchanged_currency, start_date, end_date)
                    if rate_data.get('meta').get('code') == 200:
                        data = rate_data.get("response")
                        await save_exchange_rates(data, source_currency, exchanged_currency)
                    else:
                        print(f"Failed to fetch data: {rate_data.get('error', 'Unknown error')}")