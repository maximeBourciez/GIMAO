from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from django.db.models import Prefetch

from equipement.models import Equipement, StatutEquipement, Constituer
from equipement.api.serializers import *
from maintenance.models import DemandeIntervention
from stock.models import Consommable
from donnees.models import Lieu, Document, TypeDocument


class EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.all()
    serializer_class = EquipementSerializer
    lookup_field = 'reference'


class StatutEquipementViewSet(viewsets.ModelViewSet):
    queryset = StatutEquipement.objects.all()
    serializer_class = StatutEquipementSerializer


class ConstituerViewSet(viewsets.ModelViewSet):
    queryset = Constituer.objects.all()
    serializer_class = ConstituerSerializer


class EquipementAvecDernierStatutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Equipement.objects.all()
    serializer_class = EquipementAvecDernierStatutSerializer
    lookup_field = 'reference'

    def get_queryset(self):
        return Equipement.objects.prefetch_related(
            Prefetch(
                'StatutEquipement_set',
                queryset=StatutEquipement.objects.order_by('-dateChangement'),
                to_attr='statuts'
            )
        )

class ModeleEquipementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModeleEquipement.objects.all()
    serializer_class = ModeleEquipementSerializer

class EquipementDetailViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.select_related('lieu', 'modele')  # ✅ 'modele' pas 'modeleEquipement'
    serializer_class = EquipementDetailSerializer
    lookup_field = 'reference'

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch(
                'statuts',  # ✅ Utilise le related_name, pas 'StatutEquipement_set'
                queryset=StatutEquipement.objects.order_by('-dateChangement')
            )
        )

class EquipementAffichageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Equipement.objects.all()
    serializer_class = EquipementAffichageSerializer
    lookup_field = 'reference'

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

    # Méthodes internes pour préfetch
    def _prefetch_statuts(self):
        return Prefetch(
            'StatutEquipement_set',
            queryset=StatutEquipement.objects.order_by('-dateChangement'),
            to_attr='statuts'
        )

    def _prefetch_defaillances(self):
        return Prefetch(
            'defaillance_set',
            queryset=DemandeIntervention.objects.prefetch_related(
                'intervention_set',
                'documentdefaillance_set',
                'intervention_set__documentintervention_set'
            )
        )

    def _prefetch_consommables(self):
        return Prefetch(
            'modeleEquipement__estcompatible_set__consommable',
            queryset=Consommable.objects.all()
        )

    def _prefetch_documents_techniques(self):
        return Prefetch(
            'modeleEquipement__correspondre_set__documentTechnique',
            queryset=Document.objects.all()
        )

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
