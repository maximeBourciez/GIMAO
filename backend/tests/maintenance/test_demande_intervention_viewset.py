import pytest
from django.utils import timezone
from rest_framework.test import APIRequestFactory

from maintenance.api.viewsets import DemandeInterventionViewSet
from maintenance.models import BonTravail
from tests.factories import DemandeInterventionFactory, EquipementFactory, UtilisateurFactory


@pytest.fixture
def api_factory():
    return APIRequestFactory()


@pytest.mark.django_db
def test_should_return_400_when_par_equipement_without_param(api_factory):
    view = DemandeInterventionViewSet.as_view({"get": "par_equipement"})
    request = api_factory.get("/api/maintenance/demandes-intervention/par_equipement/")

    response = view(request)

    assert response.status_code == 400
    assert "equipement_id" in response.data["error"]


@pytest.mark.django_db
def test_should_filter_demandes_by_equipement(api_factory):
    equipement_target = EquipementFactory()
    equipement_other = EquipementFactory()
    di_target = DemandeInterventionFactory(equipement=equipement_target)
    DemandeInterventionFactory(equipement=equipement_other)

    view = DemandeInterventionViewSet.as_view({"get": "par_equipement"})
    request = api_factory.get(
        "/api/maintenance/demandes-intervention/par_equipement/",
        {"equipement_id": equipement_target.pk},
    )

    response = view(request)

    assert response.status_code == 200
    ids = [item["id"] for item in response.data]
    assert ids == [di_target.id]


@pytest.mark.django_db
def test_should_return_400_when_par_utilisateur_without_param(api_factory):
    view = DemandeInterventionViewSet.as_view({"get": "par_utilisateur"})
    request = api_factory.get("/api/maintenance/demandes-intervention/par_utilisateur/")

    response = view(request)

    assert response.status_code == 400
    assert "utilisateur_id" in response.data["error"]


@pytest.mark.django_db
def test_should_filter_demandes_by_utilisateur(api_factory):
    user_target = UtilisateurFactory()
    user_other = UtilisateurFactory()
    di_target = DemandeInterventionFactory(utilisateur=user_target)
    DemandeInterventionFactory(utilisateur=user_other)

    view = DemandeInterventionViewSet.as_view({"get": "par_utilisateur"})
    request = api_factory.get(
        "/api/maintenance/demandes-intervention/par_utilisateur/",
        {"utilisateur_id": user_target.pk},
    )

    response = view(request)

    assert response.status_code == 200
    ids = [item["id"] for item in response.data]
    assert ids == [di_target.id]


@pytest.mark.django_db
def test_should_update_demande_status_via_update_status_action(api_factory):
    demande = DemandeInterventionFactory(statut="EN_ATTENTE")
    before_change = demande.date_changementStatut

    view = DemandeInterventionViewSet.as_view({"patch": "updateStatus"})
    request = api_factory.patch(
        f"/api/maintenance/demandes-intervention/{demande.pk}/updateStatus/",
        {"statut": "ACCEPTEE"},
        format="json",
    )

    response = view(request, pk=demande.pk)
    demande.refresh_from_db()

    assert response.status_code == 200
    assert demande.statut == "ACCEPTEE"
    assert demande.date_changementStatut >= before_change


@pytest.mark.django_db
def test_should_transform_demande_to_bon_travail(api_factory):
    demande = DemandeInterventionFactory(statut="EN_ATTENTE")
    responsable = UtilisateurFactory()

    view = DemandeInterventionViewSet.as_view({"post": "transform_to_bon_travail"})
    request = api_factory.post(
        f"/api/maintenance/demandes-intervention/{demande.pk}/transform_to_bon_travail/",
        {"responsable": responsable.pk},
        format="json",
    )

    response = view(request, pk=demande.pk)
    demande.refresh_from_db()

    assert response.status_code == 200
    assert demande.statut == "TRANSFORMEE"

    bt = BonTravail.objects.get(demande_intervention=demande)
    assert bt.type == "CORRECTIF"
    assert bt.responsable_id == responsable.pk


@pytest.mark.django_db
def test_should_return_400_when_delink_document_without_document_id(api_factory):
    demande = DemandeInterventionFactory()

    view = DemandeInterventionViewSet.as_view({"patch": "delink_document"})
    request = api_factory.patch(
        f"/api/maintenance/demandes-intervention/{demande.pk}/delink_document/",
        {},
        format="json",
    )

    response = view(request, pk=demande.pk)

    assert response.status_code == 400
    assert "document_id" in response.data["error"]


@pytest.mark.django_db
def test_should_return_404_when_delink_document_not_linked(api_factory):
    demande = DemandeInterventionFactory()

    view = DemandeInterventionViewSet.as_view({"patch": "delink_document"})
    request = api_factory.patch(
        f"/api/maintenance/demandes-intervention/{demande.pk}/delink_document/",
        {"document_id": 999999},
        format="json",
    )

    response = view(request, pk=demande.pk)

    assert response.status_code == 404
    assert "n'est pas lié" in response.data["error"]
