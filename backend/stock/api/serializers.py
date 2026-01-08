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


class ConsommableDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour le modèle Consommable avec informations du magasin"""
    magasin_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Consommable
        fields = ['id', 'designation', 'lienImageConsommable', 'magasin', 'magasin_details',
                  'seuilStockFaible', 'documents']
    
    def get_magasin_details(self, obj):
        if obj.magasin:
            return {
                'id': obj.magasin.id,
                'nom': obj.magasin.nom,
                'estMobile': obj.magasin.estMobile,
            }
        return None


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
