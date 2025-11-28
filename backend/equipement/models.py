from django.db import models
from django.contrib.auth.models import User


class Equipement(models.Model):
    reference = models.CharField(
        max_length=50,
        primary_key=True,
    )
    dateCreation = models.DateTimeField()
    designation = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Nom par lequel nous faisons référence à la machine."
    )
    dateMiseEnService = models.DateField()
    prixAchat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prix auquel vous avez acheté le lot"
    )
    lienImageEquipement = models.ImageField(upload_to='images/equipement', null=False)
    createurEquipement = models.ForeignKey(
        User,
        related_name='createurEquipement',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    lieu = models.ForeignKey('gestionDonnee.Lieu', on_delete=models.CASCADE, null=True, blank=True)
    modeleEquipement = models.ForeignKey(
        'gestionDonnee.ModeleEquipement',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    fournisseur = models.ForeignKey(
        'gestionDonnee.Fournisseur',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    preventifGlissant = models.BooleanField(null=True, blank=True)
    joursIntervalleMaintenance = models.SmallIntegerField()

    def __str__(self):
        return self.designation or self.reference

    class Meta:
        db_table = 'gimao_equipement'


class InformationStatut(models.Model):
    STATUT_CHOICES = [
        ('Rebuté', 'Rebuté'),
        ('En fonctionnement', 'En fonctionnement'),
        ('Dégradé', 'Dégradé'),
        ('À l\'arrêt', 'À l\'arrêt'),
    ]
    statutEquipement = models.CharField(
        max_length=50,
        choices=STATUT_CHOICES,
        null=True,
        blank=True
    )
    dateChangement = models.DateTimeField(null=True, blank=True)
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    informationStatutParent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    ModificateurStatut = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Statut de {self.equipement}: {self.statutEquipement} (modifié le {self.dateChangement})"

    class Meta:
        db_table = 'gimao_informationstatut'


class Constituer(models.Model):
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    consommable = models.ForeignKey('stock.Consommable', on_delete=models.CASCADE)

    class Meta:
        db_table = 'gimao_constituer'
