from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from fetch_stock.models import StockData
from datetime import datetime


class BacktestView(View):
    def get(self, request, symbol):
        # Get parameters from the request, ensuring they are floats
        initial_investment = float(request.GET.get("initial_investment", 10000))
        buy_threshold = int(
            float(request.GET.get("buy_threshold", 50))
        )  # 50-day moving average
        sell_threshold = int(
            float(request.GET.get("sell_threshold", 200))
        )  # 200-day moving average

        # Fetch historical data from the database
        historical_data = StockData.objects.filter(symbol=symbol).order_by("date")
        if not historical_data.exists():
            return JsonResponse(
                {"error": "No historical data found for this symbol."}, status=404
            )

        # Backtesting logic
        total_investment = initial_investment
        shares_owned = 0
        trades_executed = 0

        # Variables to track max drawdown
        peak_value = initial_investment
        max_drawdown = 0

        # Iterate through historical data
        for i in range(len(historical_data)):
            current_price = float(historical_data[i].close_price)  # Convert to float

            # Calculate moving averages
            moving_average_buy = current_price
            moving_average_sell = current_price

            if i >= buy_threshold - 1:
                moving_average_buy = (
                    sum(
                        float(historical_data[j].close_price)  # Convert to float
                        for j in range(i - (buy_threshold - 1), i + 1)
                    )
                    / buy_threshold
                )

            if i >= sell_threshold - 1:
                moving_average_sell = (
                    sum(
                        float(historical_data[j].close_price)  # Convert to float
                        for j in range(i - (sell_threshold - 1), i + 1)
                    )
                    / sell_threshold
                )

            # Buy condition
            if current_price < moving_average_buy and total_investment >= current_price:
                shares_bought = int(
                    total_investment // current_price
                )  # Ensure shares_bought is an int
                shares_owned += shares_bought
                total_investment -= shares_bought * current_price
                trades_executed += 1

            # Sell condition
            elif current_price > moving_average_sell and shares_owned > 0:
                total_investment += shares_owned * current_price
                shares_owned = 0
                trades_executed += 1

            # Calculate current total value
            current_total_value = total_investment + shares_owned * current_price

            # Update peak value and calculate max drawdown
            if current_total_value > peak_value:
                peak_value = current_total_value
            drawdown = peak_value - current_total_value
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        # Calculate final value
        final_value = (
            total_investment + shares_owned * current_price
            if shares_owned > 0
            else total_investment
        )
        total_return = (
            (final_value - initial_investment) / initial_investment * 100
            if initial_investment > 0
            else 0
        )

        # Prepare response
        result = {
            "final_value": final_value,
            "total_return": total_return,
            "trades_executed": trades_executed,
            "max_drawdown": max_drawdown,
        }

        return JsonResponse(result)
