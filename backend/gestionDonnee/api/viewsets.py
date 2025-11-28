from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Prefetch
from gestionDonnee.models import (
    Fabricant, Fournisseur, ModeleEquipement, Lieu,
    DocumentTechnique, Correspondre
)
from gestionDonnee.api.serializers import (
    FabricantSerializer, FournisseurSerializer, ModeleEquipementSerializer,
    LieuSerializer, DocumentTechniqueSerializer, CorrespondreSerializer,
    LieuHierarchySerializer
)


class FabricantViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des fabricants"""
    queryset = Fabricant.objects.all()
    serializer_class = FabricantSerializer


class FournisseurViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des fournisseurs"""
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer


class ModeleEquipementViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des modèles d'équipement"""
    queryset = ModeleEquipement.objects.all()
    serializer_class = ModeleEquipementSerializer


class LieuViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des lieux avec optimisation des requêtes"""
    queryset = Lieu.objects.all()
    serializer_class = LieuSerializer

    def get_queryset(self):
        # Précharge les parents et enfants pour optimiser les requêtes
        return Lieu.objects.select_related('lieuParent').prefetch_related('lieu_set')


class DocumentTechniqueViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des documents techniques"""
    queryset = DocumentTechnique.objects.all()
    serializer_class = DocumentTechniqueSerializer


class CorrespondreViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion de la correspondance modèle-document"""
    queryset = Correspondre.objects.all()
    serializer_class = CorrespondreSerializer


@api_view(['GET'])
def get_lieux_hierarchy(request):
    """
    Retourne les lieux de premier niveau avec leurs enfants en structure hiérarchique.
    Utilisé pour l'affichage en arbre des lieux.
    """
    top_level_lieux = Lieu.objects.filter(lieuParent__isnull=True).prefetch_related('lieu_set')
    serializer = LieuHierarchySerializer(top_level_lieux, many=True, context={'request': request})
    return Response(serializer.data)
