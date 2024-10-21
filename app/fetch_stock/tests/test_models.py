# tests/test_models.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from ..models import StockData
from datetime import date


class StockDataModelTest(TestCase):
    def setUp(self):
        self.stock_data = StockData.objects.create(
            symbol="AAPL",
            date=date(2024, 1, 1),
            open_price=Decimal("150.00"),
            close_price=Decimal("152.00"),
            high_price=Decimal("153.00"),
            low_price=Decimal("149.00"),
            volume=2000000,
        )
