from rest_framework import serializers
from demandeIntervention.models import Defaillance, DocumentDefaillance
from equipement.api.serializers import EquipementAvecDernierStatutSerializer
from bonTravail.models import Intervention, DocumentIntervention


class DefaillanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defaillance
        fields = '__all__'


class DocumentDefaillanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentDefaillance
        fields = '__all__'


class DefaillanceAfficherSerializer(serializers.ModelSerializer):
    """Serializer pour l'affichage détaillé d'une défaillance avec tous ses documents et intervention associée"""
    liste_documents_defaillance = serializers.SerializerMethodField()
    equipement = EquipementAvecDernierStatutSerializer()
    intervention = serializers.SerializerMethodField()

    class Meta:
        model = Defaillance
        fields = [
            'id', 'commentaireDefaillance', 'niveau', 'dateTraitementDefaillance',
            'utilisateur', 'equipement', 'liste_documents_defaillance', 'intervention'
        ]
        depth = 1

    def get_liste_documents_defaillance(self, obj):
        documents_defaillance = DocumentDefaillance.objects.filter(defaillance=obj)
        return [
            {
                "id": doc.id,
                "nomDocumentDefaillance": doc.nomDocumentDefaillance,
                "lienDocumentDefaillance": doc.lienDocumentDefaillance.url if doc.lienDocumentDefaillance else None,
            }
            for doc in documents_defaillance
        ]

    def get_intervention(self, obj):
        intervention = Intervention.objects.filter(defaillance=obj).first()
        if intervention:
            return {
                "id": intervention.id,
                "nomIntervention": intervention.nomIntervention,
                "interventionCurative": intervention.interventionCurative,
                "dateAssignation": intervention.dateAssignation,
                "dateCloture": intervention.dateCloture,
                "dateDebutIntervention": intervention.dateDebutIntervention,
                "dateFinIntervention": intervention.dateFinIntervention,
                "tempsEstime": str(intervention.tempsEstime),
                "commentaireIntervention": intervention.commentaireIntervention,
                "commentaireRefusCloture": intervention.commentaireRefusCloture,
                "defaillance": intervention.defaillance.id,
                "createurIntervention": intervention.createurIntervention.id if intervention.createurIntervention else None,
                "responsable": intervention.responsable.id if intervention.responsable else None
            }
        return None
