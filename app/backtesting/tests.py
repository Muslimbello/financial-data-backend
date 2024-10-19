# from django.test import TestCase
# from django.urls import reverse
# from fetch_stock.models import StockData
# from datetime import datetime, timedelta


# class BacktestTest(TestCase):
#     def test_backtest_strategy(self):
#         # Parameters for backtesting
#         initial_investment = 10000
#         buy_threshold = 50  # Buy when price is below the 50-day moving average
#         sell_threshold = 200  # Sell when price is above the 200-day moving average

#         # Run the backtest using the parameters
#         response = self.client.get(
#             reverse("run_backtest_view", args=["AAPL"]),
#             {
#                 "initial_investment": initial_investment,
#                 "buy_threshold": buy_threshold,
#                 "sell_threshold": sell_threshold,
#             },
#         )

#         # Validate the response
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("final_value", response.json())
#         self.assertIn("total_return", response.json())
#         self.assertIn("trades_executed", response.json())
#         self.assertIn("max_drawdown", response.json())

#         # Debugging: Print response to understand final values
#         json_response = response.json()
#         print(f"Final Value: {json_response['final_value']}, Expected: 10500")
#         print(f"Total Return: {json_response['total_return']}")
#         print(f"Trades Executed: {json_response['trades_executed']}")
#         print(f"Max Drawdown: {json_response['max_drawdown']}")

#         # Further validate outputs
#         self.assertEqual(
#             json_response["final_value"], 10500
#         )  # Example expected final value
#         self.assertEqual(
#             json_response["total_return"], 1500
#         )  # Example expected total return
#         self.assertEqual(
#             json_response["trades_executed"], 5
#         )  # Example expected trades executed
#         self.assertEqual(
#             json_response["max_drawdown"], 200
#         )  # Example expected max drawdown
