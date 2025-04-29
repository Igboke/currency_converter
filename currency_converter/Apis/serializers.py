from rest_framework import serializers

class CurrencyConversionSerializer(serializers.Serializer):
    """
    Serializer for Currency Conversion
    """
    base_currency = serializers.CharField(max_length=10,required=True)
    converted_currency = serializers.CharField(max_length=10,required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2,required=True)

    def validate(self, data):
        if data.get('base_currency') == data.get('converted_currency'):
            raise serializers.ValidationError("Base and converted currencies cannot be the same.")
        return data