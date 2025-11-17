from django.db import models
from .fabricant import Fabricant

class Consommable(models.Model):
    designation = models.CharField(max_length=50)
    lienImageConsommable = models.ImageField(upload_to='images/consomable', null=False) 
    fabricant = models.ForeignKey(Fabricant, on_delete=models.CASCADE)

    def __str__(self):
        return self.designation