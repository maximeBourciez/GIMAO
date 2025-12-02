from rest_framework import serializers
from stock.models import *


class ConsommableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consommable
        fields = '__all__'


class StockConsommableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magasin
        fields = '__all__'


class EstCompatibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstCompatible
        fields = '__all__'
