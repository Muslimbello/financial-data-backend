# services/data_processor.py
from typing import Dict, List
from datetime import datetime
from decimal import Decimal
from django.db import transaction
from ..models import StockData
import logging

logger = logging.getLogger(__name__)


class StockDataProcessor:
    @staticmethod
    def process_alpha_vantage_data(symbol: str, data: Dict) -> List[StockData]:
        """
        Process raw Alpha Vantage data and create StockData objects
        """
        stock_data_objects = []

        try:
            with transaction.atomic():
                for date_str, values in data.items():
                    date = datetime.strptime(date_str, "%Y-%m-%d").date()

                    stock_data = StockData(
                        symbol=symbol,
                        date=date,
                        open_price=Decimal(values["1. open"]),
                        close_price=Decimal(values["4. close"]),
                        high_price=Decimal(values["2. high"]),
                        low_price=Decimal(values["3. low"]),
                        volume=int(values["5. volume"]),
                    )
                    stock_data_objects.append(stock_data)

                # Bulk create with update on conflict
                StockData.objects.bulk_create(
                    stock_data_objects,
                    update_conflicts=True,
                )

            return stock_data_objects

        except Exception as e:
            logger.error(f"Error processing data for {symbol}: {str(e)}")
            raise
