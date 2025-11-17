# api/serializers.py
import os
from rest_framework import viewsets, status
from django.conf import settings
from django.db.models import Prefetch
from rest_framework.response import Response
from django.apps import apps
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from gimao.models import (
    Role, Avoir, Fabricant, Fournisseur, Consommable, StockConsommable,
    ModeleEquipement, EstCompatible, Lieu, Equipement, Constituer,
    InformationStatut, DocumentTechnique, Correspondre, Defaillance,
    DocumentDefaillance, Intervention, DocumentIntervention
)
from .serializers import (
    UserSerializer,
    RoleSerializer,
    AvoirSerializer,
    FabricantSerializer,
    FournisseurSerializer,
    ConsommableSerializer,
    StockConsommableSerializer,
    ModeleEquipementSerializer,
    EstCompatibleSerializer,
    LieuSerializer,
    EquipementSerializer,
    ConstituerSerializer,
    InformationStatutSerializer,
    DocumentTechniqueSerializer,
    CorrespondreSerializer,
    DefaillanceSerializer,
    DocumentDefaillanceSerializer,
    InterventionSerializer,
    DocumentInterventionSerializer,

    EquipementAvecDernierStatutSerializer,
    EquipementDetailSerializer,
    LieuHierarchySerializer,
    EquipementAffichageSerializer,
    InterventionAfficherSerializer,
    DefaillanceAfficherSerializer,
)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class AvoirViewSet(viewsets.ModelViewSet):
    queryset = Avoir.objects.all()
    serializer_class = AvoirSerializer

class FabricantViewSet(viewsets.ModelViewSet):
    queryset = Fabricant.objects.all()
    serializer_class = FabricantSerializer

class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer

class ConsommableViewSet(viewsets.ModelViewSet):
    queryset = Consommable.objects.all()
    serializer_class = ConsommableSerializer

class StockConsommableViewSet(viewsets.ModelViewSet):
    queryset = StockConsommable.objects.all()
    serializer_class = StockConsommableSerializer

class ModeleEquipementViewSet(viewsets.ModelViewSet):
    queryset = ModeleEquipement.objects.all()
    serializer_class = ModeleEquipementSerializer

class EstCompatibleViewSet(viewsets.ModelViewSet):
    queryset = EstCompatible.objects.all()
    serializer_class = EstCompatibleSerializer

class LieuViewSet(viewsets.ModelViewSet):
    queryset = Lieu.objects.all()
    serializer_class = LieuSerializer

class EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.all()
    serializer_class = EquipementSerializer

class ConstituerViewSet(viewsets.ModelViewSet):
    queryset = Constituer.objects.all()
    serializer_class = ConstituerSerializer

class InformationStatutViewSet(viewsets.ModelViewSet):
    queryset = InformationStatut.objects.all()
    serializer_class = InformationStatutSerializer

class DocumentTechniqueViewSet(viewsets.ModelViewSet):
    queryset = DocumentTechnique.objects.all()
    serializer_class = DocumentTechniqueSerializer

class CorrespondreViewSet(viewsets.ModelViewSet):
    queryset = Correspondre.objects.all()
    serializer_class = CorrespondreSerializer

class DefaillanceViewSet(viewsets.ModelViewSet):
    queryset = Defaillance.objects.all()
    serializer_class = DefaillanceSerializer

class DocumentDefaillanceViewSet(viewsets.ModelViewSet):
    queryset = DocumentDefaillance.objects.all()
    serializer_class = DocumentDefaillanceSerializer

class InterventionViewSet(viewsets.ModelViewSet):
    queryset = Intervention.objects.all()
    serializer_class = InterventionSerializer

class DocumentInterventionViewSet(viewsets.ModelViewSet):
    queryset = DocumentIntervention.objects.all()
    serializer_class = DocumentInterventionSerializer


@api_view(['DELETE'])
def delete_document(request, model_name, pk):
    try:
        # Obtenir le modèle dynamiquement
        model = apps.get_model('gimao', model_name)
        
        # Vérifier si le modèle existe
        if model is None:
            return Response({"message": f"Modèle {model_name} non trouvé"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtenir le document
        document = model.objects.get(pk=pk)
        
        # Supprimer le fichier physique
        if hasattr(document, 'lienDocumentDefaillance'):
            file_path = os.path.join(settings.MEDIA_ROOT, str(document.lienDocumentDefaillance))
        elif hasattr(document, 'lienDocumentIntervention'):
            file_path = os.path.join(settings.MEDIA_ROOT, str(document.lienDocumentIntervention))
        else:
            file_path = None

        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        
        # Supprimer l'entrée de la base de données
        document.delete()
        
        return Response({"message": "Document supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
    except model.DoesNotExist:
        return Response({"message": "Document non trouvé"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# --------------------------------------------------------------------------


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Affichage des equipemnts de la page Equipements.vue
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# Affichage de la hiérarchie des lieux (LieuxExplorer)
@api_view(['GET'])
def get_lieux_hierarchy(request):
    top_level_lieux = Lieu.objects.filter(lieuParent__isnull=True).prefetch_related('lieu_set')
    serializer = LieuHierarchySerializer(top_level_lieux, many=True, context={'request': request})
    return Response(serializer.data)


class EquipementAffichageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour l'affichage détaillé des informations d'un équipement.
    """
    queryset = Equipement.objects.all()
    lookup_field = 'reference'

    def get_serializer_class(self):
        """
        Utilise EquipementAffichageSerializer pour la vue détaillée, 
        sinon utilise EquipementSerializer.
        """
        if self.action == 'retrieve':
            return EquipementAffichageSerializer
        return EquipementSerializer

    def get_queryset(self):
        """
        Optimise la requête avec select_related et prefetch_related pour la vue détaillée.
        """
        if self.action == 'retrieve':
            return Equipement.objects.select_related(
                'lieu', 
                'modeleEquipement__fabricant', 
                'fournisseur', 
                'createurEquipement'
            ).prefetch_related(
                self._prefetch_statuts(),
                self._prefetch_defaillances(),
                self._prefetch_consommables(),
                self._prefetch_documents_techniques(),
            )
        return Equipement.objects.all()

    def _prefetch_statuts(self):
        """Méthode auxiliaire pour précharger les statuts."""
        return Prefetch(
            'informationstatut_set', 
            queryset=InformationStatut.objects.order_by('-dateChangement'),
            to_attr='statuts'
        )

    def _prefetch_defaillances(self):
        """Méthode auxiliaire pour précharger les défaillances et les données associées."""
        return Prefetch(
            'defaillance_set', 
            queryset=Defaillance.objects.prefetch_related(
                'intervention_set',
                'documentdefaillance_set',
                'intervention_set__documentintervention_set'
            )
        )

    def _prefetch_consommables(self):
        """Méthode auxiliaire pour précharger les consommables compatibles."""
        return Prefetch(
            'modeleEquipement__estcompatible_set__consommable', 
            queryset=Consommable.objects.all()
        )

    def _prefetch_documents_techniques(self):
        """Méthode auxiliaire pour précharger les documents techniques."""
        return Prefetch(
            'modeleEquipement__correspondre_set__documentTechnique',
            queryset=DocumentTechnique.objects.all()
        )

    def get_object(self):
        """
        Récupère l'objet équipement et ajoute le dernier statut.
        """
        reference = self.kwargs.get('reference')
        queryset = self.get_queryset()
        try:
            obj = queryset.get(reference=reference)
            self.check_object_permissions(self.request, obj)
            obj.dernier_statut = obj.statuts[0] if hasattr(obj, 'statuts') and obj.statuts else None
            return obj
        except Equipement.DoesNotExist:
            raise NotFound(f"Aucun équipement trouvé avec la référence {reference}")


class InterventionAfficherViewSet(viewsets.ModelViewSet):
    queryset = Intervention.objects.all()
    serializer_class = InterventionAfficherSerializer

    def get_queryset(self):
        return Intervention.objects.select_related(
            'defaillance__equipement',
            'createurIntervention',
            'responsable'
        ).prefetch_related(
            'documentintervention_set'
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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