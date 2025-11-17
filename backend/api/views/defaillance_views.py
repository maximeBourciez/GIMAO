from rest_framework import viewsets
from rest_framework.response import Response
from gimao.models import Defaillance
from api.serializers import DefaillanceAfficherSerializer


class DefaillanceAfficherViewSet(viewsets.ModelViewSet):
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
