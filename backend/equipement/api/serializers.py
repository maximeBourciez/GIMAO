from rest_framework import serializers
from equipement.models import Equipement, StatutEquipement, Constituer, ModeleEquipement, Compteur, FamilleEquipement
from donnees.api.serializers import LieuSerializer
from donnees.models import Document
from maintenance.models import DemandeIntervention, BonTravail

class EquipementSerializer(serializers.ModelSerializer):
    # Fetcg le dernier statut de l'équipement
    statut = serializers.SerializerMethodField() 
    lieu = LieuSerializer(read_only=True)  
    
    def get_statut(self, obj):
        statut = obj.statuts.order_by('-dateChangement').first()
        if statut:
            return {
                'id': statut.id,
                'statut': statut.statut,
                'dateChangement': statut.dateChangement
            }
        return None
    
    def get_lieu(self, obj):
        if obj.lieu:
            return {
                'id': obj.lieu.id,
                'nomLieu': obj.lieu.nomLieu,
                'typeLieu': obj.lieu.typeLieu
            }
        return None
    
    class Meta:
        model = Equipement
        fields = '__all__'

class EquipementAffichageSerializer(serializers.ModelSerializer):
    """Serializer pour l'affichage détaillé d'un équipement"""
    lieu = LieuSerializer(read_only=True)
    modele = serializers.SerializerMethodField()
    famille = serializers.SerializerMethodField()
    dernier_statut = serializers.SerializerMethodField()
    compteurs = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()
    consommables = serializers.SerializerMethodField()
    bons_travail = serializers.SerializerMethodField()

    class Meta:
        model = Equipement
        fields = [
            'id', 'numSerie', 'reference', 'dateCreation', 'designation',
            'dateMiseEnService', 'prixAchat', 'lienImage', 'preventifGlissant',
            'createurEquipementId', 'x', 'y',
            'lieu', 'modele', 'famille', 'dernier_statut',
            'compteurs', 'documents', 'consommables', 'bons_travail'
        ]

    def get_modele(self, obj):
        if obj.modele:
            return {
                'id': obj.modele.id,
                'nom': obj.modele.nom,
                'fabricant': {
                    'id': obj.modele.fabricant.id,
                    'nom': obj.modele.fabricant.nom,
                    'email': obj.modele.fabricant.email
                } if obj.modele.fabricant else None
            }
        return None

    def get_famille(self, obj):
        if obj.famille:
            return {
                'id': obj.famille.id,
                'nom': obj.famille.nom
            }
        return None

    def get_dernier_statut(self, obj):
        statut = obj.statuts.order_by('-dateChangement').first()
        if statut:
            return {
                'id': statut.id,
                'statut': statut.statut,
                'dateChangement': statut.dateChangement
            }
        return None

    def get_compteurs(self, obj):
        return [
            {
                'id': c.id,
                'nomCompteur': c.nomCompteur,
                'valeurCourante': c.valeurCourante,
                'valeurEcheance': c.valeurEcheance,
                'prochaineMaintenance': c.prochaineMaintenance,
                'estPrincipal': c.estPrincipal
            }
            for c in obj.compteurs.all()
        ]

    def get_documents(self, obj):
        return [
            {
                'id': d.id,
                'nomDocument': d.nomDocument if hasattr(d, 'nomDocument') else '',
                'cheminAcces': d.cheminAcces if hasattr(d, 'cheminAcces') else '',
                'typeDocument': d.typeDocument.nomTypeDocument if hasattr(d, 'typeDocument') else ''

            }
            for d in obj.documents.all()
        ]

    def get_consommables(self, obj):
        relations = Constituer.objects.filter(equipement=obj).select_related('consommable')
        return [
            {
                'id': r.consommable.id,
                'designation': r.consommable.designation,
                'fabricant': r.consommable.fabricant.nom if r.consommable.fabricant else None,
            }
            for r in relations
        ]

    def get_bons_travail(self, obj):
        bons = BonTravail.objects.filter(equipement=obj).select_related('responsable', 'demande_intervention')
        return [
            {
                'id': bon.id,
                'nom': bon.nom,
                'diagnostic': bon.diagnostic,
                'type': bon.type,
                'statut': bon.statut,
                'date_assignation': bon.date_assignation,
                'date_fin': bon.date_fin,
                'date_cloture': bon.date_cloture,
            }
            for bon in bons
        ]


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
