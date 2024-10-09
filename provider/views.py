from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import *
from .serializers import *
from rest_framework import status
# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class ProviderView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        pass