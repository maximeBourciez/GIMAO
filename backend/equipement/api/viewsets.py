from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from django.db.models import Prefetch

from equipement.models import Equipement, StatutEquipement, Constituer
from equipement.api.serializers import *
from maintenance.models import DemandeIntervention, BonTravail
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
                'lieu', 'modele__fabricant', 'famille'
            ).prefetch_related(
                self._prefetch_statuts(),
                self._prefetch_consommables(),
                self._prefetch_documents(),
                self._prefetch_compteurs(),
            )
        return Equipement.objects.all()

    # Méthodes internes pour préfetch
    def _prefetch_statuts(self):
        return Prefetch(
            'statuts',
            queryset=StatutEquipement.objects.order_by('-dateChangement'),
            to_attr='statuts_list'
        )

    def _prefetch_defaillances(self):
        return Prefetch(
            'demandeintervention_set',
            queryset=DemandeIntervention.objects.prefetch_related(
                'intervention_set',
                'documentdefaillance_set',
                'intervention_set__documentintervention_set'
            )
        )

    def _prefetch_consommables(self):
        return Prefetch(
            'modele__estcompatible_set__consommable',
            queryset=Consommable.objects.select_related('fabricant', 'magasin').prefetch_related('documents')
        )

    def _prefetch_documents(self):
        return Prefetch(
            'documents',
            queryset=Document.objects.all(),
            to_attr='documents_list'
        )

    def _prefetch_compteurs(self):
        return Prefetch(
            'compteurs',
            queryset=Compteur.objects.all(),
            to_attr='compteurs_list'
        )

    def get_object(self):
        reference = self.kwargs.get('reference')
        queryset = self.get_queryset()
        try:
            obj = queryset.get(reference=reference)
            self.check_object_permissions(self.request, obj)
            # Récupérer le dernier statut
            if hasattr(obj, 'statuts_list') and obj.statuts_list:
                obj.dernier_statut = obj.statuts_list[0]
            else:
                obj.dernier_statut = None
            return obj
        except Equipement.DoesNotExist:
            raise NotFound(f"Aucun équipement trouvé avec la référence {reference}")