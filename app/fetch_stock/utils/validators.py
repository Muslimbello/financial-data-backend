from typing import List
import re
from django.core.exceptions import ValidationError


def validate_stock_symbol(symbol: str) -> bool:
    """
    Validate stock symbol format
    """
    pattern = r"^[A-Z]{1,5}$"
    if not re.match(pattern, symbol):
        raise ValidationError(
            f"Invalid stock symbol format: {symbol}. "
            "Symbol should be 1-5 uppercase letters."
        )
    return True
