import datetime
from decimal import Decimal

import pytest

from tests.factories import RoleFactory, UtilisateurFactory
from utilisateur.middleware import set_thread_user
from utilisateur.models import Log
from utilisateur.signals import get_safe_app_user, make_serializable


@pytest.mark.django_db
def test_make_serializable_handles_common_types():
    role = RoleFactory()
    payload = {
        "decimal": Decimal("12.34"),
        "date": datetime.date(2026, 3, 17),
        "datetime": datetime.datetime(2026, 3, 17, 10, 30, 0),
        "list": [Decimal("1.5"), role],
    }

    serialized = make_serializable(payload)

    assert serialized["decimal"] == "12.34"
    assert serialized["date"] == "2026-03-17"
    assert serialized["datetime"].startswith("2026-03-17T10:30:00")
    assert serialized["list"][0] == "1.5"
    assert serialized["list"][1] == role.pk


@pytest.mark.django_db
def test_get_safe_app_user_returns_none_for_invalid_inputs():
    assert get_safe_app_user(None) is None
    assert get_safe_app_user("not-a-user") is None

    unsaved_user = UtilisateurFactory.build()
    assert get_safe_app_user(unsaved_user) is None


@pytest.mark.django_db
def test_get_safe_app_user_returns_none_for_deleted_user():
    from unittest.mock import patch

    user = UtilisateurFactory()

    with patch("utilisateur.signals.Utilisateur.objects.filter") as mock_filter:
        mock_filter.return_value.exists.return_value = False
        assert get_safe_app_user(user) is None


@pytest.mark.django_db
def test_log_save_create_creates_log_entry():
    Log.objects.all().delete()

    role = RoleFactory(nomRole="Technicien")

    entry = Log.objects.get(type="création", nomTable="gimao_role")
    assert entry.idCible["id"] == role.pk
    assert entry.champsModifies["nomRole"]["nouveau"] == "Technicien"


@pytest.mark.django_db
def test_log_save_update_tracks_changed_fields():
    Log.objects.all().delete()
    role = RoleFactory(nomRole="Avant")

    role.nomRole = "Apres"
    role.save()

    update_entry = Log.objects.filter(type="modification", nomTable="gimao_role").latest("date")
    assert update_entry.champsModifies["nomRole"]["ancien"] == "Avant"
    assert update_entry.champsModifies["nomRole"]["nouveau"] == "Apres"


@pytest.mark.django_db
def test_log_save_update_without_changes_creates_no_modification_log():
    Log.objects.all().delete()
    role = RoleFactory(nomRole="Stable")

    before_count = Log.objects.filter(type="modification", nomTable="gimao_role").count()
    role.save()
    after_count = Log.objects.filter(type="modification", nomTable="gimao_role").count()

    assert before_count == after_count


@pytest.mark.django_db
def test_log_save_uses_thread_user_when_available():
    Log.objects.all().delete()
    actor = UtilisateurFactory()

    set_thread_user(actor)
    try:
        role = RoleFactory(nomRole="RoleWithActor")
    finally:
        set_thread_user(None)

    entry = Log.objects.filter(type="création", nomTable="gimao_role").latest("date")
    assert entry.idCible["id"] == role.pk
    assert entry.utilisateur_id == actor.pk


@pytest.mark.django_db
def test_log_delete_creates_suppression_entry():
    Log.objects.all().delete()
    role = RoleFactory(nomRole="A supprimer")

    role.delete()

    delete_entry = Log.objects.filter(type="suppression", nomTable="gimao_role").latest("date")
    assert delete_entry.champsModifies == {"deleted": True}
    assert delete_entry.idCible["id"] is not None


@pytest.mark.django_db
def test_log_model_is_ignored_by_signals_to_avoid_recursion():
    Log.objects.all().delete()

    Log.objects.create(
        type="manuel",
        nomTable="manual_table",
        idCible={"id": 1},
        champsModifies={"x": "y"},
        utilisateur=None,
    )

    assert Log.objects.count() == 1
