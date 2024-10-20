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

    def test_stock_data_creation(self):
        self.assertEqual(self.stock_data.symbol, "AAPL")
        self.assertEqual(self.stock_data.get_daily_change(), Decimal("1.33"))

    def test_invalid_price_validation(self):
        with self.assertRaises(ValidationError):
            StockData.objects.create(
                symbol="AAPL",
                date=date(2024, 1, 2),
                open_price=Decimal("-1.00"),
                close_price=Decimal("152.00"),
                high_price=Decimal("153.00"),
                low_price=Decimal("149.00"),
                volume=2000000,
            )
