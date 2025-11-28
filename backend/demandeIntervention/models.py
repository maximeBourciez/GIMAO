from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Validateur pour le niveau de défaillance
def validate_niveau_de_defaillance(value):
    niveaux_valid = ["Critique", "Majeur", "Mineur"]
    if value not in niveaux_valid:
        raise ValidationError(
            f"Le niveau de défaillance doit être l'une des valeurs suivantes: {', '.join(niveaux_valid)}."
        )


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
        validators=[validate_niveau_de_defaillance]
    )
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    equipement = models.ForeignKey('equipement.Equipement', on_delete=models.CASCADE)
    dateTraitementDefaillance = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.commentaireDefaillance or f"Défaillance {self.id}"

    class Meta:
        db_table = 'gimao_defaillance'


class DocumentDefaillance(models.Model):
    nomDocumentDefaillance = models.CharField(max_length=50)
    lienDocumentDefaillance = models.FileField(upload_to='documents/documentDefaillance', null=False)
    defaillance = models.ForeignKey(Defaillance, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomDocumentDefaillance

    class Meta:
        db_table = 'gimao_documentdefaillance'
