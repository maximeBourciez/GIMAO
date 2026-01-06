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
    ChangePasswordSerializer,
    DefinirMotDePasseSerializer
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
        """
        Connexion d'un utilisateur.
        - Si l'utilisateur n'a pas de mot de passe ET jamais connecté : retourne besoinDefinirMotDePasse=True
        - Si l'utilisateur a un mot de passe : vérifie les credentials
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nomUtilisateur = serializer.validated_data['nomUtilisateur']
        motDePasse = serializer.validated_data.get('motDePasse')

        try:
            user = Utilisateur.objects.get(nomUtilisateur=nomUtilisateur, actif=True)
        except Utilisateur.DoesNotExist:
            return Response({"detail": "Utilisateur inconnu ou inactif"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.has_usable_password() and user.premiere_connexion():
            return Response({
                "besoinDefinirMotDePasse": True,
                "nomUtilisateur": user.nomUtilisateur,
                "message": "Première connexion : veuillez définir votre mot de passe"
            }, status=status.HTTP_200_OK)

        if not motDePasse or motDePasse.strip() == '':
            return Response({"detail": "Mot de passe requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(motDePasse):
            return Response({"detail": "Mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)

        from django.utils import timezone
        user.derniereConnexion = timezone.now()
        user.save(update_fields=['derniereConnexion'])

        return Response({
            "message": "Connexion réussie",
            "besoinDefinirMotDePasse": False,
            "utilisateur": UtilisateurSerializer(user).data
        }, status=status.HTTP_200_OK)

    # ---------- DÉFINIR MOT DE PASSE (PREMIÈRE CONNEXION) ----------
    @action(detail=False, methods=['post'])
    def definir_mot_de_passe(self, request):
        """
        Permet à un utilisateur sans mot de passe de définir son mot de passe lors de sa première connexion.
        Conditions : pas de mot de passe ET jamais connecté (derniereConnexion == null)
        """
        serializer = DefinirMotDePasseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nomUtilisateur = serializer.validated_data['nomUtilisateur']
        nouveau_motDePasse = serializer.validated_data['nouveau_motDePasse']

        try:
            user = Utilisateur.objects.get(nomUtilisateur=nomUtilisateur, actif=True)
        except Utilisateur.DoesNotExist:
            return Response({"detail": "Utilisateur inconnu ou inactif"}, status=status.HTTP_404_NOT_FOUND)

        if user.has_usable_password():
            return Response(
                {"detail": "Cet utilisateur a déjà un mot de passe. Utilisez l'endpoint de changement de mot de passe."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.premiere_connexion():
            return Response(
                {"detail": "Cet utilisateur s'est déjà connecté. Utilisez l'endpoint de changement de mot de passe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(nouveau_motDePasse)
        
        from django.utils import timezone
        user.derniereConnexion = timezone.now()
        user.save()

        return Response({
            "message": "Mot de passe défini avec succès. Vous pouvez maintenant vous connecter.",
            "utilisateur": UtilisateurSerializer(user).data
        }, status=status.HTTP_200_OK)

    # ---------- CHANGEMENT DE MOT DE PASSE ----------
    @action(detail=True, methods=['post'])
    def changer_mot_de_passe(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ancien = serializer.validated_data['ancien_motDePasse']
        nouveau = serializer.validated_data['nouveau_motDePasse']

        if not user.has_usable_password():
            return Response(
                {"detail": "Cet utilisateur n'a pas encore de mot de passe. Utilisez l'endpoint pour définir un mot de passe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(ancien):
            return Response({"detail": "Ancien mot de passe incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(nouveau)
        user.save()

        return Response({"message": "Mot de passe mis à jour avec succès"}, status=status.HTTP_200_OK)


# ==================== LOG VIEWSET ====================

class LogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Log.objects.all().order_by('-date')
    serializer_class = LogSerializer

