from rest_framework import viewsets
from django.contrib.auth import get_user_model
from gestionCompte.models import Role, Avoir
from gestionCompte.api.serializers import UserSerializer, RoleSerializer, AvoirSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des utilisateurs"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des rôles"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class AvoirViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion de l'association utilisateur-rôle"""
    queryset = Avoir.objects.all()
    serializer_class = AvoirSerializer
