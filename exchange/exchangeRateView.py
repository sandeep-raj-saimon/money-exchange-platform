from django.http import JsonResponse
from django.views import View
import requests
from datetime import date
def home(request):
    return JsonResponse({ "message": "exchange service is working fine" })

class CurrencyProviderAdapter:
    def get_exchange_rate(self, source_currency, exchanged_currency, start_date, end_date):
        pass

class CurrencyBeaconAdapter(CurrencyProviderAdapter):
    def get_exchange_name(self):
        return 'Beacon'
    
    def get_exchange_rate(self, source_currency, exchanged_currency, start_date, end_date):
        api_url = 'https://api.currencybeacon.com/v1/timeseries'
        API_KEY = 'ys6STsdWqL69X7hGkE0iJet9HqjY7Gev'

        params = {
            'api_key': API_KEY,
            'base': source_currency,
            'symbols': exchanged_currency,
            'start_date': start_date,
            'end_date': end_date  
        }

        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()

            # we are looking the data for current date or same date
            if (start_date == end_date):
                return_data = {}
                return_data[start_date] = data.get("response")[start_date]
                return return_data
            else:
                exchange_data = {}
                for curr_date, exchange_rates in data.get("response").items():
                    exchange_data[curr_date] = exchange_rates
                return exchange_data
        raise Exception('Something went wrong')

class OpenExchangeRateProviderAdapter(CurrencyProviderAdapter):
    def get_exchange_name(self):
        return 'OpenExchangeRates'
    
    def get_exchange_rate(self, source_currency, exchanged_currency, start_date, end_date):

        # this broker does not allow to change the base currency
        if source_currency != 'USD':
            return
        API_KEY = '29d30d2470e041ddb7e12c51ada8c207'
        api_url = f'https://openexchangerates.org/api/latest.json?app_id={API_KEY}&base={source_currency}&symbols={exchanged_currency}&prettyprint=false&show_alternative=false'

        headers = {
            'accept': 'application/json'
        }
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # we are looking the data for current date or same date
            if (start_date == end_date):
                return_data = {}
                return_data[start_date] = data.get("rates")
                return return_data
            else:
                exchange_data = {}
                for date, exchange_rates in data.get("response").items():
                    exchange_data[date] = exchange_rates
                return exchange_data
        raise Exception('Something went wrong')

class ExchangeRateProvider():
    def __init__(self, requests = {}):
        self.requests = requests
    
    def get_adapter(self, provider_name):
        if provider_name == "currency_beacon":
            return CurrencyBeaconAdapter()
        elif provider_name == "open_exchange_rate":
            return OpenExchangeRateProviderAdapter()
        else:
            raise ValueError("Unsupported provider")

    def get(self):
        source_currency = self.requests.GET.get('source_currency')
        exchanged_currency = self.requests.GET.get('exchanged_currency')
        start_date = self.requests.GET.get('start_date')
        end_date = self.requests.GET.get('end_date')
        provider_name = self.requests.GET.get('provider')

        adapter = self.get_adapter(provider_name)
        try:
            rate_data = adapter.get_exchange_rate(source_currency, exchanged_currency, start_date, end_date)
            print('rate_data is ', rate_data)
            return rate_data
        except Exception as e:
            raise Exception(e)
        
class ExchangeRateView(View):
    def get(self, request, *args, **kwargs):
        try:
            exchanger = ExchangeRateProvider(request)
            rate_data = exchanger.get()
            return JsonResponse(rate_data, status=200)
        except Exception as e:
            return JsonResponse({ 'message': f'Something went wrong ${e}'}, status=500)
