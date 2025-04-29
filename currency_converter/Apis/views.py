from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .serializers import CurrencyConversionSerializer, CurrencyConversionOutputSerializer
from drf_spectacular.utils import extend_schema
from .utils import fetch_exchange_rate, FetchRateError, RateNotFoundError, RateCalculationError

    
class ConvertCurrencyView(APIView):
    @extend_schema(
        request=CurrencyConversionSerializer,
        responses={200: CurrencyConversionOutputSerializer},
        summary="Convert an amount between two currencies (crypto or fiat).",
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
        endpoint_url_two = f"https://{date}.currency-api.pages.dev/{apiVersion}/currencies/{base_currency}.json"


        try:
            rate = fetch_exchange_rate(base_currency, converted_currency, date, endpoint_url)
            
        except (FetchRateError, RateNotFoundError, RateCalculationError) as e:
            # If endpoint one failed, store the error and try endpoint two as a fallback
            
            last_error = e

            try:
                # second Attempt
                rate = fetch_exchange_rate(base_currency, converted_currency, date, endpoint_url_two)
                

            except (FetchRateError, RateNotFoundError, RateCalculationError) as e_two:
                # If endpoint two also failed, store this error
                last_error = e_two 

                return Response(
                    {"error": f"Failed to fetch exchange rate after multiple attempts. Last error: {last_error}"},
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

        try:
            calculated_amount = amount * rate
        except Exception as e:
             return Response(
                 {"error": "Internal error during final calculation"},
                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
             )
        except Exception as e:       
            return Response(
                {"error": "An unexpected internal server error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        
        
        output_data_dict = {
            "base_currency": base_currency,
            "converted_currency": converted_currency,
            "original_amount": amount,
            "date": date, 
            "exchange_rate": rate,
            "calculated_amount": calculated_amount,
        }

        output_serializer = CurrencyConversionOutputSerializer(output_data_dict)

        return Response(output_serializer.data, status=status.HTTP_200_OK)


