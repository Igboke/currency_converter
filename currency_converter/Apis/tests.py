from rest_framework import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.response import Response
import datetime

class CurrencyConversionTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('convert_currency')  # Adjust the URL name as needed
        self.valid_data = {
            "base_currency": "usd",
            "converted_currency": "eur",
            "amount": 100,
            "date": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        self.invalid_data = {
            "base_currency": "invalid_currency",
            "converted_currency": "eur",
            "amount": 100,
            "date": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        self.empty_data = {
            "base_currency": "",
            "converted_currency": "",
            "amount": 0,
            "date": ""
        }
        self.missing_date = {
            "base_currency": "usd",
            "converted_currency": "eur",
            "amount": 100,
        }
        self.missing_base_currency = {
            "converted_currency": "eur",
            "amount": 100,
            "date": datetime.datetime.now().strftime("%Y-%m-%d")
        }
    
