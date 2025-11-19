from django.db import models
from django.contrib.auth.models import User


class Intervention(models.Model):
    nomIntervention = models.CharField(max_length=500, null=True, blank=True)
    interventionCurative = models.BooleanField(null=True, blank=True)
    dateAssignation = models.DateTimeField()
    dateCloture = models.DateTimeField(null=True, blank=True)
    dateDebutIntervention = models.DateTimeField(null=True, blank=True)
    dateFinIntervention = models.DateTimeField(null=True, blank=True)
    tempsEstime = models.TimeField(null=True, blank=True)
    commentaireIntervention = models.CharField(max_length=1000, null=True, blank=True)
    commentaireRefusCloture = models.CharField(max_length=1000, null=True, blank=True)
    defaillance = models.ForeignKey('demandeIntervention.Defaillance', on_delete=models.CASCADE)
    createurIntervention = models.ForeignKey(
        User,
        related_name='createurIntervention',
        on_delete=models.CASCADE,
        help_text="La personne qui crée l'intervention"
    )
    responsable = models.ForeignKey(
        User,
        related_name='responsable',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="La personne qui réalise l'intervention"
    )

    def __str__(self):
        return self.nomIntervention or f"Intervention {self.id}"

    class Meta:
        db_table = 'gimao_intervention'


class DocumentIntervention(models.Model):
    nomDocumentIntervention = models.CharField(max_length=500)
    lienDocumentIntervention = models.FileField(upload_to='documents/documentIntervention', null=False)
    intervention = models.ForeignKey(Intervention, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomDocumentIntervention

    class Meta:
        db_table = 'gimao_documentintervention'
