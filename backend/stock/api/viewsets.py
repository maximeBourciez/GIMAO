from rest_framework import viewsets
from stock.models import Consommable, StockConsommable, EstCompatible
from stock.api.serializers import (
    ConsommableSerializer,
    StockConsommableSerializer,
    EstCompatibleSerializer
)


class ConsommableViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des consommables"""
    queryset = Consommable.objects.all()
    serializer_class = ConsommableSerializer


class StockConsommableViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des stocks de consommables"""
    queryset = StockConsommable.objects.all()
    serializer_class = StockConsommableSerializer


class EstCompatibleViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion de la compatibilité consommable-modèle"""
    queryset = EstCompatible.objects.all()
    serializer_class = EstCompatibleSerializer
