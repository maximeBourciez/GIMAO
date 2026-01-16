from rest_framework import serializers
from equipement.models import Equipement, StatutEquipement, Constituer, ModeleEquipement, Compteur, FamilleEquipement
from donnees.api.serializers import LieuSerializer, FabricantSimpleSerializer, FournisseurSimpleSerializer
from maintenance.models import DemandeIntervention, BonTravail, PlanMaintenance
from stock.models import PorterSur

from maintenance.api.serializers import PlanMaintenanceDetailSerializer


class EquipementSerializer(serializers.ModelSerializer):
    # Fetcg le dernier statut de l'équipement
    statut = serializers.SerializerMethodField() 
    modele = serializers.CharField(source='modele.nom', read_only=True)
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


class StatutEquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatutEquipement
        fields = '__all__'


class ConstituerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constituer
        fields = '__all__'


class ModeleEquipementSerializer(serializers.ModelSerializer):
    fabricant = FabricantSimpleSerializer(read_only=True)
    class Meta:
        model = ModeleEquipement
        fields = '__all__'


class CompteurSerializer(serializers.ModelSerializer):
    planMaintenance = PlanMaintenanceDetailSerializer(read_only=True)

    nom = serializers.CharField(source='nomCompteur', read_only=True)
    description = serializers.CharField(source='descriptifMaintenance', read_only=True)
    intervalle = serializers.IntegerField(source='ecartInterventions', read_only=True)

    class Meta:
        model = Compteur
        fields = [
            'id',
            'nom',
            'description',
            'valeurCourante',
            'intervalle',
            'derniereIntervention',
            'prochaineMaintenance',
            'unite',
            'estPrincipal',
            'estGlissant',
            'necessiteHabilitationElectrique',
            'necessitePermisFeu',
            'planMaintenance',
        ]


class FamilleEquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilleEquipement
        fields = '__all__'


class EquipementCreateSerializer(serializers.ModelSerializer):
    createurEquipement = serializers.IntegerField()
    lieu = serializers.IntegerField()
    modeleEquipement = serializers.IntegerField()
    fournisseur = serializers.IntegerField()
    fabricant = serializers.IntegerField()

    consommables = serializers.ListField(child=serializers.IntegerField(), required=False)
    compteurs = serializers.JSONField(required=False)

    lienImageEquipement = serializers.ImageField(required=False)

    class Meta:
        model = Equipement
        fields = [
            'reference', 'designation', 'dateCreation', 'dateMiseEnService',
            'prixAchat', 'createurEquipement', 'lieu', 'modeleEquipement',
            'fournisseur', 'fabricant', 'consommables', 'numSerie',
            'compteurs', 'lienImageEquipement'
        ]




class EquipementAffichageSerializer(serializers.ModelSerializer):
    """Serializer pour l'affichage détaillé d'un équipement"""
    lieu = LieuSerializer(read_only=True)
    modele = ModeleEquipementSerializer(read_only=True)
    famille = serializers.SerializerMethodField()
    dernier_statut = serializers.SerializerMethodField()
    compteurs = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()
    consommables = serializers.SerializerMethodField()
    bons_travail = serializers.SerializerMethodField()
    fabricant = FabricantSimpleSerializer(read_only=True)
    fournisseur = FournisseurSimpleSerializer(read_only=True)
    createurEquipement = serializers.CharField(source='createurEquipement.nom', read_only=True)
    lienImage = serializers.SerializerMethodField()

    class Meta:
        model = Equipement
        fields = [
            'id', 'numSerie', 'reference', 'dateCreation', 'designation',
            'dateMiseEnService', 'prixAchat', 'lienImage',
            'createurEquipement', 'x', 'y', 'fabricant', 'fournisseur',
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
        compteurs_data = []
        
        for c in obj.compteurs.all():
            plan_maintenance = None
            
            # Récupérer le plan de maintenance lié à ce compteur (s'il existe)
            if c.planMaintenance:
                # Récupérer les consommables avec leurs quantités
                consommables = []
                docs = []
                relations_conso = c.planMaintenance.planmaintenanceconsommable_set.all().select_related('consommable')
                relations_docs = c.planMaintenance.planmaintenancedocument_set.all().select_related('document')

                # Récupération des consommables 
                for rel_conso in relations_conso:
                    consommables.append({
                        'consommable': rel_conso.consommable.id,
                        'quantite': rel_conso.quantite_necessaire
                    })

                # Récupération des infos des documents (pas du fichier)
                for rel_doc in relations_docs:
                    docs.append({
                        'id': rel_doc.document.id,
                        'titre': rel_doc.document.nomDocument,
                        'path': rel_doc.document.cheminAcces.name,
                        'type': rel_doc.document.typeDocument_id
                    })
                
                plan_maintenance = {
                    'id': c.planMaintenance.id,
                    'nom': c.planMaintenance.nom,
                    'type': c.planMaintenance.type_plan_maintenance_id,
                    'consommables': consommables,
                    'documents': docs
                }
            
            compteur_dict = {
                'id': c.id,
                'nom': c.nomCompteur,
                'valeurCourante': c.valeurCourante,
                'intervalle': c.ecartInterventions,
                'derniereIntervention': c.derniereIntervention,
                'prochaineMaintenance': c.prochaineMaintenance,
                'unite': c.unite,
                'estPrincipal': c.estPrincipal,
                'estGlissant': c.estGlissant,
                'planMaintenance': plan_maintenance  
            }
            
            compteurs_data.append(compteur_dict)
        
        return compteurs_data

    def get_documents(self, obj):
        docs_Pm = PlanMaintenance.objects.filter(
            equipement=obj
        ).prefetch_related('documents')
        documents_list = []
        for pm in docs_Pm:
            for doc in pm.documents.all():
                documents_list.append({
                    'id': doc.id,
                    'titre': doc.nomDocument,
                    'path': doc.cheminAcces.name,
                    'type': doc.typeDocument_id
                })
        return documents_list

    def get_consommables(self, obj):
        # Récupère tous les consommables liés à cet équipement
        relations = Constituer.objects.filter(equipement=obj).select_related('consommable')
        
        consommables_list = []
        for r in relations:
            consommable = r.consommable
            
            fabricant = consommable.fournitures.values_list('fabricant__nom', flat=True).first()
            
            consommables_list.append({
                'id': consommable.id,
                'designation': consommable.designation,
                'fabricant': fabricant if fabricant else None
            })
        
        return consommables_list


    def get_bons_travail(self, obj):
        bons = BonTravail.objects.filter(
            demande_intervention__equipement=obj
        ).select_related(
            'responsable',
            'demande_intervention',
            'demande_intervention__equipement'
        )
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
    

    def get_lienImage(self, obj):
        """Retourne le nom du fichier ou l'URL complète"""
        if obj.lienImage:
            return obj.lienImage.name  
        return None


