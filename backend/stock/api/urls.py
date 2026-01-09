from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stock.api.viewsets import (
    MagasinViewSet,
    ConsommableViewSet,
    PorterSurViewSet,
    EstCompatibleViewSet,
)

router = DefaultRouter()
router.register(r'magasins', MagasinViewSet, basename='magasin')
router.register(r'consommables', ConsommableViewSet, basename='consommable')
router.register(r'fournitures', PorterSurViewSet, basename='porter-sur')
router.register(r'compatibilites', EstCompatibleViewSet, basename='est-compatible')

urlpatterns = [
    path('', include(router.urls)),
]
