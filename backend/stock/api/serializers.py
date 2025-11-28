from rest_framework import serializers
from stock.models import Consommable, StockConsommable, EstCompatible


class ConsommableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consommable
        fields = '__all__'


class StockConsommableSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockConsommable
        fields = '__all__'


class EstCompatibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstCompatible
        fields = '__all__'
