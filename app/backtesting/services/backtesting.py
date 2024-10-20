# services/backtesting.py
from ..models import StockData

class SimpleBacktest:
    def __init__(self, symbol, investment_amount):
        self.symbol = symbol
        self.investment = investment_amount
        self.current_money = investment_amount
        self.shares = 0
        self.trades = []

    def calculate_moving_average(self, days):
        # Get stock data ordered by date
        stocks = StockData.objects.filter(symbol=self.symbol).order_by('date')

        # Simple way to calculate moving average
        moving_averages = []
        for i in range(len(stocks) - days + 1):
            prices = stocks[i:i+days].values_list('close_price', flat=True)
            average = sum(prices) / days
            moving_averages.append({
                'date': stocks[i+days-1].date,
                'average': average
            })

        return moving_averages

    def run_backtest(self):
        # Get 50 day and 200 day moving averages
        short_ma = self.calculate_moving_average(50)
        long_ma = self.calculate_moving_average(200)

        # Get all stock prices
        stock_prices = list(StockData.objects.filter(
            symbol=self.symbol
        ).order_by('date').values('date', 'close_price'))

        # Track our trades and money
        for i in range(len(stock_prices)):
            current_price = float(stock_prices[i]['close_price'])

            # Check if we can find moving averages for this date
            if i >= 200:  # We need at least 200 days of data
                # Simple buy rule: price below 50 day MA
                if (current_price < short_ma[i-200]['average'] and
                    self.current_money > 0):
                    # Buy as many shares as we can
                    shares_to_buy = self.current_money // current_price
                    cost = shares_to_buy * current_price
                    self.current_money -= cost
                    self.shares += shares_to_buy

                    self.trades.append({
                        'type': 'BUY',
                        'shares': shares_to_buy,
                        'price': current_price,
                        'date': stock_prices[i]['date']
                    })

                # Simple sell rule: price above 200 day MA
                elif (current_price > long_ma[i-200]['average'] and
                      self.shares > 0):
                    # Sell all shares
                    money_gained = self.shares * current_price
                    self.current_money += money_gained

                    self.trades.append({
                        'type': 'SELL',
                        'shares': self.shares,
                        'price': current_price,
                        'date': stock_prices[i]['date']
                    })
                    self.shares = 0

        # Calculate final value and return
        final_value = self.current_money + (self.shares * current_price)
        total_return = ((final_value - self.investment) / self.investment) * 100

        return {
            'initial_investment': self.investment,
            'final_value': round(final_value, 2),
            'total_return_percent': round(total_return, 2),
            'number_of_trades': len(self.trades),
            'trades': self.trades
        }