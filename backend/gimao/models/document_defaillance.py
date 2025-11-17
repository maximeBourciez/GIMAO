from django.db import models
from .defaillance import Defaillance

class DocumentDefaillance(models.Model):
    nomDocumentDefaillance = models.CharField(max_length=50)
    lienDocumentDefaillance = models.FileField(upload_to='documents/documentDefaillance', null=False) 
    defaillance = models.ForeignKey(Defaillance, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomDocumentDefaillance