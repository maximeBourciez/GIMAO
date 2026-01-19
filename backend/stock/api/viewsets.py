from rest_framework import viewsets
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from stock.models import *
from stock.api.serializers import (
    ConsommableSerializer,
    ConsommableDetailSerializer,
    MagasinSerializer,
    MagasinDetailSerializer,
    PorterSurSerializer,
    EstCompatibleSerializer
)


class MagasinViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des magasins avec CRUD complet"""
    queryset = Magasin.objects.all()
    serializer_class = MagasinSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estMobile']
    search_fields = ['nom']
    ordering_fields = ['nom', 'id']
    ordering = ['nom']
    
    def get_serializer_class(self):
        """Utilise le serializer détaillé pour les actions retrieve et list"""
        if self.action in ['retrieve', 'list']:
            return MagasinDetailSerializer
        return MagasinSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Création d'un magasin avec gestion de l'adresse imbriquée"""
        adresse_data = request.data.pop('adresse', None)
        if adresse_data:
            adresse = Adresse.objects.create(**adresse_data)
            request.data['adresse'] = adresse.id
        return super().create(request, *args, **kwargs)


class ConsommableViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des consommables avec CRUD complet et filtrage par magasin"""
    queryset = Consommable.objects.all()
    serializer_class = ConsommableSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['magasin']
    search_fields = ['designation']
    ordering_fields = ['designation', 'id', 'seuilStockFaible']
    ordering = ['designation']
    
    def get_serializer_class(self):
        """Utilise le serializer détaillé pour les actions retrieve et list"""
        if self.action in ['retrieve', 'list']:
            return ConsommableDetailSerializer
        return ConsommableSerializer


class PorterSurViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des fournitures de consommables"""
    queryset = PorterSur.objects.all()
    serializer_class = PorterSurSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['consommable', 'fournisseur', 'fabricant']
    ordering_fields = ['date_reference_prix', 'prix_unitaire']
    ordering = ['-date_reference_prix']


class EstCompatibleViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion de la compatibilité consommable-modèle"""
    queryset = EstCompatible.objects.all()
    serializer_class = EstCompatibleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['consommable', 'modeleEquipement']
