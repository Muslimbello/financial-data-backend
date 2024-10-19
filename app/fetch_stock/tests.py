from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from .models import StockData


class StockDataFetchTest(TestCase):
    @patch("fetch_stock.views.requests.get")  # Mocking API requests
    def test_fetch_stock_data_success(self, mock_get):
        # Mock response from Alpha Vantage API
        mock_response = {
            "Time Series (Daily)": {
                "2024-10-17": {
                    "1. open": "150.00",
                    "4. close": "152.00",
                    "2. high": "153.00",
                    "3. low": "149.00",
                    "5. volume": "2000000",
                },
            }
        }
        mock_get.return_value.json.return_value = mock_response

        # Test fetching stock data
        response = self.client.get(reverse("fetch_data_view", args=["AAPL"]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(StockData.objects.count(), 1)

        # Validate the data saved in the database
        stock = StockData.objects.get(symbol="AAPL")
        self.assertEqual(stock.open_price, 150.00)
        self.assertEqual(stock.close_price, 152.00)
        self.assertEqual(stock.high_price, 153.00)
        self.assertEqual(stock.low_price, 149.00)
        self.assertEqual(stock.volume, 2000000)

    @patch("fetch_stock.views.requests.get")
    def test_fetch_stock_data_failure(self, mock_get):
        mock_get.return_value.json.return_value = {"error": "Invalid API call"}

        response = self.client.get(reverse("fetch_data_view", args=["AAPL"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StockData.objects.count(), 0)  # No data should be saved
