# services/alpha_vantage.py
import requests
from typing import Dict, Optional
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from requests.exceptions import RequestException
import logging

logger = logging.getLogger(__name__)


class AlphaVantageService:
    def __init__(self):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = settings.ALPHA_VANTAGE_API_KEY
        self.cache_timeout = 3600  # This is in Seconds

    def get_daily_stock_data(self, symbol: str, days: int = 730) -> Optional[Dict]:
        """
        Fetch daily stock data for a given symbol
        """
        cache_key = f"stock_data_{symbol}_{days}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        try:
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol.upper(),
                "apikey": self.api_key,
                "outputsize": "full",
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "Time Series (Daily)" not in data:
                logger.error(f"Invalid API response for symbol {symbol}: {data}")
                return None

            # Filter for requested date range
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)

            filtered_data = {
                date: values
                for date, values in data["Time Series (Daily)"].items()
                if start_date <= datetime.strptime(date, "%Y-%m-%d").date() <= end_date
            }

            cache.set(cache_key, filtered_data, self.cache_timeout)
            return filtered_data

        except RequestException as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error processing data for {symbol}: {str(e)}")
            return None
