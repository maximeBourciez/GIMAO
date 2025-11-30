from django.db import models
from stock.models import Consommable

class Fabricant(models.Model):
    """
    Représente un fabricant d'équipements.
    """
    nom = models.CharField(max_length=100, help_text="Nom du fabricant")
    email = models.EmailField(max_length=191, blank=True, null=True, help_text="Adresse email du fabricant")
    numTelephone = models.CharField(max_length=20, blank=True, null=True, help_text="Numéro de téléphone du fabricant")
    serviceApresVente = models.BooleanField(default=False, help_text="Indique si le fabricant propose un service après-vente")

    def __str__(self):
        return self.nom


class Fournisseur(models.Model):
    """
    Représente un fournisseur d'équipements.
    """
    nom = models.CharField(max_length=100, help_text="Nom du fournisseur")
    email = models.EmailField(max_length=191, blank=True, null=True, help_text="Adresse email du fournisseur")
    numTelephone = models.CharField(max_length=20, blank=True, null=True, help_text="Numéro de téléphone du fournisseur")
    serviceApresVente = models.BooleanField(default=False, help_text="Indique si le fournisseur propose un service après-vente")

    def __str__(self):
        return self.nom


class ModeleEquipement(models.Model):
    """
    Représente un modèle d'équipement fabriqué par un fabricant.
    """
    nom = models.CharField(max_length=100, help_text="Nom du modèle d'équipement")
    fabricant = models.ForeignKey(Fabricant, on_delete=models.PROTECT, related_name="modeles", help_text="Fabricant du modèle")

    def __str__(self):
        return f"{self.nom} ({self.fabricant.nom})"


class FamilleEquipement(models.Model):
    """
    Représente une famille ou catégorie d'équipements.
    """
    nom = models.CharField(max_length=100, help_text="Nom de la famille d'équipements")
    familleParente = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="sous_familles", help_text="Famille parente, si applicable")

    def __str__(self):
        return self.nom


class Equipement(models.Model):
    """
    Représente un équipement physique.
    """
    numSerie = models.CharField(max_length=100, help_text="Numéro de série de l'équipement")
    reference = models.CharField(max_length=100, blank=True, null=True, help_text="Référence interne ou fournisseur")
    dateCreation = models.DateTimeField(auto_now_add=True, help_text="Date de création de l'équipement")
    designation = models.CharField(max_length=100, help_text="Nom ou désignation de l'équipement")
    dateMiseEnService = models.DateTimeField(null=True, blank=True, help_text="Date de mise en service de l'équipement")
    prixAchat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Prix d'achat de l'équipement")
    lienImage = models.CharField(max_length=255, blank=True, null=True, help_text="Lien vers une image de l'équipement")
    preventifGlissant = models.BooleanField(default=False, help_text="Indique si l'entretien préventif est glissant")
    joursIntervalleMaintenance = models.PositiveSmallIntegerField(default=0, help_text="Intervalle en jours pour la maintenance préventive")
    createurEquipementId = models.IntegerField(help_text="ID de l'utilisateur ayant créé l'équipement")
    lieuId = models.IntegerField(help_text="ID du lieu où se trouve l'équipement")
    modele = models.ForeignKey(ModeleEquipement, on_delete=models.PROTECT, related_name="equipements", help_text="Modèle de l'équipement")
    famille = models.ForeignKey(FamilleEquipement, null=True, blank=True, on_delete=models.SET_NULL, related_name="equipements", help_text="Famille de l'équipement")

    def __str__(self):
        return f"{self.designation} ({self.numSerie})"


class StatutEquipement(models.Model):
    """
    Historique des statuts d'un équipement.
    """
    statut = models.CharField(max_length=50, help_text="Statut de l'équipement")
    dateChangement = models.DateTimeField(auto_now_add=True, help_text="Date du changement de statut")
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, related_name="statuts", help_text="Équipement concerné")

    def __str__(self):
        return f"{self.statut} ({self.dateChangement})"


class Compteur(models.Model):
    """
    Représente un compteur ou indicateur lié à un équipement pour la maintenance.
    """
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, related_name="compteurs", help_text="Équipement associé au compteur")
    valeurCourante = models.FloatField(help_text="Valeur actuelle du compteur")
    valeurEcheance = models.FloatField(help_text="Valeur à l'échéance pour déclencher la maintenance")
    prochaineMaintenance = models.FloatField(help_text="Valeur prévue pour la prochaine maintenance")
    ecartInterventions = models.FloatField(help_text="Écart moyen entre interventions")
    estGlissant = models.BooleanField(default=False, help_text="Indique si ce compteur est glissant")
    descriptifMaintenance = models.CharField(max_length=255, blank=True, null=True, help_text="Description de la maintenance liée")
    necessiteHabilitationElectrique = models.BooleanField(default=False, help_text="Nécessite une habilitation électrique")
    necessitePermisFeu = models.BooleanField(default=False, help_text="Nécessite un permis feu")
    estPrincipal = models.BooleanField(default=False, help_text="Indique si ce compteur est le principal pour l'équipement")

    def __str__(self):
        return f"Compteur {self.id} - {self.equipement.designation}"


class Constituer(models.Model):
    """
    Relation many-to-many entre Equipement et Consommable (de l'app stock).
    """
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, help_text="Équipement associé")
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE, help_text="Consommable associé")

    def __str__(self):
        return f"Equipement {self.equipement.id} - Consommable {self.consommable.id}"