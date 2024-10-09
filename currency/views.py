from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import *
from .serializers import *
from rest_framework import status
# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class CurrencyView(View):
    def get(self, request):
        symbol = request.GET.get("symbol")
        code = request.GET.get("code")
        name = request.GET.get("name")
        id = request.GET.get("id")
        filter_params = {}
        if symbol:
            filter_params['symbol'] = symbol
        if code:
            filter_params['code'] = code
        if name:
            filter_params['name__icontains'] = name
        if id:
            filter_params['id'] = id

        currencies = Currency.objects.filter(**filter_params) if filter_params else Currency.objects.all()

        if len(currencies) == 0:
            return JsonResponse({ "message": "there are no currencies in the system"})
        
        serializer = CurrencySerializer(currencies, many=True)
        return JsonResponse({ "data": serializer.data })

    def post(self, request):
        data = request.data
        serializer = CurrencySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Currency created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        return JsonResponse({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        id = request.GET.get("id")
        try:
            currency = Currency.objects.get(id=id)
        except Currency.DoesNotExist:
            return JsonResponse({"message": "Currency not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        serializer = CurrencySerializer(currency, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Currency updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        return JsonResponse({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        id = request.GET.get("id")
        try:
            currency = Currency.objects.get(id=id)
        except Currency.DoesNotExist:
            return JsonResponse({"message": "Currency not found"}, status=status.HTTP_404_NOT_FOUND)

        currency.delete()

        return JsonResponse({"message": "Currency deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
