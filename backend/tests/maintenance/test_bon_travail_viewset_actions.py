import pytest

from rest_framework.test import APIRequestFactory

from maintenance.api.viewsets import BonTravailViewSet
from maintenance.models import BonTravailConsommable, BonTravailConsommableReservation
from stock.models import Magasin, Stocker
from tests.factories import BonTravailFactory, ConsommableFactory


@pytest.fixture
def api_factory():
    return APIRequestFactory()


@pytest.mark.django_db
def test_should_return_400_when_distribution_without_consommable_id(api_factory):
    bon = BonTravailFactory()

    view = BonTravailViewSet.as_view({"patch": "update_consommable_distribution"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/update_consommable_distribution/",
        {"distribue": True},
        format="json",
    )

    response = view(request, pk=bon.pk)

    assert response.status_code == 400
    assert "consommable_id" in response.data["error"]


@pytest.mark.django_db
def test_should_return_404_when_consommable_is_not_linked_to_bt(api_factory):
    bon = BonTravailFactory()
    consommable = ConsommableFactory()

    view = BonTravailViewSet.as_view({"patch": "update_consommable_distribution"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/update_consommable_distribution/",
        {"consommable_id": consommable.pk, "distribue": True},
        format="json",
    )

    response = view(request, pk=bon.pk)

    assert response.status_code == 404
    assert "Consommable non trouvé" in response.data["error"]


@pytest.mark.django_db
def test_should_confirm_distribution_and_decrease_stock_for_single_eligible_store(api_factory):
    bon = BonTravailFactory()
    consommable = ConsommableFactory()
    assoc = BonTravailConsommable.objects.create(
        bon_travail=bon,
        consommable=consommable,
        quantite_utilisee=3,
    )
    magasin = Magasin.objects.create(nom="Magasin A")
    stock = Stocker.objects.create(consommable=consommable, magasin=magasin, quantite=7)

    view = BonTravailViewSet.as_view({"patch": "update_consommable_distribution"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/update_consommable_distribution/",
        {"consommable_id": consommable.pk, "distribue": True},
        format="json",
    )

    response = view(request, pk=bon.pk)
    assoc.refresh_from_db()
    stock.refresh_from_db()

    assert response.status_code == 200
    assert assoc.estConfirme is True
    assert assoc.date_confirme is not None
    assert assoc.magasin_reserve_id == magasin.pk
    assert stock.quantite == 4


@pytest.mark.django_db
def test_should_return_409_when_multiple_stores_can_cover_and_no_choice_given(api_factory):
    bon = BonTravailFactory()
    consommable = ConsommableFactory()
    BonTravailConsommable.objects.create(
        bon_travail=bon,
        consommable=consommable,
        quantite_utilisee=2,
    )
    magasin_a = Magasin.objects.create(nom="Magasin A")
    magasin_b = Magasin.objects.create(nom="Magasin B")
    Stocker.objects.create(consommable=consommable, magasin=magasin_a, quantite=5)
    Stocker.objects.create(consommable=consommable, magasin=magasin_b, quantite=6)

    view = BonTravailViewSet.as_view({"patch": "update_consommable_distribution"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/update_consommable_distribution/",
        {"consommable_id": consommable.pk, "distribue": True},
        format="json",
    )

    response = view(request, pk=bon.pk)

    assert response.status_code == 409
    assert response.data["needs_magasin_selection"] is True
    assert len(response.data["magasins"]) == 2


@pytest.mark.django_db
def test_should_restore_stock_when_distribution_is_cancelled(api_factory):
    bon = BonTravailFactory()
    consommable = ConsommableFactory()
    magasin = Magasin.objects.create(nom="Magasin A")
    assoc = BonTravailConsommable.objects.create(
        bon_travail=bon,
        consommable=consommable,
        quantite_utilisee=3,
        estConfirme=True,
        magasin_reserve=magasin,
    )
    stock = Stocker.objects.create(consommable=consommable, magasin=magasin, quantite=1)
    BonTravailConsommableReservation.objects.create(
        bon_travail_consommable=assoc,
        magasin=magasin,
        quantite=3,
    )

    view = BonTravailViewSet.as_view({"patch": "update_consommable_distribution"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/update_consommable_distribution/",
        {"consommable_id": consommable.pk, "distribue": False},
        format="json",
    )

    response = view(request, pk=bon.pk)
    assoc.refresh_from_db()
    stock.refresh_from_db()

    assert response.status_code == 200
    assert assoc.estConfirme is False
    assert assoc.date_confirme is None
    assert assoc.magasin_reserve_id is None
    assert stock.quantite == 4
    assert assoc.reservations.count() == 0


@pytest.mark.django_db
def test_should_cancel_all_reservations_for_a_bt(api_factory):
    bon = BonTravailFactory()

    cons_1 = ConsommableFactory()
    mag_1 = Magasin.objects.create(nom="Magasin A")
    assoc_1 = BonTravailConsommable.objects.create(
        bon_travail=bon,
        consommable=cons_1,
        quantite_utilisee=2,
        estConfirme=True,
        magasin_reserve=mag_1,
    )
    stock_1 = Stocker.objects.create(consommable=cons_1, magasin=mag_1, quantite=3)
    BonTravailConsommableReservation.objects.create(
        bon_travail_consommable=assoc_1,
        magasin=mag_1,
        quantite=2,
    )

    cons_2 = ConsommableFactory()
    mag_2 = Magasin.objects.create(nom="Magasin B")
    assoc_2 = BonTravailConsommable.objects.create(
        bon_travail=bon,
        consommable=cons_2,
        quantite_utilisee=1,
        estConfirme=True,
        magasin_reserve=mag_2,
    )
    stock_2 = Stocker.objects.create(consommable=cons_2, magasin=mag_2, quantite=0)

    view = BonTravailViewSet.as_view({"patch": "cancel_mise_de_cote"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/cancel_mise_de_cote/",
        {},
        format="json",
    )

    response = view(request, pk=bon.pk)

    assoc_1.refresh_from_db()
    assoc_2.refresh_from_db()
    stock_1.refresh_from_db()
    stock_2.refresh_from_db()

    assert response.status_code == 200
    assert response.content == b'{"ok": true}'

    assert assoc_1.estConfirme is False
    assert assoc_1.date_confirme is None
    assert assoc_1.magasin_reserve_id is None
    assert assoc_1.reservations.count() == 0
    assert stock_1.quantite == 5

    assert assoc_2.estConfirme is False
    assert assoc_2.date_confirme is None
    assert assoc_2.magasin_reserve_id is None
    assert stock_2.quantite == 1


@pytest.mark.django_db
def test_should_toggle_pieces_recuperees_and_recuperation_date(api_factory):
    bon = BonTravailFactory(pieces_recuperees=False, date_recuperation=None)

    view = BonTravailViewSet.as_view({"patch": "set_recupere"})

    request_true = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/set_recupere/",
        {"recupere": True},
        format="json",
    )
    response_true = view(request_true, pk=bon.pk)
    bon.refresh_from_db()

    assert response_true.status_code == 200
    assert bon.pieces_recuperees is True
    assert bon.date_recuperation is not None

    request_false = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/set_recupere/",
        {"recupere": False},
        format="json",
    )
    response_false = view(request_false, pk=bon.pk)
    bon.refresh_from_db()

    assert response_false.status_code == 200
    assert bon.pieces_recuperees is False
    assert bon.date_recuperation is None


@pytest.mark.django_db
def test_should_return_400_when_repartition_total_does_not_match_needed_quantity(api_factory):
    bon = BonTravailFactory()
    consommable = ConsommableFactory()
    BonTravailConsommable.objects.create(
        bon_travail=bon,
        consommable=consommable,
        quantite_utilisee=4,
    )
    magasin = Magasin.objects.create(nom="Magasin A")
    Stocker.objects.create(consommable=consommable, magasin=magasin, quantite=10)

    view = BonTravailViewSet.as_view({"patch": "update_consommable_distribution"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/update_consommable_distribution/",
        {
            "consommable_id": consommable.pk,
            "distribue": True,
            "repartition": [{"magasin_id": magasin.pk, "quantite": 3}],
        },
        format="json",
    )

    response = view(request, pk=bon.pk)

    assert response.status_code == 400
    assert "totaliser exactement 4" in response.data["error"]


@pytest.mark.django_db
def test_should_return_400_when_repartition_contains_duplicate_store(api_factory):
    bon = BonTravailFactory()
    consommable = ConsommableFactory()
    BonTravailConsommable.objects.create(
        bon_travail=bon,
        consommable=consommable,
        quantite_utilisee=4,
    )
    magasin = Magasin.objects.create(nom="Magasin A")
    Stocker.objects.create(consommable=consommable, magasin=magasin, quantite=10)

    view = BonTravailViewSet.as_view({"patch": "update_consommable_distribution"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/update_consommable_distribution/",
        {
            "consommable_id": consommable.pk,
            "distribue": True,
            "repartition": [
                {"magasin_id": magasin.pk, "quantite": 2},
                {"magasin_id": magasin.pk, "quantite": 2},
            ],
        },
        format="json",
    )

    response = view(request, pk=bon.pk)

    assert response.status_code == 400
    assert "une seule fois" in response.data["error"]


@pytest.mark.django_db
def test_should_return_400_when_repartition_quantity_is_not_positive(api_factory):
    bon = BonTravailFactory()
    consommable = ConsommableFactory()
    BonTravailConsommable.objects.create(
        bon_travail=bon,
        consommable=consommable,
        quantite_utilisee=2,
    )
    magasin = Magasin.objects.create(nom="Magasin A")
    Stocker.objects.create(consommable=consommable, magasin=magasin, quantite=10)

    view = BonTravailViewSet.as_view({"patch": "update_consommable_distribution"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/update_consommable_distribution/",
        {
            "consommable_id": consommable.pk,
            "distribue": True,
            "repartition": [{"magasin_id": magasin.pk, "quantite": 0}],
        },
        format="json",
    )

    response = view(request, pk=bon.pk)

    assert response.status_code == 400
    assert "strictement positive" in response.data["error"]


@pytest.mark.django_db
def test_should_apply_repartition_split_and_create_reservations(api_factory):
    bon = BonTravailFactory()
    consommable = ConsommableFactory()
    assoc = BonTravailConsommable.objects.create(
        bon_travail=bon,
        consommable=consommable,
        quantite_utilisee=5,
    )
    magasin_a = Magasin.objects.create(nom="Magasin A")
    magasin_b = Magasin.objects.create(nom="Magasin B")
    stock_a = Stocker.objects.create(consommable=consommable, magasin=magasin_a, quantite=4)
    stock_b = Stocker.objects.create(consommable=consommable, magasin=magasin_b, quantite=6)

    view = BonTravailViewSet.as_view({"patch": "update_consommable_distribution"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/update_consommable_distribution/",
        {
            "consommable_id": consommable.pk,
            "distribue": True,
            "repartition": [
                {"magasin_id": magasin_a.pk, "quantite": 2},
                {"magasin_id": magasin_b.pk, "quantite": 3},
            ],
        },
        format="json",
    )

    response = view(request, pk=bon.pk)
    assoc.refresh_from_db()
    stock_a.refresh_from_db()
    stock_b.refresh_from_db()

    assert response.status_code == 200
    assert assoc.estConfirme is True
    assert assoc.date_confirme is not None
    assert assoc.magasin_reserve_id is None
    assert stock_a.quantite == 2
    assert stock_b.quantite == 3
    assert assoc.reservations.count() == 2


@pytest.mark.django_db
def test_should_return_400_when_update_status_payload_has_no_statut(api_factory):
    bon = BonTravailFactory(statut="EN_ATTENTE")

    view = BonTravailViewSet.as_view({"patch": "updateStatus"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/updateStatus/",
        {},
        format="json",
    )

    response = view(request, pk=bon.pk)

    assert response.status_code == 400
    assert "statut" in response.data["error"]


@pytest.mark.django_db
def test_should_move_from_en_attente_to_en_cours_and_set_date_debut(api_factory):
    bon = BonTravailFactory(statut="EN_ATTENTE", date_debut=None)

    view = BonTravailViewSet.as_view({"patch": "updateStatus"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/updateStatus/",
        {"statut": "EN_COURS"},
        format="json",
    )

    response = view(request, pk=bon.pk)
    bon.refresh_from_db()

    assert response.status_code == 200
    assert bon.statut == "EN_COURS"
    assert bon.date_debut is not None


@pytest.mark.django_db
def test_should_return_400_when_refusing_closure_without_comment(api_factory):
    bon = BonTravailFactory(statut="TERMINE")

    view = BonTravailViewSet.as_view({"patch": "updateStatus"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/updateStatus/",
        {"statut": "EN_COURS"},
        format="json",
    )

    response = view(request, pk=bon.pk)

    assert response.status_code == 400
    assert "commentaire de refus" in response.data["error"]


@pytest.mark.django_db
def test_should_reopen_terminated_bt_with_refusal_comment(api_factory):
    bon = BonTravailFactory(
        statut="TERMINE",
        date_fin="2026-01-01T10:00:00Z",
        date_cloture="2026-01-01T11:00:00Z",
        commentaire_refus_cloture=None,
    )

    view = BonTravailViewSet.as_view({"patch": "updateStatus"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/updateStatus/",
        {"statut": "EN_COURS", "commentaire_refus_cloture": "Manque une verification"},
        format="json",
    )

    response = view(request, pk=bon.pk)
    bon.refresh_from_db()

    assert response.status_code == 200
    assert bon.statut == "EN_COURS"
    assert bon.date_fin is None
    assert bon.date_cloture is None
    assert bon.commentaire_refus_cloture == "Manque une verification"


@pytest.mark.django_db
def test_should_move_from_en_cours_to_termine_and_set_date_fin(api_factory):
    bon = BonTravailFactory(statut="EN_COURS", date_fin=None)

    view = BonTravailViewSet.as_view({"patch": "updateStatus"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/updateStatus/",
        {"statut": "TERMINE"},
        format="json",
    )

    response = view(request, pk=bon.pk)
    bon.refresh_from_db()

    assert response.status_code == 200
    assert bon.statut == "TERMINE"
    assert bon.date_fin is not None


@pytest.mark.django_db
def test_should_return_400_when_trying_to_finish_bt_not_in_progress(api_factory):
    bon = BonTravailFactory(statut="EN_ATTENTE")

    view = BonTravailViewSet.as_view({"patch": "updateStatus"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/updateStatus/",
        {"statut": "TERMINE"},
        format="json",
    )

    response = view(request, pk=bon.pk)

    assert response.status_code == 400
    assert "en cours" in response.data["error"]


@pytest.mark.django_db
def test_should_cloture_and_fill_date_fin_if_missing(api_factory):
    bon = BonTravailFactory(statut="TERMINE", date_fin=None, date_cloture=None)

    view = BonTravailViewSet.as_view({"patch": "updateStatus"})
    request = api_factory.patch(
        f"/api/maintenance/bons-travail/{bon.pk}/updateStatus/",
        {"statut": "CLOTURE"},
        format="json",
    )

    response = view(request, pk=bon.pk)
    bon.refresh_from_db()

    assert response.status_code == 200
    assert bon.statut == "CLOTURE"
    assert bon.date_cloture is not None
    assert bon.date_fin is not None