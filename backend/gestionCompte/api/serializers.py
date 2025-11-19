from rest_framework import serializers
from django.contrib.auth import get_user_model
from gestionCompte.models import Role, Avoir

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class AvoirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avoir
        fields = '__all__'
