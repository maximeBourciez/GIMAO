from django.db import models
from .validators import phone_regex, EmailValidator

class Fabricant(models.Model):
    nomFabricant = models.CharField(
        max_length=50,
        help_text="Nom du fabricant",
        error_messages={
            'unique': "Ce nom de fabricant existe déjà.",
        }
    )

    paysFabricant = models.CharField(
        max_length=50,
        help_text="Pays du fabricant"
    )

    mailFabricant = models.EmailField(
        max_length=50,
        null=True,
        blank=True,
        validators=[EmailValidator()],
        help_text="Adresse e-mail du fabricant",
        error_messages={
            'invalid': "Entrez une adresse e-mail valide.",
        }
    )
    
    numTelephoneFabricant = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[phone_regex],
        help_text="Numéro de téléphone du fabricant",
        error_messages={
            'invalid': "Entrez un numéro de téléphone valide.",
        }
    )
    serviceApresVente = models.BooleanField(
        help_text="Indique si le fabricant offre un service après-vente"
    )

    def __str__(self):
        return self.nomFabricant