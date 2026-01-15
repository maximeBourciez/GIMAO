from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from utilisateur.models import Role, Utilisateur, Log


# ==================== ROLE ====================

class RoleSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Role"""
    
    class Meta:
        model = Role
        fields = ['id', 'nomRole', 'rang']


# ==================== UTILISATEUR ====================

class UtilisateurSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Utilisateur"""
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source='role',
        write_only=True
    )
    
    class Meta:
        model = Utilisateur
        fields = [
            'id',
            'nomUtilisateur',
            'prenom',
            'nomFamille',
            'email',
            'derniereConnexion',
            'dateCreation',
            'actif',
            'role',
            'role_id'
        ]
        read_only_fields = ['derniereConnexion', 'dateCreation']


class UtilisateurCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création d'utilisateur avec mot de passe"""
    motDePasse = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        style={'input_type': 'password'},
        min_length=8
    )
    motDePasse_confirmation = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = Utilisateur
        fields = [
            'id',
            'nomUtilisateur',
            'motDePasse',
            'motDePasse_confirmation',
            'prenom',
            'nomFamille',
            'email',
            'actif',
            'role'
        ]
    
    def validate(self, data):
        """Vérifie que les mots de passe correspondent"""
        mot_de_passe = data.get('motDePasse')
        confirmation = data.get('motDePasse_confirmation')

        # Si aucun mot de passe n'est fourni, on autorise la création sans mot de passe.
        if mot_de_passe in (None, '') and confirmation in (None, ''):
            return data

        # Si l'un des deux est fourni, on exige les deux + égalité.
        if mot_de_passe in (None, '') or confirmation in (None, ''):
            raise serializers.ValidationError({
                'motDePasse_confirmation': 'Confirmation du mot de passe requise'
            })

        if mot_de_passe != confirmation:
            raise serializers.ValidationError({
                'motDePasse_confirmation': 'Les mots de passe ne correspondent pas'
            })
        return data
    
    def create(self, validated_data):
        """Crée un utilisateur avec un mot de passe hashé"""
        validated_data.pop('motDePasse_confirmation', None)

        mot_de_passe = validated_data.get('motDePasse')
        if mot_de_passe in (None, ''):
            validated_data['motDePasse'] = None
        else:
            validated_data['motDePasse'] = make_password(mot_de_passe)
        return super().create(validated_data)


class UtilisateurDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé avec logs et rôles supplémentaires"""
    role = RoleSerializer(read_only=True)
    logs_recents = serializers.SerializerMethodField()
    avoirs = serializers.SerializerMethodField()
    
    class Meta:
        model = Utilisateur
        fields = [
            'id',
            'nomUtilisateur',
            'prenom',
            'nomFamille',
            'email',
            'derniereConnexion',
            'dateCreation',
            'actif',
            'role',
            'logs_recents',
            'avoirs'
        ]
    
    def get_logs_recents(self, obj):
        """Retourne les 10 derniers logs de l'utilisateur"""
        logs = obj.logs.order_by('-date')[:10]
        return [{
            'id': log.id,
            'type': log.type,
            'nomTable': log.nomTable,
            'date': log.date
        } for log in logs]
    
    def get_avoirs(self, obj):
        """Retourne les rôles supplémentaires de l'utilisateur"""
        # Certains schémas n'ont pas de relation "avoirs" sur Utilisateur.
        # On sécurise pour éviter un 500 sur l'endpoint retrieve.
        if not hasattr(obj, 'avoirs'):
            return []

        try:
            avoirs = obj.avoirs.prefetch_related('roles').all()
        except Exception:
            return []

        return [
            {
                'id': avoir.id,
                'roles': [{'id': r.id, 'nomRole': r.nomRole} for r in avoir.roles.all()],
            }
            for avoir in avoirs
        ]


class UtilisateurSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour les relations"""
    
    class Meta:
        model = Utilisateur
        fields = ['id', 'nomUtilisateur', 'prenom', 'nomFamille', 'email']


# ==================== AUTHENTIFICATION ====================

class LoginSerializer(serializers.Serializer):
    """Serializer pour la connexion"""
    nomUtilisateur = serializers.CharField(required=True)
    motDePasse = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        style={'input_type': 'password'},
        write_only=True
    )


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer pour le changement de mot de passe"""
    ancien_motDePasse = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )
    nouveau_motDePasse = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True,
        min_length=8
    )
    nouveau_motDePasse_confirmation = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )
    
    def validate(self, data):
        """Vérifie que les nouveaux mots de passe correspondent"""
        if data['nouveau_motDePasse'] != data['nouveau_motDePasse_confirmation']:
            raise serializers.ValidationError({
                'nouveau_motDePasse_confirmation': 'Les mots de passe ne correspondent pas'
            })
        return data


class DefinirMotDePasseSerializer(serializers.Serializer):
    """Serializer pour définir un mot de passe (première connexion)"""
    nomUtilisateur = serializers.CharField(required=True)
    nouveau_motDePasse = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True,
        min_length=8
    )
    nouveau_motDePasse_confirmation = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )
    
    def validate(self, data):
        """Vérifie que les mots de passe correspondent"""
        if data['nouveau_motDePasse'] != data['nouveau_motDePasse_confirmation']:
            raise serializers.ValidationError({
                'nouveau_motDePasse_confirmation': 'Les mots de passe ne correspondent pas'
            })
        return data


# ==================== LOG ====================

class LogSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Log"""
    utilisateur = UtilisateurSimpleSerializer(read_only=True)
    utilisateur_id = serializers.PrimaryKeyRelatedField(
        queryset=Utilisateur.objects.all(),
        source='utilisateur',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Log
        fields = [
            'id',
            'type',
            'nomTable',
            'idCible',
            'champsModifies',
            'date',
            'utilisateur',
            'utilisateur_id'
        ]
        read_only_fields = ['date']