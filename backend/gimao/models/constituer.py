from django.db import models
from .consommable import Consommable
from .equipement import Equipement

class Constituer(models.Model):
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE)
