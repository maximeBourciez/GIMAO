# myApp/models.py
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError


# ------------------------- Création des validateurs des models -------------------------

# Validateur pour les numéros de téléphone
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Le numéro de téléphone doit être entré au format: '+999999999'. Jusqu'à 15 chiffres autorisés.")

# Valideur pour le champ 'niveau' dans la table 'Defaillance'.
def validate_niveau_de_defaillance(value):
    niveaux_valid = ["Critique", "Majeur", "Mineur"]
    
    if value not in niveaux_valid:
        raise ValidationError(f"Le niveau de défaillance doit être l'une des valeurs suivantes: {', '.join(niveaux_valid)}.")


def validate_etat_equipement(value):
    etat_valid = ["Rebuté", "En fonctionnement", "Dégradé", "A l'arrêt"]
    
    if value not in etat_valid:
        raise ValidationError(f"Le statut du modèle doit être l'une des valeurs suivantes :  {', '.join(etat_valid)}.")


# ------------------------- Création des models -------------------------


class Role(models.Model):
    nomRole = models.CharField(max_length=50)

    def __str__(self):
        return self.nomRole

class Avoir(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)

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

class Consommable(models.Model):
    designation = models.CharField(max_length=50)
    lienImageConsommable = models.ImageField(upload_to='images/consomable', null=False) 
    fabricant = models.ForeignKey(Fabricant, on_delete=models.CASCADE)

    def __str__(self):
        return self.designation

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

class ModeleEquipement(models.Model):
    nomModeleEquipement = models.CharField(max_length=50)
    fabricant = models.ForeignKey(Fabricant, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomModeleEquipement

class EstCompatible(models.Model):
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE)
    modeleEquipement = models.ForeignKey(ModeleEquipement, on_delete=models.CASCADE)

class Lieu(models.Model):
    nomLieu = models.CharField(max_length=50)
    typeLieu = models.CharField(
        max_length=50,
        help_text="Informations complémentaires optionnelles sur le type de lieu renseigné.")

    lieuParent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Pointeur désignant la structure (un autre lieu) où se trouve l'élément en question.")

    def __str__(self):
        return self.nomLieu

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

class Constituer(models.Model):
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE)

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

class DocumentTechnique(models.Model):
    nomDocumentTechnique = models.CharField(max_length=50)
    lienDocumentTechnique = models.FileField(upload_to='documents/documentTecnique', null=False) 

    def __str__(self):
        return self.nomDocumentTechnique

class Correspondre(models.Model):
    documentTechnique = models.ForeignKey(DocumentTechnique, on_delete=models.CASCADE)
    modeleEquipement = models.ForeignKey(ModeleEquipement, on_delete=models.CASCADE)

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

class DocumentDefaillance(models.Model):
    nomDocumentDefaillance = models.CharField(max_length=50)
    lienDocumentDefaillance = models.FileField(upload_to='documents/documentDefaillance', null=False) 
    defaillance = models.ForeignKey(Defaillance, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomDocumentDefaillance


class Intervention(models.Model):
    nomIntervention = models.CharField(max_length=500, null=True, blank=True)
    interventionCurative = models.BooleanField(null=True, blank=True)
    dateAssignation = models.DateTimeField()
    dateCloture = models.DateTimeField(null=True, blank=True)
    dateDebutIntervention = models.DateTimeField(null=True, blank=True)
    dateFinIntervention = models.DateTimeField(null=True, blank=True)
    tempsEstime = models.TimeField(null=True, blank=True)
    commentaireIntervention = models.CharField(max_length=1000, null=True, blank=True)
    commentaireRefusCloture = models.CharField(max_length=1000, null=True, blank=True)
    defaillance = models.ForeignKey(Defaillance, on_delete=models.CASCADE)
    createurIntervention = models.ForeignKey(User,
    related_name='createurIntervention', 
    on_delete=models.CASCADE,
    help_text="La personne qui crée l'intervention")
    
    responsable = models.ForeignKey(User, 
    related_name='responsable', 
    on_delete=models.CASCADE, 
    null=True, blank=True,
    help_text="La personne qui réalise l'intervention"
    )

    def __str__(self):
        return self.nomIntervention

class DocumentIntervention(models.Model):
    nomDocumentIntervention = models.CharField(max_length=500)
    lienDocumentIntervention = models.FileField(upload_to='documents/documentIntervention', null=False) 
    intervention = models.ForeignKey(Intervention, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomDocumentIntervention
