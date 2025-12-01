from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password, make_password

from utilisateur.models import Role, Utilisateur, Log
from .serializers import (
    RoleSerializer,
    UtilisateurSerializer,
    UtilisateurCreateSerializer,
    UtilisateurDetailSerializer,
    UtilisateurSimpleSerializer,
    LogSerializer,
    LoginSerializer,
    ChangePasswordSerializer
)


# ==================== ROLE VIEWSET ====================

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('rang')
    serializer_class = RoleSerializer


# ==================== UTILISATEUR VIEWSET ====================

class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all().order_by('id')

    def get_serializer_class(self):
        """
        Retourne dynamiquement le serializer selon l'action :
        - create → formulaire de création avec mot de passe
        - retrieve → détails complets (logs, rôles supplémentaires)
        - autres → sérialiseur simple
        """
        if self.action == "create":
            return UtilisateurCreateSerializer
        if self.action == "retrieve":
            return UtilisateurDetailSerializer
        return UtilisateurSerializer

    # ---------- LOGIN ----------
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nomUtilisateur = serializer.validated_data['nomUtilisateur']
        motDePasse = serializer.validated_data['motDePasse']

        try:
            user = Utilisateur.objects.get(nomUtilisateur=nomUtilisateur)
        except Utilisateur.DoesNotExist:
            return Response({"detail": "Utilisateur inconnu"}, status=400)

        if not check_password(motDePasse, user.motDePasse):
            return Response({"detail": "Mot de passe incorrect"}, status=400)

        return Response({
            "message": "Connexion réussie",
            "utilisateur": UtilisateurSerializer(user).data
        })

    # ---------- CHANGEMENT DE MOT DE PASSE ----------
    @action(detail=True, methods=['post'])
    def changer_mot_de_passe(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ancien = serializer.validated_data['ancien_motDePasse']
        nouveau = serializer.validated_data['nouveau_motDePasse']

        if not check_password(ancien, user.motDePasse):
            return Response({"detail": "Ancien mot de passe incorrect"}, status=400)

        user.motDePasse = make_password(nouveau)
        user.save()

        return Response({"message": "Mot de passe mis à jour avec succès"})


# ==================== LOG VIEWSET ====================

class LogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Log.objects.all().order_by('-date')
    serializer_class = LogSerializer

