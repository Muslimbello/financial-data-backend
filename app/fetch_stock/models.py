from django.db import models


class StockData(models.Model):
    symbol = models.CharField(max_length=10)  # Stock symbol like AAPL, MSFT, etc.
    date = models.DateField()  # Date for the stock data
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()  # Volume of shares traded

    class Meta:
        unique_together = (
            "symbol",
            "date",
        )  # Ensure no duplicate data for the same stock/date combo

    def __str__(self):
        return f"{self.symbol} on {self.date}"
