import json

from rest_framework import viewsets, status
from rest_framework.response import Response
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

from maintenance.models import PlanMaintenance, PlanMaintenanceConsommable, PlanMaintenanceDocument
from donnees.models import Lieu, Document


class EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return EquipementCreateSerializer
        return EquipementSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        print("DATA BRUTES :", request.data)

        # ⚠️ IMPORTANT
        # request.data est un QueryDict + fichiers → on copie SANS le transformer en dict
        data = request.data.copy()

        # -------------------------
        # Normalisation des champs simples
        # -------------------------

        # lieu : objet -> id
        if "lieu" in data:
            lieu_value = data["lieu"]
            # Si c'est une chaîne JSON, on la parse
            if isinstance(lieu_value, str):
                try:
                    lieu_obj = json.loads(lieu_value)
                    data["lieu"] = lieu_obj["id"]
                except (TypeError, ValueError, KeyError):
                    pass  # déjà un id ou format invalide
            # Si c'est un dict, on extrait l'id
            elif isinstance(lieu_value, dict):
                data["lieu"] = lieu_value["id"]
            # Sinon c'est déjà un id (int)

        # Champs JSON envoyés en string
        for field in ["consommables", "compteurs"]:
            if field in data and isinstance(data[field], str):
                data[field] = json.loads(data[field])

        # Gestion du fichier image
        # Si le fichier n'est pas valide, on le retire
        if "lienImageEquipement" in data:
            file_value = data["lienImageEquipement"]
            # Si c'est une chaîne '[object File]' ou vide, on le retire
            if isinstance(file_value, str) and (file_value == '[object File]' or not file_value):
                data.pop("lienImageEquipement")
            # Sinon, request.FILES devrait contenir le vrai fichier

        print("DATA NORMALISÉES :", data)

        # -------------------------
        # Validation serializer
        # -------------------------
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # -------------------------
        # Récupération des dépendances
        # -------------------------
        user = Utilisateur.objects.get(id=data["createurEquipement"])
        modele = ModeleEquipement.objects.get(id=data["modeleEquipement"])
        fabricant = Fabricant.objects.get(id=data["fabricant"])
        fournisseur = Fournisseur.objects.get(id=data["fournisseur"])
        famille = FamilleEquipement.objects.get(id=data["famille"])
        lieu = Lieu.objects.get(id=data["lieu"])

        # -------------------------
        # Création de l'équipement
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
            lienImage=data.get("lienImageEquipement")  # UploadedFile OK ou None
        )

        # -------------------------
        # Consommables
        # -------------------------
        for consommable_id in data.get("consommables", []):
            Constituer.objects.create(
                equipement=equipement,
                consommable_id=consommable_id
            )

        # -------------------------
        # Compteurs & plans de maintenance
        # -------------------------
        for cp in data.get("compteurs", []):
            compteur = Compteur.objects.create(
                equipement=equipement,
                nomCompteur=cp["nom"],
                descriptifMaintenance=cp.get("description", ""),
                valeurCourante=cp["valeurActuelle"],
                ecartInterventions=cp["intervalle"],
                unite=cp["unite"],
                estPrincipal=cp.get("estPrincipal", False),
                estGlissant=cp.get("estGlissant", False),
                necessiteHabilitationElectrique=cp.get("habElec", False),
                necessitePermisFeu=cp.get("permisFeu", False),
                prochaineMaintenance=(
                    int(cp["derniereIntervention"]) + int(cp["intervalle"])
                )
            )

            pm = cp.get("planMaintenance")
            if not pm:
                continue

            plan = PlanMaintenance.objects.create(
                compteur=compteur,
                equipement=equipement,
                nom=pm["nom"],
                type_plan_maintenance_id=pm["type"]
            )

            # Consommables du plan
            for cpm in pm.get("consommables", []):
                PlanMaintenanceConsommable.objects.create(
                    plan_maintenance=plan,
                    consommable_id=cpm["consommable"],
                    quantite_necessaire=cpm["quantite"]
                )

            # Documents
            for doc in pm.get("documents", []):
                # Vérifier si le fichier est valide
                doc_file = doc.get("file")
                if not doc_file or (isinstance(doc_file, dict) and not doc_file):
                    # Fichier invalide, on saute ce document
                    continue

                document = Document.objects.create(
                    nomDocument=doc["titre"],
                    cheminAcces=doc_file,
                    typeDocument_id=doc["type"]
                )

                PlanMaintenanceDocument.objects.create(
                    plan_maintenance=plan,
                    document=document
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