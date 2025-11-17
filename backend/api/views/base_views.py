from rest_framework import viewsets
from django.contrib.auth import get_user_model
from gimao.models import (
    Role, Avoir, Fabricant, Fournisseur, Consommable, StockConsommable,
    ModeleEquipement, EstCompatible, Lieu, Equipement, Constituer,
    InformationStatut, DocumentTechnique, Correspondre, Defaillance,
    DocumentDefaillance, Intervention, DocumentIntervention
)
from api.serializers import (
    UserSerializer, RoleSerializer, AvoirSerializer, FabricantSerializer,
    FournisseurSerializer, ConsommableSerializer, StockConsommableSerializer,
    ModeleEquipementSerializer, EstCompatibleSerializer, LieuSerializer,
    EquipementSerializer, ConstituerSerializer, InformationStatutSerializer,
    DocumentTechniqueSerializer, CorrespondreSerializer, DefaillanceSerializer,
    DocumentDefaillanceSerializer, InterventionSerializer, DocumentInterventionSerializer
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
