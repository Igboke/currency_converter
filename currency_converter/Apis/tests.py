from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.response import Response
import datetime

class CurrencyConversionTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('convert_currency')
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
    def test_valid_conversion(self):
        response = self.client.post(self.url, data=self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("calculated_amount", response.data)
        self.assertIn("exchange_rate", response.data)

    def test_invalid_data(self):
        response = self.client.post(self.url, data=self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["base_currency"], [
    "Ensure this field has no more than 6 characters."])
