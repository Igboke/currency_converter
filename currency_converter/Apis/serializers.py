from rest_framework import serializers

class CurrencyConversionSerializer(serializers.Serializer):
    """
    Serializer for Currency Conversion
    """
    base_currency = serializers.CharField(max_length=10,required=True)
    converted_currency = serializers.CharField(max_length=10,required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2,required=True)
    date = serializers.DateField(required=False, help_text="Date in YYYY-MM-DD format. Defaults to latest if not provided.")

    def validate(self, data):
        if data.get("base_currency") == data.get("converted_currency"):
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

