from rest_framework import serializers

class CurrencySerializer(serializers.Serializer):
    """
    Serializer for Currency Data
    """
    currency = serializers.CharField(max_length=3,required=True)
    amount = serializers.DecimalField(max_digits=15,decimal_places=2,required=True)
    