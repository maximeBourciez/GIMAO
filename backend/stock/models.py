from django.db import models
from django.core.validators import MinValueValidator

from donnees.models import Adresse

class Magasin(models.Model):
    nom = models.CharField(max_length=100)
    estMobile = models.BooleanField(default=False)
    adresse = models.ForeignKey(Adresse, on_delete=models.CASCADE, null=True, blank=True, help_text="Adresse du magasin")

    def __str__(self):
        return self.nom

    class Meta:
        db_table = 'gimao_magasin'
        verbose_name = 'Magasin'
        verbose_name_plural = 'Magasins'


class Consommable(models.Model):
    designation = models.CharField(max_length=50)
    lienImageConsommable = models.ImageField(upload_to='images/', null=True, blank=True)
    magasins = models.ManyToManyField(Magasin, through='Stocker', related_name='consommables', blank=True)
    seuilStockFaible = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True, help_text="Seuil en dessous duquel le stock est considéré comme faible")
    documents = models.ManyToManyField('donnees.Document', blank=True, help_text="Documents associés au consommable")
    
    def __str__(self):
        return self.designation

    class Meta:
        db_table = 'gimao_consommable'
        verbose_name = 'Consommable'
        verbose_name_plural = 'Consommables'

class PorterSur(models.Model):
    """
    Table d'association pour FournitureConsommable
    Relation entre Consommable, Fournisseur et Fabricant
    """
    # Relations
    consommable = models.ForeignKey(
        Consommable,
        on_delete=models.CASCADE,
        related_name='fournitures'
    )
    fournisseur = models.ForeignKey(
        'donnees.Fournisseur',
        on_delete=models.CASCADE,
        related_name='fournitures'
    )
    fabricant = models.ForeignKey(
        'donnees.Fabricant',
        on_delete=models.CASCADE,
        related_name='fournitures'
    )
    
    # Attributs
    quantite = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    date_reference_prix = models.DateTimeField()
    
    class Meta:
        db_table = 'gimao_porter_sur'
        verbose_name = 'Fourniture de consommable'
        verbose_name_plural = 'Fournitures de consommables'
        unique_together = ['consommable', 'fournisseur', 'fabricant', 'date_reference_prix']
    
    def __str__(self):
        return f"{self.consommable} - {self.fournisseur} - {self.fabricant} ({self.date_reference_prix})"


class Stocker(models.Model):
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE, related_name='stocks')
    magasin = models.ForeignKey(Magasin, on_delete=models.CASCADE, related_name='stocks')
    quantite = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'gimao_stocker'
        verbose_name = 'Stock en magasin'
        verbose_name_plural = 'Stocks en magasin'
        unique_together = ['consommable', 'magasin']

    def __str__(self):
        return f"{self.consommable} dans {self.magasin} : {self.quantite}"


class EstCompatible(models.Model):
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE)
    modeleEquipement = models.ForeignKey('equipement.ModeleEquipement', on_delete=models.CASCADE)

    class Meta:
        db_table = 'gimao_estcompatible'
        verbose_name = 'Compatibilité consommable-modèle'
        verbose_name_plural = 'Compatibilités consommable-modèle'
        unique_together = ['consommable', 'modeleEquipement']