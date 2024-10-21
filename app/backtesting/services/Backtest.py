import pandas as pd
from fetch_stock.models import StockData


class Backtest:
    def __init__(self, symbol, investment_amount, short_ma_days=50, long_ma_days=200):
        self.symbol = symbol
        self.investment_amount = investment_amount
        self.short_ma_days = short_ma_days
        self.long_ma_days = long_ma_days
        self.stock_data = None

    def fetch_data(self):
        # Fetch stock data from the database
        self.stock_data = StockData.objects.filter(symbol=self.symbol).order_by("date")

        if not self.stock_data.exists():
            raise ValueError(f"No stock data available for symbol {self.symbol}")

    def calculate_moving_averages(self):
        # Convert stock data to a pandas DataFrame
        df = pd.DataFrame(list(self.stock_data.values("date", "close_price")))
        df.set_index("date", inplace=True)

        # Calculate the short and long moving averages
        df["SMA_short"] = df["close_price"].rolling(window=self.short_ma_days).mean()
        df["SMA_long"] = df["close_price"].rolling(window=self.long_ma_days).mean()

        return df

    def run_backtest(self):
        # Fetch stock data
        self.fetch_data()

        # Calculate moving averages
        df = self.calculate_moving_averages()

        # Placeholder for backtest logic
        # Here you would add the strategy logic, including buy/sell signals, and calculate performance metrics

        results = {
            "symbol": self.symbol,
            "investment_amount": self.investment_amount,
            "strategy_results": "Backtest results placeholder",
        }
        return results


def run_backtest(symbol, investment_amount, short_ma_days=50, long_ma_days=200):
    backtest = Backtest(symbol, investment_amount, short_ma_days, long_ma_days)
    return backtest
