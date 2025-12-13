from django.db import models
from stock.models import Consommable
from donnees.models import Lieu, Document, Fabricant, Fournisseur
from utilisateur.models import Utilisateur



class ModeleEquipement(models.Model):
    """
    Représente un modèle d'équipement fabriqué par un fabricant.
    """
    nom = models.CharField(max_length=100, help_text="Nom du modèle d'équipement")
    fabricant = models.ForeignKey(Fabricant, on_delete=models.PROTECT, related_name="modeles", help_text="Fabricant du modèle")

    def __str__(self):
        return f"{self.nom} ({self.fabricant.nom})"
    
    class Meta:
        db_table = 'gimao_modele_equipement'
        verbose_name = 'Modèle d\'équipement'
        verbose_name_plural = 'Modèles d\'équipements'


class FamilleEquipement(models.Model):
    """
    Représente une famille ou catégorie d'équipements.
    """
    nom = models.CharField(max_length=100, help_text="Nom de la famille d'équipements")
    familleParente = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="sous_familles", help_text="Famille parente, si applicable")

    def __str__(self):
        return self.nom
    
    class Meta:
        db_table = 'gimao_famille_equipement'
        verbose_name = 'Famille d\'équipement'
        verbose_name_plural = 'Familles d\'équipements'


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
    createurEquipement = models.ForeignKey(
        Utilisateur,
        on_delete=models.PROTECT,
        default=None,
        related_name="equipements_crees",
        help_text="Utilisateur ayant créé l'équipement"
    )
    lieu = models.ForeignKey(Lieu, on_delete=models.PROTECT, related_name="equipements", help_text="Lieu où se trouve l'équipement")
    documents = models.ManyToManyField( Document, 
                                        through='DocumentEquipement', 
                                        blank=True, 
                                        help_text="Documents associés à l'équipement"
                                    )   
    fabricant = models.ForeignKey(Fabricant, on_delete=models.PROTECT, null=True, blank=True, related_name="equipements", help_text="Fabricant de l'équipement")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.PROTECT, null=True, blank=True, related_name="equipements", help_text="Fournisseur de l'équipement")
    modele = models.ForeignKey(ModeleEquipement, on_delete=models.PROTECT, null=True, blank=True, related_name="equipements", help_text="Modèle de l'équipement")
    famille = models.ForeignKey(FamilleEquipement, null=True, blank=True, on_delete=models.SET_NULL, related_name="equipements", help_text="Famille de l'équipement")
    x = models.FloatField(null=True, blank=True, help_text="Coordonnée X de l'équipement dans le lieu")
    y = models.FloatField(null=True, blank=True, help_text="Coordonnée Y del'équipement dans le lieu")
    lieu = models.ForeignKey(Lieu, on_delete=models.PROTECT, related_name="equipements", help_text="Lieu où se trouve l'équipement")

    def __str__(self):
        return f"{self.designation} ({self.numSerie})"
    
    class Meta:
        db_table = 'gimao_equipement'
        verbose_name = 'Équipement'
        verbose_name_plural = 'Équipements'


class StatutEquipement(models.Model):
    """
    Historique des statuts d'un équipement.
    """
    statut = models.CharField(max_length=50, help_text="Statut de l'équipement")
    dateChangement = models.DateTimeField(auto_now_add=True, help_text="Date du changement de statut")
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, related_name="statuts", help_text="Équipement concerné")

    def __str__(self):
        return f"{self.statut} ({self.dateChangement})"
    
    class Meta:
        db_table = 'gimao_statut_equipement'
        verbose_name = 'Statut d\'équipement'
        verbose_name_plural = 'Statuts d\'équipements'
        ordering = ['-dateChangement']


class Compteur(models.Model):
    """
    Représente un compteur ou indicateur lié à un équipement pour la maintenance.
    """
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, related_name="compteurs", help_text="Équipement associé au compteur")
    nomCompteur = models.CharField(max_length=100, null=False, default="Compteur sans nom", help_text="Nom du compteur")
    valeurCourante = models.FloatField(help_text="Valeur actuelle du compteur")
    prochaineMaintenance = models.FloatField(help_text="Valeur prévue pour la prochaine maintenance")
    ecartInterventions = models.FloatField(help_text="Écart moyen entre interventions")
    unite = models.CharField(max_length=50, help_text="Unité de mesure du compteur", default="jours")
    estGlissant = models.BooleanField(default=False, help_text="Indique si ce compteur est glissant")
    descriptifMaintenance = models.CharField(max_length=255, blank=True, null=True, help_text="Description de la maintenance liée")
    necessiteHabilitationElectrique = models.BooleanField(default=False, help_text="Nécessite une habilitation électrique")
    necessitePermisFeu = models.BooleanField(default=False, help_text="Nécessite un permis feu")
    estPrincipal = models.BooleanField(default=False, help_text="Indique si ce compteur est le principal pour l'équipement")

    def __str__(self):
        return f"Compteur {self.id} - {self.equipement.designation}"
    
    class Meta:
        db_table = 'gimao_compteur'
        verbose_name = 'Compteur'
        verbose_name_plural = 'Compteurs'


class Constituer(models.Model):
    """
    Relation many-to-many entre Equipement et Consommable (de l'app stock).
    """
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, help_text="Équipement associé")
    consommable = models.ForeignKey(Consommable, on_delete=models.CASCADE, help_text="Consommable associé")

    def __str__(self):
        return f"Equipement {self.equipement.id} - Consommable {self.consommable.id}"
    
    class Meta:
        db_table = 'gimao_constituer'
        verbose_name = 'Constituer'
        verbose_name_plural = 'Constituer'
        
        
class DocumentEquipement(models.Model):
    """
    Relation many-to-many entre Equipement et Document (de l'app donnees).
    """
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, help_text="Équipement associé")
    document = models.ForeignKey(Document, on_delete=models.CASCADE, help_text="Document associé")

    def __str__(self):
        return f"Equipement {self.equipement.id} - Document {self.document.id}"
    
    class Meta:
        db_table = 'gimao_document_equipement'
        verbose_name = 'Lien Document-Equipement'
        verbose_name_plural = 'Liens Documents-Equipements'