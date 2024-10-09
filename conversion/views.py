from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from exchange.models import *
from currency.models import *
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

class ConvertAmountView(APIView):
    def get(self, request):
        source_currency_code = request.GET.get('source_currency')
        target_currency_code = request.GET.get('target_currency')
        amount = request.GET.get('amount')

        if not source_currency_code or not target_currency_code or not amount:
            return Response({"error": "source_currency, target_currency, and amount are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(amount)
        except:
            return Response({"error": "Invalid amount format."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            source_currency = Currency.objects.get(code=source_currency_code)
            target_currency = Currency.objects.get(code=target_currency_code)
        except Currency.DoesNotExist:
            return Response({"error": "Invalid currency code."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            exchange_rate = CurrencyExchangeRate.objects.filter(
                source_currency=source_currency,
                exchanged_currency=target_currency
            ).latest('valuation_date')
        except CurrencyExchangeRate.DoesNotExist:
            return Response({"error": "Exchange rate not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print({ "msg": f"Something went wrong: {e}"})
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        converted_amount = amount * exchange_rate.rate_value

        response_data = {
            "source_currency": source_currency_code,
            "target_currency": target_currency_code,
            "amount": amount,
            "rate": exchange_rate.rate_value,
            "converted_amount": converted_amount,
            "valuation_date": exchange_rate.valuation_date
        }

        return Response(response_data, status=status.HTTP_200_OK)
