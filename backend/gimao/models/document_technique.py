from django.db import models

class DocumentTechnique(models.Model):
    nomDocumentTechnique = models.CharField(max_length=50)
    lienDocumentTechnique = models.FileField(upload_to='documents/documentTecnique', null=False) 

    def __str__(self):
        return self.nomDocumentTechnique