from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stock.api.viewsets import (
    ConsommableViewSet,
    StockConsommableViewSet,
    EstCompatibleViewSet,
)

router = DefaultRouter()
router.register(r'consommables', ConsommableViewSet, basename='consommable')
router.register(r'stock-consommables', StockConsommableViewSet, basename='stock-consommable')
router.register(r'est-compatibles', EstCompatibleViewSet, basename='est-compatible')

urlpatterns = [
    path('', include(router.urls)),
]
