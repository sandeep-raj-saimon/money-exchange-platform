steps to set up
1. install all the requirements using requriements.txt
2. for loading the historical data use the command
**python manage.py load_historical_data 2024-10-01 2024-10-09**
pass the start date and end date.
3. 2 global exchange providers are integrated: CurrencyBeacon and OpenExchangeRate
4. OpenExchange does not have a time-series API for a free subscription, hence only CurrencyBeacon time series api is being used for historical data.
5. A daily cron is set up for 12 midnight to fetch the latest data.
6. Initial Setup steps:
  a. create currency using post api of currency.
  b. get-rates api is useful for getting the exchange rates
