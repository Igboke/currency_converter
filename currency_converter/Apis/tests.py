from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.response import Response
import datetime

class CurrencyConversionTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("convert_currency")
        self.currency_list_url = reverse("currency_list")
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
        self.missing_amount = {
            "base_currency": "usd",
            "converted_currency": "eur",
            "date": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        self.amount_less_than_zero = {
            "base_currency": "usd",
            "converted_currency": "eur",
            "amount": -100,
            "date": datetime.datetime.now().strftime("%Y-%m-%d")
        }
    def test_valid_conversion(self):
        response = self.client.post(self.url, data=self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("calculated_amount", response.data)
        self.assertIn("exchange_rate", response.data)

    def test_invalid_data(self):
        response = self.client.post(self.url, data=self.invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["base_currency"], [
    "Ensure this field has no more than 6 characters."])
    
    def test_empty_data(self):
        response = self.client.post(self.url,data=self.empty_data,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_missing_date(self):
        response = self.client.post(self.url,data=self.missing_date,format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("calculated_amount", response.data)
        self.assertIn("exchange_rate", response.data)
    
    def test_missing_base_currency(self):
        response = self.client.post(self.url,data=self.missing_base_currency,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn("base_currency",response.data)

    def test_missing_amount(self):
        response = self.client.post(self.url,data=self.missing_amount,format="json")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn("calculated_amount", response.data)
        self.assertIn("exchange_rate", response.data)
        self.assertEqual(response.data["original_amount"], "1.00")

    def test_amount_less_than_zero(self):
        response = self.client.post(self.url,data=self.amount_less_than_zero,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    

    def test_currency_list(self):
        response = self.client.get(self.currency_list_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
        self.assertTrue(
        any(item.get('code') == 'usd' for item in response.data),
        "Response data does not contain an item with code 'usd'"
    )