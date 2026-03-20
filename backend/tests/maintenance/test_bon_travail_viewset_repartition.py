from rest_framework.test import APIRequestFactory

from maintenance.api.viewsets import BonTravailViewSet


def _build_request(viewset, payload):
    raw_request = APIRequestFactory().patch(
        "/api/bons-travail/1/update_consommable_distribution/",
        payload,
        format="json",
    )
    viewset.action_map = {"patch": "update_consommable_distribution"}
    return viewset.initialize_request(raw_request)


def test_should_return_none_when_repartition_field_is_missing():
    """
    Si le champ repartition est absent, _extract_repartition() doit renvoyer None.
    """
    viewset = BonTravailViewSet()
    request = _build_request(
        viewset,
        {
            "consommable_id": 12,
            "distribue": True,
            "magasin_id": 4,
        },
    )

    assert viewset._extract_repartition(request) is None


def test_should_keep_explicit_repartition_json_split():
    """
    Si le payload contient une repartition explicite, _extract_repartition()
    doit la conserver telle quelle.
    """
    viewset = BonTravailViewSet()
    repartition = [{"magasin_id": 4, "quantite": 3}]
    request = _build_request(
        viewset,
        {
            "consommable_id": 12,
            "distribue": True,
            "repartition": repartition,
        },
    )

    assert viewset._extract_repartition(request) == repartition
