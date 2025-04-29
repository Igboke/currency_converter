from django.urls import path
from .views import ConvertCurrencyView
#Defining endpoints
urlpatterns =[
    path("v1/convert/", ConvertCurrencyView.as_view(), name='convert_currency'),

]