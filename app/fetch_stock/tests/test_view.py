# tests/test_views.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from ..models import StockData


class StockDataViewSetTest(APITestCase):
    def setUp(self):
        self.url = reverse("stockdata-fetch-stock-data")

    @patch("fetch_data.services.alpha_vantage.AlphaVantageService.get_daily_stock_data")
    def test_fetch_stock_data_success(self, mock_get_data):
        mock_get_data.return_value = {
            "2024-01-01": {
                "1. open": "150.00",
                "4. close": "152.00",
                "2. high": "153.00",
                "3. low": "149.00",
                "5. volume": "2000000",
            }
        }

        response = self.client.post(self.url, {"symbol": "AAPL"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(StockData.objects.count(), 1)

    def test_fetch_stock_data_missing_symbol(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
