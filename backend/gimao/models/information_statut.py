from django.db import models
from .equipement import Equipement
from django.contrib.auth.models import User, AbstractUser

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
    informationStatutParent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    ModificateurStatut = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Statut de {self.equipement}: {self.statutEquipement} (modifié le {self.dateChangement})"

