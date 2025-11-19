from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    nomRole = models.CharField(max_length=50)

    def __str__(self):
        return self.nomRole

    class Meta:
        db_table = 'gimao_role'


class Avoir(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'gimao_avoir'
