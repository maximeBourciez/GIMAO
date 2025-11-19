from rest_framework import serializers
from gestionDonnee.models import (
    Fabricant, Fournisseur, ModeleEquipement, Lieu,
    DocumentTechnique, Correspondre
)


class FabricantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabricant
        fields = '__all__'


class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = '__all__'


class ModeleEquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeleEquipement
        fields = '__all__'


class LieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lieu
        fields = '__all__'


class DocumentTechniqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTechnique
        fields = '__all__'


class CorrespondreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correspondre
        fields = '__all__'


class LieuHierarchySerializer(serializers.ModelSerializer):
    """Serializer pour afficher la hiérarchie des lieux (arbre)"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Lieu
        fields = ['id', 'nomLieu', 'typeLieu', 'children']

    def get_children(self, obj):
        children = Lieu.objects.filter(lieuParent=obj)
        serializer = self.__class__(children, many=True)
        return serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not representation['children']:
            representation.pop('children')
        return representation
