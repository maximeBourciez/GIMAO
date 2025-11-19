from django.db import models


class Consommable(models.Model):
    designation = models.CharField(max_length=50)
    lienImageConsommable = models.ImageField(upload_to='images/consomable', null=False)
    fabricant = models.ForeignKey('gestionDonnee.Fabricant', on_delete=models.CASCADE)

    def __str__(self):
        return self.designation

    class Meta:
        db_table = 'gimao_consommable'


class StockConsommable(models.Model):
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey('gestionDonnee.Fournisseur', on_delete=models.CASCADE)
    prixAchat = models.DecimalField(max_digits=7, decimal_places=2)
    dateAchat = models.DateField()
    quantiteConsommable = models.SmallIntegerField()
    commentaire = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        help_text="Informations complémentaires possibles à renseigner",
    )

    class Meta:
        db_table = 'gimao_stockconsommable'


class EstCompatible(models.Model):
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE)
    modeleEquipement = models.ForeignKey('gestionDonnee.ModeleEquipement', on_delete=models.CASCADE)

    class Meta:
        db_table = 'gimao_estcompatible'
