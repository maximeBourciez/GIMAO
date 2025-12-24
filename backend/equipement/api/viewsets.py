import json
from rest_framework import viewsets, status
from rest_framework.response import Response
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
        print("=" * 80)
        print("📦 DONNÉES BRUTES REÇUES")
        print("=" * 80)
        print("POST data:", dict(request.data))
        print("\n📁 FICHIERS REÇUS:")
        for key in request.FILES.keys():
            print(f"  - {key}: {request.FILES[key].name}")
        print("=" * 80)

        data = dict(request.data)
        
        # Extraire les valeurs uniques des listes (QueryDict met tout en liste)
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        # -------------------------
        # Normalisation des champs simples
        # -------------------------

        # lieu : objet -> id
        if "lieu" in data:
            lieu_value = data["lieu"]
            if isinstance(lieu_value, str):
                try:
                    lieu_obj = json.loads(lieu_value)
                    data["lieu"] = lieu_obj["id"]
                except (TypeError, ValueError, KeyError):
                    pass
            elif isinstance(lieu_value, dict):
                data["lieu"] = lieu_value["id"]

        # Champs JSON envoyés en string
        for field in ["consommables", "compteurs"]:
            if field in data and isinstance(data[field], str):
                data[field] = json.loads(data[field])

        print("\n✅ DONNÉES NORMALISÉES:", data)

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
            lienImage=data.get("lienImageEquipement")
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
        for compteur_index, cp in enumerate(data.get("compteurs", [])):
            print(f"\n🔧 Traitement compteur #{compteur_index}: {cp.get('nom')}")
            
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
                print(f"  ⚠️  Pas de plan de maintenance pour ce compteur")
                continue

            print(f"  📋 Création du plan: {pm['nom']}")
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

            # -------------------------
            # Documents du plan
            # -------------------------
            for doc_index, doc in enumerate(pm.get("documents", [])):
                # Cherche le fichier avec le nouveau format
                file_key = f"compteur_{compteur_index}_document_{doc_index}"
                uploaded_file = request.FILES.get(file_key)

                if not uploaded_file:
                    continue

                # Créer le document
                document = Document.objects.create(
                    nomDocument=doc.get("titre", uploaded_file.name),
                    cheminAcces=uploaded_file,
                    typeDocument_id=doc.get("type")
                )

                # Lier au plan de maintenance
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