from django.db import models
from .validators import validate_niveau_de_defaillance
from django.contrib.auth.models import User, AbstractUser
from .equipement import Equipement

class Defaillance(models.Model):
    DEFAILLANCE_CHOICES = [
        ('Critique', 'Critique'),
        ('Majeur', 'Majeur'),
        ('Mineur', 'Mineur'),
    ]
    commentaireDefaillance = models.CharField(max_length=1000, null=True, blank=True)
    niveau = models.CharField(
        max_length=50,
        choices=DEFAILLANCE_CHOICES, 
        validators=[validate_niveau_de_defaillance])
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    dateTraitementDefaillance = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.commentaireDefaillance