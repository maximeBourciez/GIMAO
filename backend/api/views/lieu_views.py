from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Prefetch
from gimao.models import Lieu, Equipement
from api.serializers import LieuSerializer, LieuHierarchySerializer

class LieuViewSet(viewsets.ModelViewSet):
    """
    CRUD pour les lieux. Précharge parents, enfants et équipements liés pour optimiser les requêtes.
    """
    queryset = Lieu.objects.all()
    serializer_class = LieuSerializer

    def get_queryset(self):
        # On select_related le parent et prefetch les enfants + équipements (to_attr pour accès côté objet)
        return Lieu.objects.select_related('lieuParent').prefetch_related(
            'lieu_set',
            Prefetch(
                'equipement_set',
                queryset=Equipement.objects.select_related('modeleEquipement'),
                to_attr='equipements'
            )
        )

@api_view(['GET'])
def get_lieux_hierarchy(request):
    """
    Retourne les lieux de premier niveau avec leurs enfants (utilisé par LieuxExplorer).
    """
    top_level_lieux = Lieu.objects.filter(lieuParent__isnull=True).prefetch_related('lieu_set')
    serializer = LieuHierarchySerializer(top_level_lieux, many=True, context={'request': request})
    return Response(serializer.data)
