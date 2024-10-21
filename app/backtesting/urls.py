from django.urls import path
from .views import run_backtest

urlpatterns = [
    path("", run_backtest, name="run_backtest"),
]
