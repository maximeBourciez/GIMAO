from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from donnees.models import Lieu, Fabricant, Fournisseur, TypeDocument
from donnees.api.serializers import (
    FabricantSimpleSerializer,
    FournisseurSimpleSerializer,
    TypeDocumentSerializer,
)
from stock.models import Consommable
from stock.api.serializers import ConsommableSerializer
from maintenance.models import TypePlanMaintenance
from maintenance.api.serializers import TypePlanMaintenanceSerializer
from equipement.models import ModeleEquipement, FamilleEquipement
from equipement.api.serializers import (
    ModeleEquipementSerializer,
    FamilleEquipementSerializer,
)


class EquipementFormDataView(APIView):
    """
    Endpoint unique pour récupérer toutes les données nécessaires à la création d'un équipement.
    Réduit 8 requêtes API en une seule pour améliorer les performances (Green IT).

    GET /api/equipements/form-data/
    """

    def get(self, request):
        try:
            # Hiérarchie des lieux
            def build_tree(lieu):
                children = Lieu.objects.filter(lieuParent=lieu)
                return {
                    "id": lieu.id,
                    "nomLieu": lieu.nomLieu,
                    "children": [build_tree(child) for child in children],
                }

            racines = Lieu.objects.filter(lieuParent__isnull=True)
            locations = [build_tree(racine) for racine in racines]

            # Autres données
            equipment_models = ModeleEquipementSerializer(
                ModeleEquipement.objects.all(), many=True
            ).data

            fabricants = FabricantSimpleSerializer(
                Fabricant.objects.all(), many=True
            ).data

            fournisseurs = FournisseurSimpleSerializer(
                Fournisseur.objects.all(), many=True
            ).data

            consumables = ConsommableSerializer(
                Consommable.objects.all(), many=True
            ).data

            familles = FamilleEquipementSerializer(
                FamilleEquipement.objects.all(), many=True
            ).data

            types_pm = TypePlanMaintenanceSerializer(
                TypePlanMaintenance.objects.all(), many=True
            ).data

            types_documents = TypeDocumentSerializer(
                TypeDocument.objects.all(), many=True
            ).data

            return Response(
                {
                    "locations": locations,
                    "equipmentModels": equipment_models,
                    "fabricants": fabricants,
                    "fournisseurs": fournisseurs,
                    "consumables": consumables,
                    "familles": familles,
                    "typesPM": types_pm,
                    "typesDocuments": types_documents,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "error": "Erreur lors de la récupération des données",
                    "detail": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
