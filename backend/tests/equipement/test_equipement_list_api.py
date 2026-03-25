import pytest
from rest_framework.test import APIClient

from tests.factories import EquipementFactory, LieuFactory, ModeleEquipementFactory


@pytest.mark.django_db
def test_equipement_list_returns_paginated_payload_when_page_is_provided():
    client = APIClient()

    for index in range(30):
        EquipementFactory(designation=f"Equipement {index:02d}")

    response = client.get("/api/equipements/", {"page": 1, "page_size": 10})

    assert response.status_code == 200
    payload = response.json()

    assert payload["count"] == 30
    assert len(payload["results"]) == 10
    assert payload["next"] is not None
    assert payload["previous"] is None


@pytest.mark.django_db
def test_equipement_list_keeps_legacy_array_response_without_page_param():
    client = APIClient()

    EquipementFactory()
    EquipementFactory()

    response = client.get("/api/equipements/")

    assert response.status_code == 200
    payload = response.json()

    assert isinstance(payload, list)
    assert len(payload) == 2


@pytest.mark.django_db
def test_equipement_list_supports_search_and_filters_with_pagination():
    client = APIClient()

    lieu_cible = LieuFactory(nomLieu="Atelier principal")
    lieu_autre = LieuFactory(nomLieu="Magasin")
    modele_cible = ModeleEquipementFactory(nom="Modele pompe")
    modele_autre = ModeleEquipementFactory(nom="Modele convoyeur")

    match = EquipementFactory(
        designation="Pompe de relevage",
        lieu=lieu_cible,
        modele=modele_cible,
    )
    EquipementFactory(
        designation="Pompe secondaire",
        lieu=lieu_autre,
        modele=modele_cible,
    )
    EquipementFactory(
        designation="Convoyeur principal",
        lieu=lieu_cible,
        modele=modele_autre,
    )

    response = client.get(
        "/api/equipements/",
        {
            "page": 1,
            "page_size": 10,
            "search": "Pompe",
            "lieu_ids": str(lieu_cible.id),
            "modele_ids": str(modele_cible.id),
        },
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["count"] == 1
    assert [item["id"] for item in payload["results"]] == [match.id]
