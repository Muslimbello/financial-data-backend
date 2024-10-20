# serializers/stock_serializers.py
from rest_framework import serializers
from ..models import StockData


class StockDataSerializer(serializers.ModelSerializer):
    daily_change = serializers.SerializerMethodField()

    class Meta:
        model = StockData
        fields = [
            "symbol",
            "date",
            "open_price",
            "close_price",
            "high_price",
            "low_price",
            "volume",
            "daily_change",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_daily_change(self, obj):
        return obj.get_daily_change()


class StockDataBulkCreateSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=10)
    days = serializers.IntegerField(min_value=1, max_value=730, default=730)
