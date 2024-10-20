from ..models import StockData
from datetime import datetime
from django.db import IntegrityError
from typing import Dict, List

class StockDataProcessor:
    def process_alpha_vantage_data(self, symbol: str, data: Dict) -> List[StockData]:
        """
        Process the Alpha Vantage API response and save to database
        Updates existing records or creates new ones
        """
        processed_data = []

        if not data:
            return processed_data

        for date_str, daily_data in data.items():
            date = datetime.strptime(date_str, '%Y-%m-%d').date()

            try:
                # Try to get existing record
                stock_data, created = StockData.objects.update_or_create(
                    symbol=symbol,
                    date=date,
                    defaults={
                        'open_price': float(daily_data['1. open']),
                        'high_price': float(daily_data['2. high']),
                        'low_price': float(daily_data['3. low']),
                        'close_price': float(daily_data['4. close']),
                        'volume': int(daily_data['5. volume'])
                    }
                )
                processed_data.append(stock_data)

            except IntegrityError as e:
                # Log the error but continue processing
                print(f"Error processing data for {symbol} on {date}: {str(e)}")
                continue
            except Exception as e:
                print(f"Unexpected error processing {symbol} on {date}: {str(e)}")
                continue

        return processed_data