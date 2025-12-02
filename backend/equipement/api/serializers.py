from rest_framework import serializers
from equipement.models import Equipement, StatutEquipement, Constituer

from donnees.models import Lieu
from donnees.api.serializers import DocumentSerializer
from equipement.models import ModeleEquipement, Fournisseur
from equipement.models import *
from maintenance.models import DemandeIntervention, BonTravail

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


# Serializers pour affichage détaillé
class LieuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lieu
        fields = '__all__'


class ModeleEquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeleEquipement
        fields = '__all__'


class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = '__all__'


class EquipementDetailSerializer(serializers.ModelSerializer):
    lieu = LieuSerializer(read_only=True)
    modele = ModeleEquipementSerializer(read_only=True)  # ✅ modele, pas modeleEquipement
    statut = serializers.SerializerMethodField()
    
    class Meta:
        model = Equipement
        fields = '__all__'
    
    def get_statut(self, obj):
        """Retourne le statut le plus récent"""
        statut_recent = obj.statuts.order_by('-dateChangement').first() 
        if statut_recent:
            return {
                'statut': statut_recent.statut,
                'dateChangement': statut_recent.dateChangement
            }
        return None


class EquipementAvecDernierStatutSerializer(serializers.ModelSerializer):
    dernier_statut = serializers.SerializerMethodField()
    lieu = LieuSerializer(read_only=True)

    class Meta:
        model = Equipement
        fields = ['reference', 'dateCreation', 'designation', 'dateMiseEnService',
                  'prixAchat', 'preventifGlissant', 'joursIntervalleMaintenance',
                  'lieu', 'dernier_statut']

    def get_dernier_statut(self, obj):
        dernier_statut = obj.StatutEquipement_set.order_by('-dateChangement').first()
        if dernier_statut:
            return {
                'id': dernier_statut.id,
                'statutEquipement': dernier_statut.statutEquipement,
                'dateChangement': dernier_statut.dateChangement,
                'equipement': dernier_statut.equipement.reference,
                'StatutEquipementParent': dernier_statut.StatutEquipementParent.id if dernier_statut.StatutEquipementParent else None,
                'ModificateurStatut': dernier_statut.ModificateurStatut.username if dernier_statut.ModificateurStatut else None
            }
        return None


class EquipementAffichageSerializer(serializers.ModelSerializer):
    lieu = LieuSerializer(read_only=True)
    modele = ModeleEquipementSerializer(read_only=True)
    famille = serializers.StringRelatedField(read_only=True)
    createurEquipementId = serializers.IntegerField(read_only=True)

    fabricant = serializers.SerializerMethodField()
    dernier_statut = serializers.SerializerMethodField()
    
    # Nouveaux champs
    compteurs = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()
    
    liste_defaillances = serializers.SerializerMethodField()
    liste_interventions = serializers.SerializerMethodField()
    liste_consommables = serializers.SerializerMethodField()

    class Meta:
        model = Equipement
        fields = [ 'id',
            'numSerie', 'reference', 'dateCreation', 'designation',
            'dateMiseEnService', 'prixAchat', 'lienImage', 'preventifGlissant',
            'createurEquipementId', 'x', 'y',
            'lieu', 'modele', 'famille', 'fabricant',
            'dernier_statut', 'compteurs', 'documents',
            'liste_defaillances', 'liste_interventions', 'liste_consommables'
        ]

    def get_fabricant(self, obj):
        if obj.modele and obj.modele.fabricant:
            fabricant = obj.modele.fabricant
            return {
                "id": fabricant.id,
                "nomFabricant": fabricant.nom,
                "paysFabricant": fabricant.adresse.pays,
                "mailFabricant": fabricant.email,
                "numTelephoneFabricant": fabricant.numTelephone,
            }
        return None

    def get_dernier_statut(self, obj):
        if hasattr(obj, 'dernier_statut') and obj.dernier_statut:
            return {
                'id': obj.dernier_statut.id,
                'statut': obj.dernier_statut.statut,
                'dateChangement': obj.dernier_statut.dateChangement,
            }
        # Fallback si pas préfetched
        dernier_statut = obj.statuts.order_by('-dateChangement').first()
        if dernier_statut:
            return {
                'id': dernier_statut.id,
                'statut': dernier_statut.statut,
                'dateChangement': dernier_statut.dateChangement,
            }
        return None

    def get_compteurs(self, obj):
        if hasattr(obj, 'compteurs_list'):
            compteurs = obj.compteurs_list
        else:
            compteurs = obj.compteurs.all()
        
        return [
            {
                "id": compteur.id,
                "valeurCourante": compteur.valeurCourante,
                "valeurEcheance": compteur.valeurEcheance,
                "prochaineMaintenance": compteur.prochaineMaintenance,
                "ecartInterventions": compteur.ecartInterventions,
                "estGlissant": compteur.estGlissant,
                "descriptifMaintenance": compteur.descriptifMaintenance,
                "necessiteHabilitationElectrique": compteur.necessiteHabilitationElectrique,
                "necessitePermisFeu": compteur.necessitePermisFeu,
                "estPrincipal": compteur.estPrincipal,
            }
            for compteur in compteurs
        ]

    def get_documents(self, obj):
        """
        Récupère tous les documents liés à l'équipement.
        Utilise la relation ManyToMany avec préfetch.
        """
        # Si les documents sont préfetchés
        if hasattr(obj, 'documents_prefetches'):
            documents = obj.documents_prefetches
        else:
            # Fallback : charger les documents
            documents = obj.documents.all()
        
        return DocumentSerializer(documents, many=True).data

    def get_liste_defaillances(self, obj):
        if hasattr(obj, 'demandeintervention_set'):
            defaillances = obj.demandeintervention_set.all()
            return [
                {
                    "id": defaillance.id,
                    "commentaireDefaillance": defaillance.commentaireDefaillance,
                    "niveau": defaillance.niveau,
                    "utilisateur": defaillance.utilisateur.id if defaillance.utilisateur else None,
                    "equipement": defaillance.equipement.reference,
                    "dateTraitementDefaillance": defaillance.dateTraitementDefaillance
                }
                for defaillance in defaillances
            ]
        return []

    def get_liste_interventions(self, obj):
        interventions = []
        if hasattr(obj, 'demandeintervention_set'):
            for defaillance in obj.demandeintervention_set.all():
                if hasattr(defaillance, 'intervention_set'):
                    interventions.extend(defaillance.intervention_set.all())
        
        return [
            {
                "id": intervention.id,
                "nomIntervention": intervention.nomIntervention,
                "interventionCurative": intervention.interventionCurative,
                "dateAssignation": intervention.dateAssignation,
                "dateCloture": intervention.dateCloture,
                "dateDebutIntervention": intervention.dateDebutIntervention,
                "dateFinIntervention": intervention.dateFinIntervention,
                "tempsEstime": intervention.tempsEstime,
                "commentaireIntervention": intervention.commentaireIntervention,
                "commentaireRefusCloture": intervention.commentaireRefusCloture,
                "defaillance": intervention.defaillance.id,
                "createurIntervention": intervention.createurIntervention.id if intervention.createurIntervention else None,
                "responsable": intervention.responsable.id if intervention.responsable else None,
            }
            for intervention in interventions
        ]

    def get_liste_consommables(self, obj):
        # Via la relation EstCompatible du modèle
        consommables_list = []
        if obj.modele and hasattr(obj.modele, 'estcompatible_set'):
            compatibilites = obj.modele.estcompatible_set.select_related('consommable').all()
            for compatibilite in compatibilites:
                consommable = compatibilite.consommable
                consommables_list.append({
                    "id": consommable.id,
                    "designation": consommable.designation,
                    "lienImageConsommable": consommable.lienImageConsommable.url if consommable.lienImageConsommable else None,
                    "magasin": {
                        "id": consommable.magasin.id,
                        "nom": consommable.magasin.nom,
                        "estMobile": consommable.magasin.estMobile,
                    } if consommable.magasin else None,
                    "seuilStockFaible": consommable.seuilStockFaible,
                    "compatibilite_id": compatibilite.id
                })
        
        # Ajouter aussi via la relation Constituer directe
        if hasattr(obj, 'constituer_set'):
            constituer_relations = obj.constituer_set.select_related('consommable__magasin').all()
            for relation in constituer_relations:
                consommable = relation.consommable
                # Éviter les doublons
                if not any(c["id"] == consommable.id for c in consommables_list):
                    consommables_list.append({
                        "id": consommable.id,
                        "designation": consommable.designation,
                        "lienImageConsommable": consommable.lienImageConsommable.url if consommable.lienImageConsommable else None,
                        "magasin": {
                            "id": consommable.magasin.id,
                            "nom": consommable.magasin.nom,
                            "estMobile": consommable.magasin.estMobile,
                        } if consommable.magasin else None,
                        "seuilStockFaible": consommable.seuilStockFaible,
                        "constituer_id": relation.id
                    })
        
        return consommables_list

    def get_liste_documents(self, obj):
        return self.get_documents(obj)  


class DocumentEquipementSerializer(serializers.ModelSerializer):
    document_details = DocumentSerializer(source='document', read_only=True)
    uploader_username = serializers.CharField(source='uploader.username', read_only=True)
    
    class Meta:
        model = DocumentEquipement
        fields = [
            'id', 'document', 'document_details', 'date_ajout', 
            'type_document', 'commentaire', 'uploader', 'uploader_username', 'est_public'
        ]