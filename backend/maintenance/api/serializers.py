from rest_framework import serializers
from maintenance.models import (
    DemandeIntervention,
    BonTravail,
    TypePlanMaintenance,
    PlanMaintenance,
    PlanMaintenanceConsommable
)
from equipement.models import Equipement, Compteur
from utilisateur.models import Utilisateur
from stock.models import Consommable
from donnees.models import Document


# ==================== SERIALIZERS SIMPLES ====================

class UtilisateurSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour Utilisateur"""
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'prenom', 'nom']


class EquipementSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour Equipement"""
    class Meta:
        model = Equipement
        fields = ['id', 'reference', 'designation', 'numSerie']


class ConsommableSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour Consommable"""
    class Meta:
        model = Consommable
        fields = ['id', 'designation']


class DocumentSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour Document"""
    class Meta:
        model = Document
        fields = ['id', 'nomDocument', 'cheminAcces']


class CompteurSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour Compteur"""
    class Meta:
        model = Compteur
        fields = ['id', 'valeurCourante', 'valeurEcheance', 'estPrincipal']


# ==================== DEMANDE INTERVENTION ====================

class DemandeInterventionSerializer(serializers.ModelSerializer):
    """Serializer pour DemandeIntervention"""
    utilisateur = UtilisateurSimpleSerializer(read_only=True)
    equipement = EquipementSimpleSerializer(read_only=True)
    
    utilisateur_id = serializers.PrimaryKeyRelatedField(
        queryset=Utilisateur.objects.all(),
        source='utilisateur',
        write_only=True
    )
    equipement_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipement.objects.all(),
        source='equipement',
        write_only=True
    )
    
    class Meta:
        model = DemandeIntervention
        fields = [
            'id',
            'nom',
            'commentaire',
            'date_traitement',
            'date_commencement',
            'utilisateur',
            'equipement',
            'utilisateur_id',
            'equipement_id'
        ]


class DemandeInterventionDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé avec les bons de travail"""
    utilisateur = UtilisateurSimpleSerializer(read_only=True)
    equipement = EquipementSimpleSerializer(read_only=True)
    bons_travail = serializers.SerializerMethodField()
    
    class Meta:
        model = DemandeIntervention
        fields = [
            'id',
            'nom',
            'commentaire',
            'date_traitement',
            'date_commencement',
            'utilisateur',
            'equipement',
            'bons_travail'
        ]
    
    def get_bons_travail(self, obj):
        bons = obj.bons_travail.all()
        return [{
            'id': bon.id,
            'nom': bon.nom,
            'type': bon.type,
            'statut': bon.statut,
            'date_assignation': bon.date_assignation,
            'date_cloture': bon.date_cloture
        } for bon in bons]


# ==================== BON TRAVAIL ====================

class BonTravailSerializer(serializers.ModelSerializer):
    """Serializer pour BonTravail"""
    demande_intervention = serializers.PrimaryKeyRelatedField(
        queryset=DemandeIntervention.objects.all()
    )
    responsable = UtilisateurSimpleSerializer(read_only=True)
    utilisateur_assigne = UtilisateurSimpleSerializer(many=True, read_only=True)
    
    responsable_id = serializers.PrimaryKeyRelatedField(
        queryset=Utilisateur.objects.all(),
        source='responsable',
        write_only=True,
        required=False,
        allow_null=True
    )
    utilisateur_assigne_ids = serializers.PrimaryKeyRelatedField(
        queryset=Utilisateur.objects.all(),
        source='utilisateur_assigne',
        write_only=True,
        many=True,
        required=False
    )
    
    class Meta:
        model = BonTravail
        fields = [
            'id',
            'nom',
            'diagnostic',
            'type',
            'date_assignation',
            'date_cloture',
            'date_debut',
            'date_fin',
            'date_prevue',
            'statut',
            'commentaire',
            'commentaire_refus_cloture',
            'demande_intervention',
            'responsable',
            'utilisateur_assigne',
            'responsable_id',
            'utilisateur_assigne_ids'
        ]


class BonTravailDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour BonTravail"""
    demande_intervention = DemandeInterventionSerializer(read_only=True)
    responsable = UtilisateurSimpleSerializer(read_only=True)
    utilisateur_assigne = UtilisateurSimpleSerializer(many=True, read_only=True)
    
    class Meta:
        model = BonTravail
        fields = [
            'id',
            'nom',
            'diagnostic',
            'type',
            'date_assignation',
            'date_cloture',
            'date_debut',
            'date_fin',
            'date_prevue',
            'statut',
            'commentaire',
            'commentaire_refus_cloture',
            'demande_intervention',
            'responsable',
            'utilisateur_assigne'
        ]


# ==================== TYPE PLAN MAINTENANCE ====================

class TypePlanMaintenanceSerializer(serializers.ModelSerializer):
    """Serializer pour TypePlanMaintenance"""
    class Meta:
        model = TypePlanMaintenance
        fields = ['id', 'libelle']


# ==================== PLAN MAINTENANCE ====================

class PlanMaintenanceConsommableSerializer(serializers.ModelSerializer):
    """Serializer pour la table d'association"""
    consommable = ConsommableSimpleSerializer(read_only=True)
    consommable_id = serializers.PrimaryKeyRelatedField(
        queryset=Consommable.objects.all(),
        source='consommable',
        write_only=True
    )
    
    class Meta:
        model = PlanMaintenanceConsommable
        fields = [
            'id',
            'consommable',
            'consommable_id',
            'quantite_necessaire'
        ]


class PlanMaintenanceSerializer(serializers.ModelSerializer):
    """Serializer pour PlanMaintenance"""
    type_plan_maintenance = TypePlanMaintenanceSerializer(read_only=True)
    equipement = EquipementSimpleSerializer(read_only=True)
    compteur = CompteurSimpleSerializer(read_only=True)
    
    type_plan_maintenance_id = serializers.PrimaryKeyRelatedField(
        queryset=TypePlanMaintenance.objects.all(),
        source='type_plan_maintenance',
        write_only=True
    )
    equipement_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipement.objects.all(),
        source='equipement',
        write_only=True
    )
    compteur_id = serializers.PrimaryKeyRelatedField(
        queryset=Compteur.objects.all(),
        source='compteur',
        write_only=True
    )
    
    class Meta:
        model = PlanMaintenance
        fields = [
            'id',
            'nom',
            'contenu',
            'type_plan_maintenance',
            'equipement',
            'compteur',
            'type_plan_maintenance_id',
            'equipement_id',
            'compteur_id'
        ]


class PlanMaintenanceDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé avec consommables et documents"""
    type_plan_maintenance = TypePlanMaintenanceSerializer(read_only=True)
    equipement = EquipementSimpleSerializer(read_only=True)
    compteur = CompteurSimpleSerializer(read_only=True)
    documents = DocumentSimpleSerializer(many=True, read_only=True)
    consommables_necessaires = serializers.SerializerMethodField()
    
    class Meta:
        model = PlanMaintenance
        fields = [
            'id',
            'nom',
            'contenu',
            'type_plan_maintenance',
            'equipement',
            'compteur',
            'documents',
            'consommables_necessaires'
        ]
    
    def get_consommables_necessaires(self, obj):
        associations = PlanMaintenanceConsommable.objects.filter(
            plan_maintenance=obj
        ).select_related('consommable')
        return [{
            'id': assoc.consommable.id,
            'designation': assoc.consommable.designation,
            'quantite_necessaire': assoc.quantite_necessaire
        } for assoc in associations]