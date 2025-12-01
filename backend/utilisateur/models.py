from django.db import models

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
        help_text="Mot de passe hashé de l'utilisateur"
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

    def __str__(self):
        return f"{self.prenom} {self.nomFamille} ({self.nomUtilisateur})"


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


class Avoir(models.Model):
    """
    Représente une relation d'appartenance entre un utilisateur et une entité.
    """
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="avoirs",
        help_text="Utilisateur concerné par la relation"
    )
    roles = models.ManyToManyField(
        Role,
        help_text="Rôles attribués à l'utilisateur pour cette entité"
    )

    def __str__(self):
        return f"{self.utilisateur.nomUtilisateur} - Rôles: {', '.join(role.nomRole for role in self.roles.all())}"