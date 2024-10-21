from rest_framework import serializers


class BacktestInputSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=10)
    investment_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    short_ma_days = serializers.IntegerField(default=50, required=False)
    long_ma_days = serializers.IntegerField(default=200, required=False)
