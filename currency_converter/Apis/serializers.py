from rest_framework import serializers
import datetime

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
    base_currency = serializers.CharField(max_length=4,required=True)
    converted_currency = serializers.CharField(max_length=4,required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2,required=True)
    date = serializers.DateField(required=False, help_text="Date in YYYY-MM-DD format.",allow_null=True)

    def validate(self, data):
        validated_data = super().validate(data)
        if "date" not in validated_data or validated_data["date"] is None:
             # If date is missing or None, set it to today's date
             validated_data["date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        if data["base_currency"] == data["converted_currency"]:
            raise serializers.ValidationError("Base and converted currencies cannot be the same.")
        return data
    
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

