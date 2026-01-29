from rest_framework import viewsets
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
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
    queryset = Consommable.objects.all().prefetch_related('stocks', 'fournitures', 'stocks__magasin')
    serializer_class = ConsommableSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['magasins']
    search_fields = ['designation']
    ordering_fields = ['designation', 'id', 'seuilStockFaible']
    ordering = ['designation']
    
    def get_serializer_class(self):
        """Utilise le serializer détaillé pour les actions retrieve et list"""
        if self.action in ['retrieve', 'list']:
            return ConsommableDetailSerializer
        return ConsommableSerializer

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def transfer_stock(self, request, pk=None):
        """Transférer du stock d'un magasin vers d'autres"""
        consommable = self.get_object()
        source_magasin_id = request.data.get('from_magasin')
        transfers = request.data.get('transfers', []) # list of {to_magasin: id, quantite: int}

        if not source_magasin_id or not transfers:
            return Response({"error": "Données incomplètes"}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier stock source
        try:
            source_stock = Stocker.objects.get(consommable=consommable, magasin_id=source_magasin_id)
        except Stocker.DoesNotExist:
             return Response({"error": "Stock source introuvable"}, status=status.HTTP_404_NOT_FOUND)

        total_transfer = sum(t.get('quantite', 0) for t in transfers)
        
        if source_stock.quantite < total_transfer:
             return Response(
                 {"error": f"Stock insuffisant (Disponible: {source_stock.quantite}, Demandé: {total_transfer})"},
                 status=status.HTTP_400_BAD_REQUEST
             )

        # Effectuer le transfert
        source_stock.quantite -= total_transfer
        source_stock.save()

        for transfer in transfers:
            to_magasin_id = transfer.get('to_magasin')
            quantite = transfer.get('quantite')
            
            if quantite > 0:
                dest_stock, created = Stocker.objects.get_or_create(
                    consommable=consommable,
                    magasin_id=to_magasin_id,
                    defaults={'quantite': 0}
                )
                dest_stock.quantite += quantite
                dest_stock.save()

        return Response({"status": "Transfert effectué"}, status=status.HTTP_200_OK)


class PorterSurViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des fournitures de consommables"""
    queryset = PorterSur.objects.all()
    serializer_class = PorterSurSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['consommable', 'fournisseur', 'fabricant']
    ordering_fields = ['date_reference_prix', 'prix_unitaire']
    ordering = ['-date_reference_prix']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Créer un achat et distribuer le stock si demandé"""
        distribution_data = request.data.pop('distribution', [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        purchase = serializer.save()

        if distribution_data:
            total_distributed = sum(item.get('quantite', 0) for item in distribution_data)
            if total_distributed != purchase.quantite:
                # Rollback handled by transaction.atomic if we raise exception
                # But here we just want to return strict error before proceeding?
                # Actually, raising exception acts as rollback.
                raise serializers.ValidationError({
                    "distribution": f"La quantité distribuée ({total_distributed}) ne correspond pas à la quantité achetée ({purchase.quantite})."
                })

            for item in distribution_data:
                magasin_id = item.get('magasin')
                quantite = item.get('quantite')
                if quantite > 0:
                    stock, created = Stocker.objects.get_or_create(
                        consommable=purchase.consommable,
                        magasin_id=magasin_id,
                        defaults={'quantite': 0}
                    )
                    stock.quantite += quantite
                    stock.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EstCompatibleViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion de la compatibilité consommable-modèle"""
    queryset = EstCompatible.objects.all()
    serializer_class = EstCompatibleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['consommable', 'modeleEquipement']
