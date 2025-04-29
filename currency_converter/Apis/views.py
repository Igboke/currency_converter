from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .serializers import CurrencyConversionSerializer, CurrencyConversionOutputSerializer
from drf_spectacular.utils import extend_schema
import requests 
import json
from decimal import Decimal


class ConvertCurrencyView(APIView):
    @extend_schema(
        request=CurrencyConversionSerializer,
        responses={200: CurrencyConversionOutputSerializer},
        summary="Convert an amount between two currencies",
        description="Fetches the latest exchange rate and calculates the converted amount."
    )
    def post(self, request, *args, **kwargs):
        input_serializer = CurrencyConversionSerializer(data=request.data)

        # Validation
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Data is clean now
        validated_data = input_serializer.validated_data
        base_currency = validated_data["base_currency"]
        converted_currency = validated_data["converted_currency"]
        amount = validated_data["amount"]
        date = validated_data["date"]


        #utilizing endpoint
        apiVersion = "v1"
        # date="latest"
        endpoint_url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/{apiVersion}/currencies/{base_currency}.json"
        endpoint_url_two = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/{apiVersion}/currencies/{base_currency}/{converted_currency}.min.json"

        try:
            response = requests.get(endpoint_url)
            response.raise_for_status()
            data = response.json()
            rate_data = data.get(base_currency, {}) # Get the inner dictionary for the base currency or default to empyt bracket
            rate = rate_data.get(converted_currency) # Get the rate for the converted currency

            if rate is None:
                 # Handle case where the target currency is not found for the base
                 return Response(
                     {"error": f"Could not find exchange rate for {base_currency} to {converted_currency}"},
                     status=status.HTTP_404_NOT_FOUND
                 )

            # Perform the calculation
            try:
                 rate = Decimal(str(rate)) # Convert potentially float/string rate to Decimal
                 calculated_amount = amount * rate
            except Exception as e:
                 print(f"Error converting rate or calculating: {e}")
                 return Response(
                     {"error": "Error during calculation"},
                     status=status.HTTP_500_INTERNAL_SERVER_ERROR
                 )

            # Prepare the output data
            output_data_dict = {
                "base_currency": base_currency,
                "converted_currency": converted_currency,
                "original_amount": amount,
                "exchange_rate": rate,
                "calculated_amount": calculated_amount,
                "date":date
            }

            # Instantiate the output
            output_serializer = CurrencyConversionOutputSerializer(output_data_dict)

            # Return the serialized data in the response
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            print(f"Error calling external API: {e}")
            # Handle errors calling the external API
            return Response(
                {"error": "Failed to fetch exchange rate from external API"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except json.JSONDecodeError as e:
             print(f"JSON Decode Error from external API: {e}")
             return Response(
                {"error": "Invalid response format from external API"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # Catch any other unexpected errors
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


