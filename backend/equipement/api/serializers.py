from rest_framework import serializers
from equipement.models import Equipement, InformationStatut, Constituer
from gestionDonnee.models import Lieu, ModeleEquipement, Fournisseur, Fabricant, Correspondre
from demandeIntervention.models import Defaillance, DocumentDefaillance
from bonTravail.models import Intervention, DocumentIntervention


class EquipementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipement
        fields = '__all__'


class InformationStatutSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationStatut
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
    modeleEquipement = ModeleEquipementSerializer(read_only=True)
    statut = serializers.SerializerMethodField()

    class Meta:
        model = Equipement
        fields = ['reference', 'dateCreation', 'designation', 'dateMiseEnService',
                  'prixAchat', 'lienImageEquipement', 'preventifGlissant',
                  'joursIntervalleMaintenance', 'createurEquipement',
                  'lieu', 'modeleEquipement', 'fournisseur', 'statut']

    def get_statut(self, obj):
        dernier_statut = obj.informationstatut_set.order_by('-dateChangement').first()
        if dernier_statut:
            return InformationStatutSerializer(dernier_statut).data
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
        dernier_statut = obj.informationstatut_set.order_by('-dateChangement').first()
        if dernier_statut:
            return {
                'id': dernier_statut.id,
                'statutEquipement': dernier_statut.statutEquipement,
                'dateChangement': dernier_statut.dateChangement,
                'equipement': dernier_statut.equipement.reference,
                'informationStatutParent': dernier_statut.informationStatutParent.id if dernier_statut.informationStatutParent else None,
                'ModificateurStatut': dernier_statut.ModificateurStatut.username if dernier_statut.ModificateurStatut else None
            }
        return None


class EquipementAffichageSerializer(serializers.ModelSerializer):
    lieu = LieuSerializer(read_only=True)
    modeleEquipement = ModeleEquipementSerializer(read_only=True)
    fournisseur = FournisseurSerializer(read_only=True)

    fabricant = serializers.SerializerMethodField()
    dernier_statut = serializers.SerializerMethodField()

    liste_defaillances = serializers.SerializerMethodField()
    liste_interventions = serializers.SerializerMethodField()
    liste_consommables = serializers.SerializerMethodField()

    liste_documents_techniques = serializers.SerializerMethodField()
    liste_documents_defaillance = serializers.SerializerMethodField()
    liste_documents_intervention = serializers.SerializerMethodField()

    class Meta:
        model = Equipement
        fields = [
            'reference', 'dateCreation', 'designation', 'dateMiseEnService',
            'prixAchat', 'lienImageEquipement',
            'preventifGlissant', 'joursIntervalleMaintenance', 'createurEquipement',
            'lieu', 'modeleEquipement', 'fournisseur',
            'fabricant', 'dernier_statut',
            'liste_defaillances', 'liste_interventions', 'liste_consommables',
            'liste_documents_techniques', 'liste_documents_defaillance', 'liste_documents_intervention'
        ]

    def get_fabricant(self, obj):
        if obj.modeleEquipement and obj.modeleEquipement.fabricant:
            fabricant = obj.modeleEquipement.fabricant
            return {
                "id": fabricant.id,
                "nomFabricant": fabricant.nomFabricant,
                "paysFabricant": fabricant.paysFabricant,
                "mailFabricant": fabricant.mailFabricant,
                "numTelephoneFabricant": fabricant.numTelephoneFabricant,
            }
        return None

    def get_dernier_statut(self, obj):
        dernier_statut = obj.informationstatut_set.order_by('-dateChangement').first()
        if dernier_statut:
            return {
                'id': dernier_statut.id,
                'statutEquipement': dernier_statut.statutEquipement,
                'dateChangement': dernier_statut.dateChangement,
                'equipement': dernier_statut.equipement.reference,
                'informationStatutParent': dernier_statut.informationStatutParent.id if dernier_statut.informationStatutParent else None,
                'ModificateurStatut': dernier_statut.ModificateurStatut.username if dernier_statut.ModificateurStatut else None
            }
        return None

    def get_liste_defaillances(self, obj):
        defaillances = Defaillance.objects.filter(equipement=obj)
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

    def get_liste_interventions(self, obj):
        interventions = Intervention.objects.filter(
            defaillance__equipement=obj
        ).select_related('defaillance', 'createurIntervention', 'responsable')
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
        constituer_relations = Constituer.objects.filter(
            equipement=obj
        ).select_related('consommable__fabricant')
        return [
            {
                "id": relation.consommable.id,
                "designation": relation.consommable.designation,
                "lienImageConsommable": relation.consommable.lienImageConsommable.url if relation.consommable.lienImageConsommable else None,
                "fabricant": {
                    "id": relation.consommable.fabricant.id,
                    "nomFabricant": relation.consommable.fabricant.nomFabricant,
                    "paysFabricant": relation.consommable.fabricant.paysFabricant,
                    "mailFabricant": relation.consommable.fabricant.mailFabricant,
                    "numTelephoneFabricant": relation.consommable.fabricant.numTelephoneFabricant,
                } if relation.consommable.fabricant else None,
                "constituer_id": relation.id
            }
            for relation in constituer_relations
        ]

    def get_liste_documents_techniques(self, obj):
        correspondances = Correspondre.objects.filter(
            modeleEquipement=obj.modeleEquipement
        ).select_related('documentTechnique')
        return [
            {
                "id": correspondance.documentTechnique.id,
                "nomDocumentTechnique": correspondance.documentTechnique.nomDocumentTechnique,
                "lienDocumentTechnique": correspondance.documentTechnique.lienDocumentTechnique.url if correspondance.documentTechnique.lienDocumentTechnique else None
            }
            for correspondance in correspondances
        ]

    def get_liste_documents_defaillance(self, obj):
        documents_defaillance = DocumentDefaillance.objects.filter(defaillance__equipement=obj)
        return [
            {
                "id": doc.id,
                "nomDocumentDefaillance": doc.nomDocumentDefaillance,
                "lienDocumentDefaillance": doc.lienDocumentDefaillance.url if doc.lienDocumentDefaillance else None,
                "defaillance": doc.defaillance.id
            }
            for doc in documents_defaillance
        ]

    def get_liste_documents_intervention(self, obj):
        documents_intervention = DocumentIntervention.objects.filter(
            intervention__defaillance__equipement=obj
        ).select_related('intervention')

        return [
            {
                "id": doc.id,
                "nomDocumentIntervention": doc.nomDocumentIntervention,
                "lienDocumentIntervention": doc.lienDocumentIntervention.url if doc.lienDocumentIntervention else None,
                "intervention": doc.intervention.id
            }
            for doc in documents_intervention
        ]
