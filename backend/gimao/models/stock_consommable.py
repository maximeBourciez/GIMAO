from django.db import models
from .consommable import Consommable
from .fournisseur import Fournisseur

class StockConsommable(models.Model):
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    prixAchat = models.DecimalField(max_digits=7, decimal_places=2)
    dateAchat = models.DateField()
    quantiteConsommable = models.SmallIntegerField()
    commentaire = models.CharField(
        max_length=1000, 
        null=True, 
        blank=True,
        help_text="Informations complémentaires possibles à renseigner",
        )