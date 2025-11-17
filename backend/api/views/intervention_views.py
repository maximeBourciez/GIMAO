from rest_framework import viewsets
from rest_framework.response import Response
from gimao.models import Intervention
from api.serializers import InterventionAfficherSerializer


class InterventionAfficherViewSet(viewsets.ModelViewSet):
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
