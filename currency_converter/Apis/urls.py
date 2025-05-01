from django.urls import path
from .views import ConvertCurrencyView, CurrencyListView#, CurrencyExchangeRateView

#Defining endpoints
urlpatterns =[
    path("v1/convert/", ConvertCurrencyView.as_view(), name='convert_currency'),
    path("v1/currencies/", CurrencyListView.as_view(), name='currency_list'),

]