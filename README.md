steps to set up
1. install all the requirements using requriements.txt
 **pip install -r requirements.txt**

2. for loading the historical data use the command
**python manage.py load_historical_data 2024-10-01 2024-10-09**
pass the start date and end date.


3. 2 global exchange providers are integrated: CurrencyBeacon and OpenExchangeRate
4. OpenExchange does not have a time-series API for a free subscription, hence only CurrencyBeacon time series api is being used for historical data.
5. A daily cron is set up for 12 midnight to fetch the latest data.
6. Initial Setup steps:
  a. create currency using post api of currency.
  b. get-rates api is useful for getting the exchange rates


different curls are:

get-rates api
**curl --location 'http://127.0.0.1:8000/exchange/get-rates?source_currency=INR&exchanged_currency=EUR&start_date=2024-10-01&provider=currency_beacon&end_date=2024-10-10'**


get currency API
**curl --location 'http://127.0.0.1:8000/currency?symbol=Rs&code=INR&id=10'**


post currency API
**curl --location 'http://127.0.0.1:8000/currency/' \
--header 'Content-Type: application/json' \
--data '{
    "code": "GBP",
    "name": "GREAT BRITAIN",
    "symbol": "$"
}'**


put currency API
**curl --location --request PUT 'http://127.0.0.1:8000/currency/?id=2' \
--header 'Content-Type: application/json' \
--data '{
    "id": 2,
    "code": "INR",
    "name": "Indian Rupees",
    "symbol": "Rs"
}'**


delete currency API
**curl --location --request DELETE 'http://127.0.0.1:8000/currency/?id=2'**



convert amount api
**curl --location --request GET 'http://127.0.0.1:8000/convert?source_currency=USD&target_currency=INR&amount=1000' \
--header 'Content-Type: application/json' \
--data '{
    "code": "USD",
    "name": "US Dollar",
    "symbol": "$"
}'**


7. admin view has been implemented for converting amounts, you will find the converter view in the currencies tab.
8. admin view has been implemented for providers also, for their, you can create and set priority and mark it as active or in_active.

