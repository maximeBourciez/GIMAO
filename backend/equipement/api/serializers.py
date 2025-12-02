from rest_framework import serializers
from equipement.models import Equipement, StatutEquipement, Constituer, ModeleEquipement, Compteur, FamilleEquipement


class EquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipement
        fields = '__all__'


class StatutEquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatutEquipement
        fields = '__all__'


class ConstituerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constituer
        fields = '__all__'


class ModeleEquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeleEquipement
        fields = '__all__'


class CompteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compteur
        fields = '__all__'


class FamilleEquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilleEquipement
        fields = '__all__'
