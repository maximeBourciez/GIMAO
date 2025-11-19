from rest_framework import viewsets
from rest_framework.response import Response
from bonTravail.models import Intervention, DocumentIntervention
from bonTravail.api.serializers import (
    InterventionSerializer,
    DocumentInterventionSerializer,
    InterventionAfficherSerializer
)


class InterventionViewSet(viewsets.ModelViewSet):
    """ViewSet de base pour les opérations CRUD sur les interventions"""
    queryset = Intervention.objects.all()
    serializer_class = InterventionSerializer


class DocumentInterventionViewSet(viewsets.ModelViewSet):
    """ViewSet de base pour les opérations CRUD sur les documents d'intervention"""
    queryset = DocumentIntervention.objects.all()
    serializer_class = DocumentInterventionSerializer


class InterventionAfficherViewSet(viewsets.ModelViewSet):
    """ViewSet pour l'affichage détaillé des interventions avec relations"""
    queryset = Intervention.objects.all()
    serializer_class = InterventionAfficherSerializer

    def get_queryset(self):
        return Intervention.objects.select_related(
            'defaillance__equipement',
            'createurIntervention',
            'responsable'
        ).prefetch_related(
            'documentintervention_set'
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
