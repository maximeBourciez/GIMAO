from django.db import models
from django.core.validators import RegexValidator, EmailValidator


# Validateur pour les numéros de téléphone
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Le numéro de téléphone doit être entré au format: '+999999999'. Jusqu'à 15 chiffres autorisés."
)


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

    class Meta:
        db_table = 'gimao_fabricant'


class Fournisseur(models.Model):
    nomFournisseur = models.CharField(max_length=50)
    numRue = models.SmallIntegerField()
    nomRue = models.CharField(max_length=50)
    codePostal = models.CharField(max_length=50)
    ville = models.CharField(max_length=50)
    paysFournisseur = models.CharField(max_length=50)
    mailFournisseur = models.EmailField(
        max_length=50,
        null=True,
        blank=True,
        validators=[EmailValidator()]
    )
    numTelephoneFournisseur = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[phone_regex]
    )
    serviceApresVente = models.BooleanField(
        help_text="Indique si le fournisseur propose un service d'après vente",
    )

    def __str__(self):
        return self.nomFournisseur

    class Meta:
        db_table = 'gimao_fournisseur'


class ModeleEquipement(models.Model):
    nomModeleEquipement = models.CharField(max_length=50)
    fabricant = models.ForeignKey(Fabricant, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomModeleEquipement

    class Meta:
        db_table = 'gimao_modeleequipement'


class Lieu(models.Model):
    nomLieu = models.CharField(max_length=50)
    typeLieu = models.CharField(
        max_length=50,
        help_text="Informations complémentaires optionnelles sur le type de lieu renseigné."
    )
    lieuParent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Pointeur désignant la structure (un autre lieu) où se trouve l'élément en question."
    )

    def __str__(self):
        return self.nomLieu

    class Meta:
        db_table = 'gimao_lieu'


class DocumentTechnique(models.Model):
    nomDocumentTechnique = models.CharField(max_length=50)
    lienDocumentTechnique = models.FileField(upload_to='documents/documentTecnique', null=False)

    def __str__(self):
        return self.nomDocumentTechnique

    class Meta:
        db_table = 'gimao_documenttechnique'


class Correspondre(models.Model):
    documentTechnique = models.ForeignKey(DocumentTechnique, on_delete=models.CASCADE)
    modeleEquipement = models.ForeignKey(ModeleEquipement, on_delete=models.CASCADE)

    class Meta:
        db_table = 'gimao_correspondre'
