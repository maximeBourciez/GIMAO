import json
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from django.db.models import Prefetch
from django.db import transaction

# Models
from maintenance.models import DemandeIntervention, BonTravail
from donnees.models import Document
from stock.models import Consommable
from equipement.models import *
from utilisateur.models import Utilisateur

# Serializers
from equipement.api.serializers import (
    EquipementSerializer,
    StatutEquipementSerializer,
    ConstituerSerializer,
    ModeleEquipementSerializer,
    CompteurSerializer,
    FamilleEquipementSerializer,
    EquipementAffichageSerializer,
    EquipementCreateSerializer
)


class EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return EquipementCreateSerializer
        return EquipementSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        print("DATA REÇUES :", request.data)

        # Convertir QueryDict -> dict normal
        data = {k: v for k, v in request.data.items()}

        # Normaliser listes envoyées par Vuetify (['x'] → 'x')
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        # Désérialiser les JSON envoyés en string
        import json
        if "consommables" in data and isinstance(data["consommables"], str):
            data["consommables"] = json.loads(data["consommables"])

        if "compteurs" in data and isinstance(data["compteurs"], str):
            data["compteurs"] = json.loads(data["compteurs"])

        print("DATA TRAITÉES :", data)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # -------------------------
        # Récupération des données dépendantes
        # -------------------------
        user = Utilisateur.objects.get(id=data["createurEquipement"])
        modele = ModeleEquipement.objects.get(id=data["modeleEquipement"])
        fabricant = Fabricant.objects.get(id=data["fabricant"])
        fournisseur = Fournisseur.objects.get(id=data["fournisseur"])
        famille = FamilleEquipement.objects.get(id=data["famille"])
        lieu = Lieu.objects.get(id=data["lieu"])

        # -------------------------
        # Création de l'équipement simple
        # -------------------------
        equipement = Equipement.objects.create(
            reference=data["reference"],
            designation=data["designation"],
            dateCreation=data["dateCreation"],
            dateMiseEnService=data.get("dateMiseEnService"),
            prixAchat=data.get("prixAchat", 0),
            createurEquipement=user,
            lieu=lieu,
            modele=modele,
            famille=famille,
            fournisseur=fournisseur,
            fabricant=fabricant,
            numSerie=data.get("numSerie", ""),
            lienImage=data.get("lienImageEquipement")
        )

        # -------------------------
        # Gérer les consommables
        # -------------------------
        for cid in data.get("consommables", []):
            Constituer.objects.create(equipement=equipement, consommable_id=cid)

        # -------------------------
        # Gestion des compteurs
        # -------------------------
        for cp in data.get("compteurs", []):
            compteur = Compteur.objects.create(
                equipement=equipement,
                nomCompteur=cp["nom"],
                intervalle=cp["intervalle"],
                unite=cp["unite"],
            )

            # Plan de maintenance ?
            pm = cp.get("planMaintenance")
            if pm:
                plan = PlanMaintenance.objects.create(
                    compteur=compteur,
                    nom=pm["nom"]
                )

                # Consommables du plan
                for cpm in pm.get("consommables", []):
                    PlanMaintenanceConsommable.objects.create(
                        plan=plan,
                        consommable_id=cpm["consommable"],
                        quantite=cpm["quantite"]
                    )

                # Documents
                for doc in pm.get("documents", []):
                    Document.objects.create(
                        planMaintenance=plan,
                        nomDocument=doc["titre"],
                        fichier=doc["file"]
                    )

        return Response(
            EquipementSerializer(equipement).data,
            status=status.HTTP_201_CREATED
        )


class StatutEquipementViewSet(viewsets.ModelViewSet):
    queryset = StatutEquipement.objects.all()
    serializer_class = StatutEquipementSerializer


class ConstituerViewSet(viewsets.ModelViewSet):
    queryset = Constituer.objects.all()
    serializer_class = ConstituerSerializer


class ModeleEquipementViewSet(viewsets.ModelViewSet):
    queryset = ModeleEquipement.objects.all()
    serializer_class = ModeleEquipementSerializer


class CompteurViewSet(viewsets.ModelViewSet):
    queryset = Compteur.objects.all()
    serializer_class = CompteurSerializer


class FamilleEquipementViewSet(viewsets.ModelViewSet):
    queryset = FamilleEquipement.objects.all()
    serializer_class = FamilleEquipementSerializer


class EquipementAffichageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour l'affichage détaillé des équipements"""
    serializer_class = EquipementAffichageSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Equipement.objects.select_related(
            'lieu', 'modele__fabricant', 'famille'
        ).prefetch_related(
            'statuts',
            'compteurs',
            'documents'
        )
