from rest_framework import serializers
import datetime
from decimal import Decimal

class CurrencyItemSerializer(serializers.Serializer):
    """
    Serializer to represent a single currency item in the output list.
    """
    code = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True) 

class CurrencyConversionSerializer(serializers.Serializer):
    """
    Serializer for Currency Conversion
    """
    base_currency = serializers.CharField(max_length=6,required=True)
    converted_currency = serializers.CharField(max_length=6,required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2,required=False,allow_null=True)
    date = serializers.DateField(required=False, help_text="Date in YYYY-MM-DD format.",allow_null=True)

    def validate_base_currency(self, value):
        """
        convert to lowercase.
        """
        if value:
            return value.lower()
        return value
    
    def validate_converted_currency(self, value):
        """
        convert to lowercase.
        """
        if value:
            return value.lower()
        return value

    def validate(self, data):
        validated_data = super().validate(data)
        if "date" not in validated_data or validated_data["date"] is None:
             # If date is missing or None, set it to today's date
             validated_data["date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        if validated_data["base_currency"] == validated_data["converted_currency"]:
            raise serializers.ValidationError("Base and converted currencies cannot be the same.")
        if "amount" not in validated_data:
            validated_data["amount"] = Decimal('1')
        if validated_data["amount"] is not None and validated_data["amount"] <= 0:
             raise serializers.ValidationError("Amount must be greater than zero.")
        return validated_data
    
class CurrencyConversionOutputSerializer(serializers.Serializer):
    """
    Serializer to format the output data for the conversion endpoint.
    """
    base_currency = serializers.CharField(read_only=True)
    converted_currency = serializers.CharField(read_only=True)
    original_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    exchange_rate = serializers.DecimalField(max_digits=20, decimal_places=10, read_only=True)
    calculated_amount = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
    date = serializers.DateField(read_only=True) 

