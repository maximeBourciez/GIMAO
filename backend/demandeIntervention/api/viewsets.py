from rest_framework import viewsets
from rest_framework.response import Response
from demandeIntervention.models import Defaillance, DocumentDefaillance
from demandeIntervention.api.serializers import (
    DefaillanceSerializer,
    DocumentDefaillanceSerializer,
    DefaillanceAfficherSerializer
)


class DefaillanceViewSet(viewsets.ModelViewSet):
    """ViewSet de base pour les opérations CRUD sur les défaillances"""
    queryset = Defaillance.objects.all()
    serializer_class = DefaillanceSerializer


class DocumentDefaillanceViewSet(viewsets.ModelViewSet):
    """ViewSet de base pour les opérations CRUD sur les documents de défaillance"""
    queryset = DocumentDefaillance.objects.all()
    serializer_class = DocumentDefaillanceSerializer


class DefaillanceAfficherViewSet(viewsets.ModelViewSet):
    """ViewSet pour l'affichage détaillé des défaillances avec relations"""
    queryset = Defaillance.objects.all()
    serializer_class = DefaillanceAfficherSerializer

    def get_queryset(self):
        return Defaillance.objects.select_related(
            'equipement',
            'utilisateur'
        ).prefetch_related(
            'documentdefaillance_set',
            'intervention_set'
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
