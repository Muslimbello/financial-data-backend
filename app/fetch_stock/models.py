from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class StockData(models.Model):
    symbol = models.CharField(max_length=10, db_index=True, help_text="Stock symbol ")
    date = models.DateField(db_index=True, help_text="Date of the stock data")
    open_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    close_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    high_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    low_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    volume = models.BigIntegerField(
        validators=[MinValueValidator(0)], help_text="Volume of shares traded"
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("symbol", "date")
        indexes = [
            models.Index(fields=["symbol", "date"]),
            models.Index(fields=["date"]),
        ]
        ordering = ["-date", "symbol"]

    def __str__(self):
        return f"{self.symbol} - {self.date}"
