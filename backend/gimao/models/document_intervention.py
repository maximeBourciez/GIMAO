from django.db import models
from .intervention import Intervention

class DocumentIntervention(models.Model):
    nomDocumentIntervention = models.CharField(max_length=500)
    lienDocumentIntervention = models.FileField(upload_to='documents/documentIntervention', null=False) 
    intervention = models.ForeignKey(Intervention, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomDocumentIntervention
