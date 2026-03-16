import hashlib
import secrets
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from utilisateur.models import Utilisateur


class ApiToken(models.Model):

    token_hash = models.CharField(max_length=64, unique=True, db_index=True)
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="api_tokens")

    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()

    is_revoked = models.BooleanField(default=False)

    def is_valid(self):
        return not self.is_revoked and self.valid_until > timezone.now()

    def __str__(self):
        return f"{self.user} - {self.token_hash[:10]}"
    




def create_token(user):

    token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(token.encode()).hexdigest()

    ApiToken.objects.create(
        token_hash=token_hash,
        user=user,
        valid_until=timezone.now() + timedelta(days=14)
    )

    return token