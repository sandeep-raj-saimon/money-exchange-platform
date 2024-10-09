import aiohttp
import asyncio
from asgiref.sync import sync_to_async
from datetime import timedelta, datetime
from exchange.models import CurrencyExchangeRate
from currency.models import Currency
from provider.models import Provider

# Helper function to create a list of dates between start_date and end_date
def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

# Asynchronous function to fetch exchange rate for a specific date
async def fetch_rate(session, source_currency, exchanged_currency, start_date, end_date):
    print('fetch_rate')
    api_url = 'https://api.currencybeacon.com/v1/timeseries'
    API_KEY = 'ys6STsdWqL69X7hGkE0iJet9HqjY7Gev'
    params = {
        'api_key': API_KEY,
        'base': source_currency,
        'symbols': exchanged_currency,
        'start_date': start_date,
        'end_date': end_date  
    }
    print('params is ', params)
    async with session.get(api_url, params=params) as response:
        return await response.json()

# Asynchronous function to load historical exchange rates
async def load_historical_data(source_currency, start_date, end_date):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for date in date_range(start_date, end_date):
            url = f'https://api.example.com/{source_currency}/{date}'
            tasks.append(fetch_rate(session, url))
        
        results = await asyncio.gather(*tasks)
        return results

# Save the fetched data to the database
async def save_exchange_rates(data, source_currency, exchanged_currency):
    source_currency = await sync_to_async(Currency.objects.get)(code=source_currency)
    exchanged_currency = await sync_to_async(Currency.objects.get)(code=exchanged_currency)
    provider = await sync_to_async(Provider.objects.get)(name='currency_beacon')
    # Iterate through the fetched data and save the rates for each day
    for date_str, rates in data.items():
        # print(date_str, rates)
        rate_value = rates.get(exchanged_currency.code)

        if rate_value:
            print('rate_value', date_str, rate_value, source_currency.code, exchanged_currency.code)
            # Save to the database
            await sync_to_async(CurrencyExchangeRate.objects.update_or_create)(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                valuation_date=date_str,
                rate_value=rate_value,
                provider=provider
            )


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)