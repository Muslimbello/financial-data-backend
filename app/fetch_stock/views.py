# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .services.alpha_vantage import AlphaVantageService
from .services.data_processor import StockDataProcessor
from .serializers.stock_serializers import StockDataSerializer
from .models import StockData
import logging

logger = logging.getLogger(__name__)


class StockDataViewSet(viewsets.ModelViewSet):
    queryset = StockData.objects.all()
    serializer_class = StockDataSerializer
    lookup_field = "symbol"

    @action(detail=False, methods=["post"])
    def fetch_stock_data(self, request):
        """
        Fetch stock data for a given symbol
        """
        symbol = request.data.get("symbol")
        days = request.data.get("days", 730)  # Default to 2 years

        if not symbol:
            return Response(
                {"error": "Symbol is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Fetch data from Alpha Vantage
            alpha_vantage = AlphaVantageService()
            stock_data = alpha_vantage.get_daily_stock_data(symbol, days)

            if not stock_data:
                return Response(
                    {"error": "Failed to fetch stock data"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            # Process and save the data
            processor = StockDataProcessor()
            saved_data = processor.process_alpha_vantage_data(symbol, stock_data)

            # Serialize and return the response
            serializer = self.serializer_class(saved_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            logger.error(f"Validation error for symbol {symbol}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error processing symbol {symbol}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
