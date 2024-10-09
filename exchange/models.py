
from django.db import models
from currency.models import *
from provider.models import *
# Create your models here.
class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(Currency, related_name='exchanges', on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE) # given the exchange rate, we can find the provider
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)
    class Meta:
        unique_together = ('source_currency', 'exchanged_currency', 'valuation_date', 'provider')


