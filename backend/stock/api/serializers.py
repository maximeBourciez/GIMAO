from rest_framework import serializers
from stock.models import *


class MagasinSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Magasin"""
    class Meta:
        model = Magasin
        fields = '__all__'


class MagasinDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour le modèle Magasin avec informations de l'adresse"""
    adresse_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Magasin
        fields = ['id', 'nom', 'estMobile', 'adresse', 'adresse_details']
    
    def get_adresse_details(self, obj):
        if obj.adresse:
            return {
                'id': obj.adresse.id,
                'rue': getattr(obj.adresse, 'rue', None),
                'codePostal': getattr(obj.adresse, 'codePostal', None),
                'ville': getattr(obj.adresse, 'ville', None),
            }
        return None


class ConsommableSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Consommable"""
    class Meta:
        model = Consommable
        fields = '__all__'


class FournitureConsommableSerializer(serializers.ModelSerializer):
    """Serializer pour les fournitures (PorterSur) avec détails du fournisseur et fabricant"""
    fournisseur_nom = serializers.CharField(source='fournisseur.nom', read_only=True)
    fabricant_nom = serializers.CharField(source='fabricant.nom', read_only=True)
    
    class Meta:
        model = PorterSur
        fields = ['id', 'fournisseur', 'fournisseur_nom', 'fabricant', 'fabricant_nom', 
                  'quantite', 'prix_unitaire', 'date_reference_prix']


class ConsommableDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour le modèle Consommable avec informations du magasin"""
    magasin_details = serializers.SerializerMethodField()
    fournitures = FournitureConsommableSerializer(many=True, read_only=True)
    quantite_totale = serializers.SerializerMethodField()
    
    class Meta:
        model = Consommable
        fields = ['id', 'designation', 'lienImageConsommable', 'magasin', 'magasin_details',
                  'fournitures', 'quantite_totale', 'seuilStockFaible', 'documents']
    
    def get_magasin_details(self, obj):
        if obj.magasin:
            return {
                'id': obj.magasin.id,
                'nom': obj.magasin.nom,
                'estMobile': obj.magasin.estMobile,
            }
        return None
    
    def get_quantite_totale(self, obj):
        # Somme des quantités de toutes les fournitures
        total = sum(fourniture.quantite for fourniture in obj.fournitures.all())
        return total


class PorterSurSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle PorterSur (fourniture de consommable)"""
    class Meta:
        model = PorterSur
        fields = '__all__'


class EstCompatibleSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle EstCompatible"""
    class Meta:
        model = EstCompatible
        fields = '__all__'
