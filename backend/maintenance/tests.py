from django.test import TestCase
from rest_framework.test import APIRequestFactory

from maintenance.api.viewsets import BonTravailViewSet


class BonTravailViewSetRepartitionExtractionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.viewset = BonTravailViewSet()

    def _build_request(self, payload):
        raw_request = self.factory.patch(
            '/api/bons-travail/1/update_consommable_distribution/',
            payload,
            format='json'
        )
        return self.viewset.initialize_request(raw_request)

    def test_extract_repartition_returns_none_when_field_is_missing(self):
        request = self._build_request({
            'consommable_id': 12,
            'distribue': True,
            'magasin_id': 4,
        })

        self.assertIsNone(self.viewset._extract_repartition(request))

    def test_extract_repartition_keeps_explicit_json_split(self):
        repartition = [{'magasin_id': 4, 'quantite': 3}]
        request = self._build_request({
            'consommable_id': 12,
            'distribue': True,
            'repartition': repartition,
        })

        self.assertEqual(repartition, self.viewset._extract_repartition(request))
