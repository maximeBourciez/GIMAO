from django.db import models
from .role import Role
from django.contrib.auth.models import User, AbstractUser

class Avoir(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)