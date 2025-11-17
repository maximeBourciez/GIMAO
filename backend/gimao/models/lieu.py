from django.db import models


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
