from rest_framework import serializers
from .models import StockData


class StockDataSerializer(serializers.ModelSerializer):
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
        ]
        read_only_fields = ["created_at", "updated_at"]
