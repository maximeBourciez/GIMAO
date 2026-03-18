import hashlib
from datetime import timedelta

import pytest
from django.utils import timezone

from security.models import ApiToken, create_token
from tests.factories import UtilisateurFactory


@pytest.mark.django_db
def test_should_consider_token_valid_when_not_revoked_and_not_expired():
    user = UtilisateurFactory()
    token = ApiToken.objects.create(
        user=user,
        token_hash="a" * 64,
        valid_until=timezone.now() + timedelta(hours=1),
        is_revoked=False,
    )

    assert token.is_valid() is True


@pytest.mark.django_db
def test_should_consider_token_invalid_when_revoked():
    user = UtilisateurFactory()
    token = ApiToken.objects.create(
        user=user,
        token_hash="b" * 64,
        valid_until=timezone.now() + timedelta(hours=1),
        is_revoked=True,
    )

    assert token.is_valid() is False


@pytest.mark.django_db
def test_should_consider_token_invalid_when_expired():
    user = UtilisateurFactory()
    token = ApiToken.objects.create(
        user=user,
        token_hash="c" * 64,
        valid_until=timezone.now() - timedelta(seconds=1),
        is_revoked=False,
    )

    assert token.is_valid() is False


@pytest.mark.django_db
def test_should_create_token_and_store_hash_with_one_day_validity():
    user = UtilisateurFactory()

    raw_token = create_token(user)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    stored = ApiToken.objects.get(token_hash=token_hash)

    assert stored.user_id == user.pk
    assert stored.is_revoked is False

    remaining = stored.valid_until - timezone.now()
    assert timedelta(hours=23) <= remaining <= timedelta(hours=24, minutes=1)
