from django.db import models
from .document_technique import DocumentTechnique
from .modele_equipement import ModeleEquipement

class Correspondre(models.Model):
    documentTechnique = models.ForeignKey(DocumentTechnique, on_delete=models.CASCADE)
    modeleEquipement = models.ForeignKey(ModeleEquipement, on_delete=models.CASCADE)
