from django.urls import path
from .views import BacktestView

urlpatterns = [
    path(
        "run-backtest/<str:symbol>/", BacktestView.as_view(), name="run_backtest_view"
    ),
]
