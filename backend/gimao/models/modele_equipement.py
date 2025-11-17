from django.db import models
from .fabricant import Fabricant

class ModeleEquipement(models.Model):
    nomModeleEquipement = models.CharField(max_length=50)
    fabricant = models.ForeignKey(Fabricant, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomModeleEquipement