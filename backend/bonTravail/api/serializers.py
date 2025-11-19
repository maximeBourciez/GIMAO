from rest_framework import serializers
from bonTravail.models import Intervention, DocumentIntervention


class InterventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intervention
        fields = '__all__'


class DocumentInterventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentIntervention
        fields = '__all__'


class InterventionAfficherSerializer(serializers.ModelSerializer):
    """Serializer pour l'affichage détaillé d'une intervention avec tous ses documents"""
    liste_documents_intervention = serializers.SerializerMethodField()

    class Meta:
        model = Intervention
        fields = [
            'id', 'nomIntervention', 'interventionCurative', 'dateAssignation',
            'dateCloture', 'dateDebutIntervention', 'dateFinIntervention',
            'tempsEstime', 'commentaireIntervention', 'commentaireRefusCloture',
            'defaillance', 'createurIntervention', 'responsable',
            'liste_documents_intervention'
        ]
        depth = 1

    def get_liste_documents_intervention(self, obj):
        documents_intervention = DocumentIntervention.objects.filter(intervention=obj)
        return [
            {
                "id": doc.id,
                "nomDocumentIntervention": doc.nomDocumentIntervention,
                "lienDocumentIntervention": doc.lienDocumentIntervention.url if doc.lienDocumentIntervention else None,
            }
            for doc in documents_intervention
        ]
