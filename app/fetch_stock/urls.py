# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockDataViewSet

router = DefaultRouter()
router.register(r"stocks", StockDataViewSet, basename="stockdata")

urlpatterns = [
    path("", include(router.urls)),
]
