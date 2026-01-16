from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Role(models.Model):
    """
    Représente un rôle attribué à un utilisateur, avec un rang pour la hiérarchie.
    """
    nomRole = models.CharField(
        max_length=50,
        help_text="Nom du rôle (ex: Administrateur, Technicien, etc.)"
    )
    rang = models.PositiveSmallIntegerField(
        help_text="Rang du rôle pour hiérarchiser les permissions (plus petit = plus élevé)"
    )

    def __str__(self):
        return self.nomRole
    
    class Meta:
        db_table = 'gimao_role'
        verbose_name = 'Rôle'
        verbose_name_plural = 'Rôles'
        ordering = ['rang']


class Utilisateur(models.Model):
    """
    Représente un utilisateur du système.
    """
    nomUtilisateur = models.CharField(
        max_length=50,
        unique=True,
        help_text="Identifiant unique pour la connexion"
    )
    motDePasse = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="Mot de passe hashé de l'utilisateur (null si pas encore défini)"
    )
    prenom = models.CharField(
        max_length=50,
        help_text="Prénom de l'utilisateur"
    )
    nomFamille = models.CharField(
        max_length=50,
        help_text="Nom de famille de l'utilisateur"
    )
    email = models.EmailField(
        max_length=150,
        unique=True,
        help_text="Adresse email de l'utilisateur"
    )
    photoProfil = models.FileField(
        upload_to='utilisateur_photos/',
        null=True,
        blank=True,
        help_text="Photo de profil de l'utilisateur"
    )
    derniereConnexion = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date et heure de la dernière connexion"
    )
    dateCreation = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de création du compte"
    )
    actif = models.BooleanField(
        default=True,
        help_text="Indique si le compte est actif"
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="utilisateurs",
        help_text="Rôle attribué à l'utilisateur"
    )

    def set_password(self, raw_password):
        if raw_password:
            self.motDePasse = make_password(raw_password)
        else:
            self.motDePasse = None
    
    def check_password(self, raw_password):
        if not self.motDePasse:
            return False
        return check_password(raw_password, self.motDePasse)
    
    def has_usable_password(self):
        return self.motDePasse is not None and self.motDePasse != ''
    
    def premiere_connexion(self):
        return self.derniereConnexion is None

    def __str__(self):
        return f"{self.prenom} {self.nomFamille} ({self.nomUtilisateur})"
    
    class Meta:
        db_table = 'gimao_utilisateur'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['nomFamille', 'prenom']


class Log(models.Model):
    """
    Représente un journal d'activité ou de modification dans le système.
    """
    type = models.CharField(
        max_length=50,
        help_text="Type de log (ex: création, modification, suppression)"
    )
    nomTable = models.CharField(
        max_length=50,
        help_text="Nom de la table affectée par l'action"
    )
    idCible = models.JSONField(
        help_text="Identifiant(s) de l'objet modifié"
    )
    champsModifies = models.JSONField(
        help_text="Champs modifiés et leurs nouvelles valeurs"
    )
    date = models.DateTimeField(
        auto_now_add=True,
        help_text="Date et heure de l'action"
    )
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="logs",
        help_text="Utilisateur qui a effectué l'action"
    )

    def __str__(self):
        return f"{self.type} sur {self.nomTable} ({self.date})"
    
    class Meta:
        db_table = 'gimao_log'
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
        ordering = ['-date']