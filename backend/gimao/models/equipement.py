from django.db import models
from django.contrib.auth.models import User, AbstractUser

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
    createurEquipement = models.ForeignKey(User, related_name='createurEquipement', on_delete=models.CASCADE, null=True, blank=True)
    lieu = models.ForeignKey('Lieu', on_delete=models.CASCADE, null=True, blank=True)
    modeleEquipement = models.ForeignKey('ModeleEquipement', on_delete=models.CASCADE, null=True, blank=True)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, null=True, blank=True)
    preventifGlissant = models.BooleanField(null=True, blank=True)
    joursIntervalleMaintenance = models.SmallIntegerField()

    def __str__(self):
        return self.designation