from django.db import models
from django.core.validators import MinValueValidator

from stock.models import Consommable
from equipement.models import Equipement, Compteur
from utilisateur.models import Utilisateur
from stock.models import Consommable
from donnees.models import Fabricant, Fournisseur, Document

class DemandeIntervention(models.Model):
    """Demande d'intervention sur un équipement"""
    commentaire = models.TextField(blank=True, null=True)
    nom = models.CharField(max_length=255)
    statut = models.CharField(max_length=50)
    date_creation = models.DateTimeField()
    date_changementStatut = models.DateTimeField()
    
    # Relations
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='demandes_intervention'
    )
    equipement = models.ForeignKey(
        Equipement,
        on_delete=models.CASCADE,
        related_name='demandes_intervention'
    )
    
    class Meta:
        db_table = 'gimao_demande_intervention'
        verbose_name = 'Demande d\'intervention'
        verbose_name_plural = 'Demandes d\'intervention'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.nom} - {self.equipement}"


class BonTravail(models.Model):
    """Bon de travail généré suite à une demande d'intervention"""
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('EN_COURS', 'En cours'),
        ('TERMINE', 'Terminé'),
        ('EN_RETARD', 'En retard'),
        ('CLOTURE', 'Clôturé'),
    ]
    
    TYPE_CHOICES = [
        ('CORRECTIF', 'Correctif'),
        ('PREVENTIF', 'Préventif'),
        ('AMELIORATIF', 'Amélioratif'),
    ]
    
    nom = models.CharField(max_length=255)
    diagnostic = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    date_assignation = models.DateTimeField(blank=True, null=True)
    date_cloture = models.DateTimeField(blank=True, null=True)
    date_debut = models.DateTimeField(blank=True, null=True)
    date_fin = models.DateTimeField(blank=True, null=True)
    date_prevue = models.DateTimeField(blank=True, null=True)
    statut = models.CharField(
        max_length=50,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE'
    )
    commentaire = models.TextField(blank=True, null=True)
    commentaire_refus_cloture = models.TextField(blank=True, null=True)
    
    # Relations
    demande_intervention = models.ForeignKey(
        DemandeIntervention,
        on_delete=models.CASCADE,
        related_name='bons_travail'
    )
    utilisateur_assigne = models.ManyToManyField(
        Utilisateur,
        blank=True,
        related_name='bons_travail_assignes'
    )
    responsable = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bons_travail_responsable'
    )
    equipement = models.ForeignKey(
        Equipement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bons_travail'
    )
    
    class Meta:
        db_table = 'bon_travail'
        verbose_name = 'Bon de travail'
        verbose_name_plural = 'Bons de travail'
        ordering = ['-date_assignation']
    
    def __str__(self):
        return f"{self.nom} - {self.statut}"
    
    class Meta:
        db_table = 'gimao_bon_travail'
        verbose_name = 'Bon de travail'
        verbose_name_plural = 'Bons de travail'


class TypePlanMaintenance(models.Model):
    """Type de plan de maintenance (préventif, prédictif, etc.)"""
    libelle = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'type_plan_maintenance'
        verbose_name = 'Type de plan de maintenance'
        verbose_name_plural = 'Types de plan de maintenance'
    
    def __str__(self):
        return self.libelle
    
    class Meta:
        db_table = 'gimao_type_plan_maintenance'
        verbose_name = 'Type de plan de maintenance'
        verbose_name_plural = 'Types de plan de maintenance'


class PlanMaintenance(models.Model):
    """Plan de maintenance pour un équipement"""
    nom = models.CharField(max_length=255)
    contenu = models.TextField(blank=True, null=True)
    
    # Relations
    type_plan_maintenance = models.ForeignKey(
        TypePlanMaintenance,
        on_delete=models.CASCADE,
        related_name='plans_maintenance'
    )
    compteur = models.ForeignKey(
        Compteur,
        on_delete=models.CASCADE,
        related_name='plans_maintenance'
    )
    equipement = models.ForeignKey(
        Equipement,
        on_delete=models.CASCADE,
        related_name='plans_maintenance'
    )
    
    # RelationsMany-to-Many
    documents = models.ManyToManyField(
        Document,
        through='PlanMaintenanceDocument',
        related_name='plans_maintenance',
        blank=True
    )
    consommables = models.ManyToManyField(
        Consommable,
        through='PlanMaintenanceConsommable',
        related_name='plans_maintenance',
        blank=True
    )
    
    class Meta:
        db_table = 'gimao_plan_maintenance'
        verbose_name = 'Plan de maintenance'
        verbose_name_plural = 'Plans de maintenance'
    
    def __str__(self):
        return f"{self.nom} - {self.equipement}"



# ==================== TABLE D'ASSOCIATION ====================

class PlanMaintenanceConsommable(models.Model):
    """Table d'association entre PlanMaintenance et Consommable"""
    plan_maintenance = models.ForeignKey(
        PlanMaintenance,
        on_delete=models.PROTECT
    )
    consommable = models.ForeignKey(
        Consommable,
        on_delete=models.CASCADE
    )
    quantite_necessaire = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        help_text="Quantité nécessaire pour ce plan"
    )
    
    class Meta:
        db_table = 'gimao_plan_maintenance_consommable'
        unique_together = ['plan_maintenance', 'consommable']
        verbose_name = 'Consommable nécessaire'
        verbose_name_plural = 'Consommables nécessaires'
    
    def __str__(self):
        return f"{self.plan_maintenance} - {self.consommable} (x{self.quantite_necessaire})"
    
    
class PlanMaintenanceDocument(models.Model):
    """Table d'association entre PlanMaintenance et Document"""
    plan_maintenance = models.ForeignKey(
        PlanMaintenance,
        on_delete=models.CASCADE
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE
    )
    
    class Meta:
        db_table = 'gimao_plan_maintenance_document'
        unique_together = ['plan_maintenance', 'document']
        verbose_name = 'Document de plan de maintenance'
        verbose_name_plural = 'Documents de plans de maintenance'
    
    def __str__(self):
        return f"{self.plan_maintenance} - {self.document}"