from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Prefetch
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from gimao.models import Equipement, InformationStatut, Defaillance, Consommable, DocumentTechnique, Lieu
from api.serializers import (
    EquipementAvecDernierStatutSerializer,
    EquipementDetailSerializer,
    LieuHierarchySerializer,
    EquipementAffichageSerializer,
)


class EquipementAvecDernierStatutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Equipement.objects.all()
    serializer_class = EquipementAvecDernierStatutSerializer
    lookup_field = 'reference'

    def get_queryset(self):
        return Equipement.objects.prefetch_related(
            Prefetch('informationstatut_set',
                     queryset=InformationStatut.objects.order_by('-dateChangement'),
                     to_attr='statuts')
        )


class EquipementDetailViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.select_related('lieu', 'modeleEquipement')
    serializer_class = EquipementDetailSerializer
    lookup_field = 'reference'

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'createurEquipement',
            'fournisseur',
            Prefetch('informationstatut_set',
                     queryset=InformationStatut.objects.order_by('-dateChangement'),
                     to_attr='statuts')
        )


@api_view(['GET'])
def get_lieux_hierarchy(request):
    top_level_lieux = Lieu.objects.filter(lieuParent__isnull=True).prefetch_related('lieu_set')
    serializer = LieuHierarchySerializer(top_level_lieux, many=True, context={'request': request})
    return Response(serializer.data)


class EquipementAffichageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Equipement.objects.all()
    lookup_field = 'reference'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EquipementAffichageSerializer
        return EquipementAffichageSerializer

    def get_queryset(self):
        if self.action == 'retrieve':
            return Equipement.objects.select_related(
                'lieu', 'modeleEquipement__fabricant', 'fournisseur', 'createurEquipement'
            ).prefetch_related(
                self._prefetch_statuts(),
                self._prefetch_defaillances(),
                self._prefetch_consommables(),
                self._prefetch_documents_techniques(),
            )
        return Equipement.objects.all()

    def _prefetch_statuts(self):
        return Prefetch('informationstatut_set', queryset=InformationStatut.objects.order_by('-dateChangement'), to_attr='statuts')

    def _prefetch_defaillances(self):
        return Prefetch('defaillance_set', queryset=Defaillance.objects.prefetch_related(
            'intervention_set', 'documentdefaillance_set', 'intervention_set__documentintervention_set'))

    def _prefetch_consommables(self):
        return Prefetch('modeleEquipement__estcompatible_set__consommable', queryset=Consommable.objects.all())

    def _prefetch_documents_techniques(self):
        return Prefetch('modeleEquipement__correspondre_set__documentTechnique', queryset=DocumentTechnique.objects.all())

    def get_object(self):
        reference = self.kwargs.get('reference')
        queryset = self.get_queryset()
        try:
            obj = queryset.get(reference=reference)
            self.check_object_permissions(self.request, obj)
            obj.dernier_statut = obj.statuts[0] if hasattr(obj, 'statuts') and obj.statuts else None
            return obj
        except Equipement.DoesNotExist:
            raise NotFound(f"Aucun équipement trouvé avec la référence {reference}")
