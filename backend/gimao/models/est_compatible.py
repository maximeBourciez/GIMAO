from django.db import models
from .consommable import Consommable
from .modele_equipement import ModeleEquipement

class EstCompatible(models.Model):
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE)
    modeleEquipement = models.ForeignKey(ModeleEquipement, on_delete=models.CASCADE)
