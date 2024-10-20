# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.backtesting import SimpleBacktest
from rest_framework import status

@api_view(['POST'])
def run_backtest(request):
    # Get parameters from request
    symbol = request.data.get('symbol')
    investment = request.data.get('investment')

    # Basic validation
    if not symbol:
        return Response(
            {'error': 'Please provide a stock symbol'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not investment:
        return Response(
            {'error': 'Please provide investment amount'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        investment = float(investment)
        if investment <= 0:
            return Response(
                {'error': 'Investment must be positive'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except ValueError:
        return Response(
            {'error': 'Investment must be a number'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Run backtest
        backtest = SimpleBacktest(symbol, investment)
        results = backtest.run_backtest()

        return Response(results, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Something went wrong: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )