

import hashlib
from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password, make_password

from utilisateur.models import Role, Utilisateur, Log, Permission, UtilisateurPermission, RolePermission, Module
from .serializers import (
    RoleSerializer,
    UtilisateurSerializer,
    UtilisateurCreateSerializer,
    UtilisateurDetailSerializer,
    UtilisateurSimpleSerializer,
    LogSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    DefinirMotDePasseSerializer,
    PermissionSerializer,
    ModuleSerializer,
)
from gimao.viewsets import GimaoModelViewSet
from gimao.pagination import StandardPagination
from security.models import ApiToken, create_token


# ==================== ROLE VIEWSET ====================

class RoleViewSet(GimaoModelViewSet):
    queryset = Role.objects.all().order_by('nomRole')
    serializer_class = RoleSerializer

    @action(detail=True, methods=['post'])
    def dupliquer(self, request, pk=None):
        role = self.get_object()
        nouveau_nom = request.data.get('nomRole', f'Copie de {role.nomRole}')
        
        # Vérifier que le nom n'existe pas déjà
        if Role.objects.filter(nomRole=nouveau_nom).exists():
            return Response(
                {"detail": f"Un rôle avec le nom '{nouveau_nom}' existe déjà."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer le nouveau rôle
        nouveau_role = Role.objects.create(nomRole=nouveau_nom)
        
        # Copier les permissions
        for rp in RolePermission.objects.filter(role=role):
            RolePermission.objects.create(role=nouveau_role, permission=rp.permission)
        
        serializer = self.get_serializer(nouveau_role)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ==================== MODULE VIEWSET ====================

class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet en lecture seule pour lister tous les modules disponibles.
    GET /api/modules/
    GET /api/modules/{id}/
    """
    queryset = Module.objects.all().order_by('nom')
    serializer_class = ModuleSerializer


# ==================== PERMISSION VIEWSET ====================

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet en lecture seule pour lister toutes les permissions disponibles.
    Utilisé par les pages de gestion des rôles et des permissions utilisateur.
    GET /api/permissions/
    GET /api/permissions/{id}/
    """
    queryset = Permission.objects.select_related('module').all().order_by('nomPermission')
    serializer_class = PermissionSerializer


# ==================== UTILISATEUR VIEWSET ====================

class UtilisateurViewSet(GimaoModelViewSet):
    queryset = Utilisateur.objects.all()
    pagination_class = StandardPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nomUtilisateur', 'prenom', 'nomFamille', 'email', 'role__nomRole']
    ordering_fields = ['id', 'nomUtilisateur', 'prenom', 'nomFamille', 'dateCreation', 'derniereConnexion']
    ordering = ['nomFamille', 'prenom', 'id']

    def _get_list_queryset(self):
        return Utilisateur.objects.select_related('role').prefetch_related(
            Prefetch(
                'role__permissions',
                queryset=Permission.objects.only('id', 'nomPermission', 'description').order_by('id'),
            ),
            Prefetch(
                'permissions_personnalisees',
                queryset=UtilisateurPermission.objects.select_related('permission').only(
                    'id',
                    'utilisateur_id',
                    'permission_id',
                    'permission__id',
                    'permission__nomPermission',
                ),
            ),
        ).order_by('nomFamille', 'prenom', 'id')

    def get_queryset(self):
        queryset = self._get_list_queryset()

        role_id = self.request.query_params.get('role_id')
        if role_id and str(role_id).isdigit():
            queryset = queryset.filter(role_id=int(role_id))

        return queryset

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
    def exists(self, request):
        """
        Vérifie si un utilisateur avec le nom d'utilisateur donné existe et est actif.
        """
        nomUtilisateur = request.data.get('nomUtilisateur')
        message = ""
        if not nomUtilisateur:
            return Response({"detail": "nomUtilisateur est requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Utilisateur.objects.get(nomUtilisateur=nomUtilisateur, actif=True)
            exists = user.has_usable_password()
        except Utilisateur.DoesNotExist:
            exists = False
            message = "Utilisateur inconnu ou inactif"

        return Response({"existe": exists, "message": message}, status=status.HTTP_200_OK)

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
            return Response({"detail": "Mot de passe requis", "error": True}, status=status.HTTP_403_FORBIDDEN)

        if not user.check_password(motDePasse):
            return Response({"detail": "Mot de passe incorrect", "error": True}, status=status.HTTP_403_FORBIDDEN)

        from django.utils import timezone
        user.derniereConnexion = timezone.now()
        user.save(update_fields=['derniereConnexion'])

        token = create_token(user)

        return Response({
            "message": "Connexion réussie",
            "besoinDefinirMotDePasse": False,
            "utilisateur": UtilisateurSerializer(user).data,
            "token": token,
            "error": False
        }, status=status.HTTP_200_OK)

    # ---------- DÉFINIR MOT DE PASSE (PREMIÈRE CONNEXION) ----------
    @action(detail=False, methods=['post'])
    def definir_mot_de_passe(self, request):
        """
        Permet à un utilisateur sans mot de passe de définir son mot de passe lors de sa première connexion.
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
        token = create_token(user)

        return Response({
            "message": "Mot de passe défini avec succès. Vous pouvez maintenant vous connecter.",
            "utilisateur": UtilisateurSerializer(user).data,
            "token": token
        }, status=status.HTTP_200_OK)

    # ---------- CHANGEMENT DE MOT DE PASSE ----------
    @action(detail=True, methods=['post'])
    def changer_mot_de_passe(self, request, pk=None):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ancien = serializer.validated_data['ancien_motDePasse']
        nouveau = serializer.validated_data['nouveau_motDePasse']

        # Récupérer l'utilisateur connecté depuis le thread local
        from utilisateur.middleware import get_thread_user
        current_user = get_thread_user()

        is_self = current_user and current_user.pk == user.pk

        if current_user and not is_self:
            # Vérifier la permission user:edit
            perms_perso = UtilisateurPermission.objects.filter(
                utilisateur=current_user,
                permission__nomPermission='user:edit'
            ).exists()
            perms_role = RolePermission.objects.filter(
                role=current_user.role,
                permission__nomPermission='user:edit'
            ).exists()
            if perms_perso or perms_role:
                user.set_password(nouveau)
                user.save()
                return Response({"message": "Mot de passe mis à jour avec succès"}, status=status.HTTP_200_OK)

        if not user.has_usable_password():
            return Response(
                {"detail": "Cet utilisateur n'a pas encore de mot de passe."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not user.check_password(ancien):
            return Response({"detail": "Ancien mot de passe incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(nouveau)
        user.save()
        return Response({"message": "Mot de passe mis à jour avec succès"}, status=status.HTTP_200_OK)
        
    # ---------- PERMISSIONS PERSONNALISÉES (SCRUM-159) ----------

    @action(detail=True, methods=['get'])
    def permissions(self, request, pk=None):
        """
        Retourne les permissions d'un utilisateur.
        Si des permissions personnalisées existent, elles sont retournées.
        Sinon, les permissions du rôle sont retournées.

        GET /api/utilisateurs/{id}/permissions/
        """
        user = self.get_object()
        perms_perso = user.permissions_personnalisees.select_related('permission').all()

        if perms_perso.exists():
            permissions = [up.permission for up in perms_perso]
            source = "personnalisees"
        else:
            permissions = list(user.role.permissions.all()) if user.role else []
            source = "role"

        return Response({
            "source": source,
            "permissions": PermissionSerializer(permissions, many=True).data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def definir_permissions(self, request, pk=None):
        """
        Définit les permissions personnalisées d'un utilisateur.
        Remplace toutes les permissions personnalisées existantes.

        POST /api/utilisateurs/{id}/definir_permissions/
        Body: { "permissions_ids": [1, 2, 3] }
        """
        user = self.get_object()
        permissions_ids = request.data.get('permissions_ids', [])

        if not isinstance(permissions_ids, list):
            return Response(
                {"detail": "permissions_ids doit être une liste"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier que toutes les permissions existent
        permissions = Permission.objects.filter(id__in=permissions_ids)
        if len(permissions) != len(permissions_ids):
            return Response(
                {"detail": "Une ou plusieurs permissions sont introuvables"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Supprimer les anciennes permissions personnalisées et les remplacer
        UtilisateurPermission.objects.filter(utilisateur=user).delete()
        for perm in permissions:
            UtilisateurPermission.objects.create(utilisateur=user, permission=perm)

        return Response({
            "message": f"{len(permissions)} permissions personnalisées définies pour {user.nomUtilisateur}",
            "permissions": PermissionSerializer(permissions, many=True).data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reinitialiser_permissions(self, request, pk=None):
        """
        Supprime les permissions personnalisées d'un utilisateur.
        L'utilisateur retrouve les permissions de son rôle.

        POST /api/utilisateurs/{id}/reinitialiser_permissions/
        """
        user = self.get_object()
        count = UtilisateurPermission.objects.filter(utilisateur=user).delete()[0]

        return Response({
            "message": f"Permissions personnalisées supprimées. {user.nomUtilisateur} utilise maintenant les permissions du rôle '{user.role.nomRole}'.",
            "permissions": PermissionSerializer(user.role.permissions.all(), many=True).data
        }, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'])
    def logout(self, request):

        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return Response({"detail": "Token manquant"}, status=401)

        token = auth.split(" ")[1]
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        try:
            api_token = ApiToken.objects.get(token_hash=token_hash)

            api_token.is_revoked = True
            api_token.save()

        except ApiToken.DoesNotExist:
            pass  # On ne révèle rien pour la sécurité

        return Response({"detail": "Déconnexion réussie"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def techniciens(self, request):
        """
        Retourne la liste des utilisateurs ayant le rôle de technicien.
        GET /api/utilisateurs/techniciens/
        """
        technicien_role = Role.objects.filter(nomRole__iexact='Technicien').first()
        if not technicien_role:
            return Response({"detail": "Rôle 'Technicien' introuvable"}, status=status.HTTP_404_NOT_FOUND)

        techniciens = Utilisateur.objects.filter(role=technicien_role, actif=True).order_by('nomUtilisateur')
        serializer = UtilisateurSimpleSerializer(techniciens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ==================== LOG VIEWSET ====================

class LogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Log.objects.all().order_by('-date')
    serializer_class = LogSerializer
