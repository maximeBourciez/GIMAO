from django.db import models
from .validators import phone_regex, EmailValidator


class Fournisseur(models.Model):
    nomFournisseur = models.CharField(max_length=50)
    numRue = models.SmallIntegerField()
    nomRue = models.CharField(max_length=50)
    codePostal = models.CharField(max_length=50)
    ville = models.CharField(max_length=50)
    paysFournisseur = models.CharField(max_length=50)
    mailFournisseur = models.EmailField(max_length=50, null=True, blank=True, validators=[EmailValidator()])
    numTelephoneFournisseur = models.CharField(max_length=15, null=True, blank=True, validators=[phone_regex])
    serviceApresVente = models.BooleanField(
        help_text="Indique si le fournisseur propose un service d'aprés vente",
    )


    def __str__(self):
        return self.nomFournisseur

