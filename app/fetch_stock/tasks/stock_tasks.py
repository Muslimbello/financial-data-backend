from celery import shared_task
from ..services.alpha_vantage import AlphaVantageService
from ..services.data_processor import StockDataProcessor
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=300, rate_limit="2/m")
def fetch_stock_data_task(self, symbol: str, days: int = 730):
    """
    Celery task to fetch and process stock data asynchronously.
    Handles API rate limiting and network errors.
    """
    try:
        service = AlphaVantageService()
        data = service.get_daily_stock_data(symbol, days)

        if not data:
            logger.error(f"Failed to fetch data for symbol {symbol}")
            return None

        processor = StockDataProcessor()
        saved_data = processor.process_alpha_vantage_data(symbol, data)

        return f"Successfully processed {len(saved_data)} records for {symbol}"

    except Exception as exc:
        logger.error(f"Error in fetch_stock_data_task for {symbol}: {str(exc)}")
        raise self.retry(exc=exc)
