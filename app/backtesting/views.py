from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from .services.Backtest import (
    run_backtest,
)  # Import the service from the services directory


@require_http_methods(["POST"])
def run_backtest_view(request):
    try:
        # Parse JSON body
        data = json.loads(request.body)
        symbol = data.get("symbol")
        investment_amount = data.get("investment_amount")
        short_ma_days = data.get("short_ma_days", 50)  # default to 50 days
        long_ma_days = data.get("long_ma_days", 200)  # default to 200 days

        # Ensure required fields are provided
        if not all([symbol, investment_amount]):
            return JsonResponse(
                {
                    "error": "Missing required parameters: 'symbol' and 'investment_amount'"
                },
                status=400,
            )

        # Call the backtest service
        backtest = run_backtest(symbol, investment_amount, short_ma_days, long_ma_days)
        results = backtest.run_backtest()

        # Return the backtest results as a JSON response
        return JsonResponse(results)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    except Exception as e:
        # Generic exception handler to return error message
        return JsonResponse({"error": str(e)}, status=500)
