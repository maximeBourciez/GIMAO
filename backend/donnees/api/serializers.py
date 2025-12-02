from rest_framework import serializers
from donnees.models import Lieu, TypeDocument, Document, Fabricant, Fournisseur, Adresse


class AdresseSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Adresse"""
    
    class Meta:
        model = Adresse
        fields = [
            'id',
            'numero',
            'rue',
            'ville',
            'code_postal',
            'pays',
            'complement'
        ]


class LieuSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Lieu"""
    lieuParent = serializers.PrimaryKeyRelatedField(
        queryset=Lieu.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Lieu
        fields = [
            'id',
            'nomLieu',
            'typeLieu',
            'lienPlan',
            'lieuParent',
            'x',
            'y'
        ]


class LieuDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour le modèle Lieu avec les relations"""
    lieuParent = serializers.SerializerMethodField()
    sous_lieux = serializers.SerializerMethodField()
    hierarchie_complete = serializers.SerializerMethodField()
    
    class Meta:
        model = Lieu
        fields = [
            'id',
            'nomLieu',
            'typeLieu',
            'lienPlan',
            'lieuParent',
            'x',
            'y',
            'sous_lieux',
            'hierarchie_complete'
        ]
    
    def get_lieuParent(self, obj):
        if obj.lieuParent:
            return {
                'id': obj.lieuParent.id,
                'nomLieu': obj.lieuParent.nomLieu,
                'typeLieu': obj.lieuParent.typeLieu
            }
        return None
    
    def get_sous_lieux(self, obj):
        sous_lieux = Lieu.objects.filter(lieuParent=obj)
        return [
            {
                'id': lieu.id,
                'nomLieu': lieu.nomLieu,
                'typeLieu': lieu.typeLieu
            }
            for lieu in sous_lieux
        ]
    
    def get_hierarchie_complete(self, obj):
        """Méthode récursive pour obtenir la hiérarchie complète des lieux parents"""
        hierarchy = []
        current_lieu = obj.lieuParent
        while current_lieu:
            hierarchy.append({
                'id': current_lieu.id,
                'nomLieu': current_lieu.nomLieu,
                'typeLieu': current_lieu.typeLieu
            })
            current_lieu = current_lieu.lieuParent
        return hierarchy[::-1]  # Inverser pour avoir du plus ancien au plus récent


class TypeDocumentSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle TypeDocument"""
    
    class Meta:
        model = TypeDocument
        fields = ['id', 'nomTypeDocument']


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Document"""
    typeDocument = TypeDocumentSerializer(read_only=True)
    typeDocument_id = serializers.PrimaryKeyRelatedField(
        queryset=TypeDocument.objects.all(),
        source='typeDocument',
        write_only=True
    )
    
    class Meta:
        model = Document
        fields = [
            'id',
            'nomDocument',
            'cheminAcces',
            'typeDocument',
            'typeDocument_id'
        ]


class DocumentSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour le modèle Document (sans nested objects)"""
    
    class Meta:
        model = Document
        fields = [
            'id',
            'nomDocument',
            'cheminAcces',
            'typeDocument'
        ]
        ref_name = 'DonneesDocumentSimple'


class FabricantSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Fabricant"""
    adresse = AdresseSerializer(read_only=True)
    adresse_id = serializers.PrimaryKeyRelatedField(
        queryset=Adresse.objects.all(),
        source='adresse',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Fabricant
        fields = [
            'id',
            'nom',
            'email',
            'numTelephone',
            'serviceApresVente',
            'adresse',
            'adresse_id'
        ]


class FabricantSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour le modèle Fabricant (sans nested objects)"""
    
    class Meta:
        model = Fabricant
        fields = [
            'id',
            'nom',
            'email',
            'numTelephone',
            'serviceApresVente',
            'adresse'
        ]
        ref_name = 'DonneesFabricantSimple'


class FournisseurSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Fournisseur"""
    adresse = AdresseSerializer(read_only=True)
    adresse_id = serializers.PrimaryKeyRelatedField(
        queryset=Adresse.objects.all(),
        source='adresse',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Fournisseur
        fields = [
            'id',
            'nom',
            'email',
            'numTelephone',
            'serviceApresVente',
            'adresse',
            'adresse_id'
        ]


class FournisseurSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour le modèle Fournisseur (sans nested objects)"""
    
    class Meta:
        model = Fournisseur
        fields = [
            'id',
            'nom',
            'email',
            'numTelephone',
            'serviceApresVente',
            'adresse'
        ]
        ref_name = 'DonneesFournisseurSimple'