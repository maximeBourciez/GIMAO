from rest_framework import serializers
from maintenance.models import (
    DemandeIntervention,
    BonTravail,
    TypePlanMaintenance,
    PlanMaintenance,
    PlanMaintenanceConsommable
)
from equipement.models import Equipement, Compteur, StatutEquipement
from utilisateur.models import Utilisateur
from stock.models import Consommable
from donnees.models import Document
from donnees.api.serializers import DocumentSerializer


# ==================== SERIALIZERS SIMPLES ====================

class UtilisateurSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour Utilisateur"""
    class Meta:
        model = Utilisateur
        fields = ['id', 'nomUtilisateur', 'email', 'prenom', 'nomFamille']
        ref_name = 'MaintenanceUtilisateurSimple'


class EquipementSimpleSerializer(serializers.ModelSerializer):
    lieu = serializers.CharField(source='lieu.nomLieu')
    dernier_statut = serializers.SerializerMethodField()

    class Meta:
        model = Equipement
        fields = ['id', 'reference', 'designation', 'lieu', 'dernier_statut']
        ref_name = 'EquipementSimpleSerializer'

    def get_dernier_statut(self, obj):
        statut = obj.statuts.order_by('-dateChangement').first()
        if statut:
            return {
                'id': statut.id,
                'statut': statut.statut,
                'dateChangement': statut.dateChangement
            }
        return None

class ConsommableSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour Consommable"""
    class Meta:
        model = Consommable
        fields = ['id', 'designation']
        ref_name = 'MaintenanceConsommableSimple'


class DocumentSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour Document"""
    class Meta:
        model = Document
        fields = ['id', 'nomDocument', 'cheminAcces']
        ref_name = 'MaintenanceDocumentSimple'


class CompteurSimpleSerializer(serializers.ModelSerializer):
    """Serializer simple pour Compteur"""
    class Meta:
        model = Compteur
        fields = ['id', 'nomCompteur', 'valeurCourante']
        ref_name = 'MaintenanceCompteurSimple'


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
            'statut',
            'date_creation',
            'date_changementStatut',
            'equipement',
            'utilisateur',
            'utilisateur_id',
            'equipement_id'
        ]
        read_only_fields = ['id', 'date_creation', 'date_changementStatut', 'statut']

    def create(self, validated_data):
        from django.utils import timezone
        
        validated_data['date_creation'] = timezone.now()
        validated_data['date_changementStatut'] = timezone.now()
        validated_data['statut'] = 'EN_ATTENTE'
            
        return super().create(validated_data)


class DemandeInterventionDetailSerializer(DemandeInterventionSerializer):
    """Serializer détaillé avec les documents et le bon de travail"""
    documentsDI = DocumentSerializer(source='documents', many=True, read_only=True)
    

    class Meta(DemandeInterventionSerializer.Meta):
        fields = DemandeInterventionSerializer.Meta.fields + [
            'documentsDI'
        ]


# ==================== BON TRAVAIL ====================

class BonTravailSerializer(serializers.ModelSerializer):
    """Serializer pour BonTravail"""
    demande_intervention = serializers.PrimaryKeyRelatedField(
        queryset=DemandeIntervention.objects.all()
    )
    equipement_designation = serializers.CharField(
        source='demande_intervention.equipement.designation',
        read_only=True
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
            'equipement_designation',
            'responsable',
            'utilisateur_assigne',
            'responsable_id',
            'utilisateur_assigne_ids'
        ]


class BonTravailDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour BonTravail"""
    demande_intervention = DemandeInterventionDetailSerializer(read_only=True)
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
            'commentaire',
            'type_plan_maintenance',
            'equipement',
            'compteur',
            'type_plan_maintenance_id',
            'equipement_id',
            'compteur_id'
        ]


class PlanMaintenanceDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé avec consommables et documents"""
    type = serializers.IntegerField(
        source='type_plan_maintenance.id',
        read_only=True
    )
    documents = DocumentSerializer(many=True, read_only=True)
    consommables = serializers.SerializerMethodField()
    
    class Meta:
        model = PlanMaintenance
        fields = [
            'id',
            'nom',
            'type',
            'documents',
            'consommables'
        ]
    
    def get_consommables(self, obj):
        associations = PlanMaintenanceConsommable.objects.filter(
            plan_maintenance=obj
        ).select_related('consommable')
        return [{
            'consommable': assoc.consommable.id,
            'quantite': assoc.quantite_necessaire
        } for assoc in associations]