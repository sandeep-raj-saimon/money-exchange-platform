from django.contrib import admin
from django.urls import path
from .exchangeRateView import *

urlpatterns = [
    path("", view=home),
    path("get-rates/", view=ExchangeRateView.as_view()),
]
