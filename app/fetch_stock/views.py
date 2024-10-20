# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .services.alpha_vantage import AlphaVantageService
from .services.data_processor import StockDataProcessor
from .serializers import StockDataSerializer
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
        clear_existing = request.data.get("clear_existing", False)  # New parameter

        if not symbol:
            return Response(
                {"error": "Symbol is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Optionally clear existing data
            if clear_existing:
                StockData.objects.filter(symbol=symbol).delete()

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
            processed_data = processor.process_alpha_vantage_data(symbol, stock_data)

            if not processed_data:
                return Response(
                    {"error": "No data was processed"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Serialize and return the response
            serializer = self.serializer_class(processed_data, many=True)
            return Response({
                "message": f"Successfully processed {len(processed_data)} records",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            logger.error(f"Validation error for symbol {symbol}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error processing symbol {symbol}: {str(e)}")
            return Response(
                {"error": f"Internal server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["delete"])
    def clear_stock_data(self, request):
        """
        Clear all stock data for a given symbol
        """
        symbol = request.query_params.get("symbol")

        if not symbol:
            return Response(
                {"error": "Symbol is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            deleted_count = StockData.objects.filter(symbol=symbol).delete()[0]
            return Response({
                "message": f"Successfully deleted {deleted_count} records for {symbol}"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error clearing data for symbol {symbol}: {str(e)}")
            return Response(
                {"error": f"Internal server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )