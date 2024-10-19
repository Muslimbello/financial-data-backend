import requests
from django.conf import settings
from django.http import JsonResponse
from .models import StockData
from datetime import datetime, timedelta


def fetch_stock_data(symbol):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": " PAXV0Y4R8O7VOHFZ",
        "outputsize": "compact",
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (Daily)" not in data:
        return {"error": "Invalid API response"}

    time_series = data["Time Series (Daily)"]

    for date_str, values in time_series.items():
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        # Create or update stock data in the database
        StockData.objects.update_or_create(
            symbol=symbol,
            date=date,
            defaults={
                "open_price": values["1. open"],
                "close_price": values["4. close"],
                "high_price": values["2. high"],
                "low_price": values["3. low"],
                "volume": values["5. volume"],
            },
        )
    return {"status": "success"}


# Sample view to trigger data fetching via API
def fetch_data_view(request, symbol):
    result = fetch_stock_data(symbol)
    return JsonResponse(result)
