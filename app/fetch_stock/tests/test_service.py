# tests/test_services.py
from django.test import TestCase
from unittest.mock import patch, MagicMock
from ..services.alpha_vantage import AlphaVantageService
from ..services.data_processor import StockDataProcessor
from django.core.cache import cache


class AlphaVantageServiceTest(TestCase):
    def setUp(self):
        self.service = AlphaVantageService()
        cache.clear()

    @patch("requests.get")
    def test_get_daily_stock_data_success(self, mock_get):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Time Series (Daily)": {
                "2024-01-01": {
                    "1. open": "150.00",
                    "4. close": "152.00",
                    "2. high": "153.00",
                    "3. low": "149.00",
                    "5. volume": "2000000",
                }
            }
        }
        mock_get.return_value = mock_response

        data = self.service.get_daily_stock_data("AAPL", days=1)
        self.assertIsNotNone(data)
        self.assertIn("2024-01-01", data)

    @patch("requests.get")
    def test_get_daily_stock_data_failure(self, mock_get):
        mock_get.side_effect = Exception("API Error")
        data = self.service.get_daily_stock_data("AAPL")
        self.assertIsNone(data)
