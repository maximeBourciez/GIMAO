import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from donnees.models import Document, TypeDocument
from equipement.models import Constituer, Declencher, DocumentEquipement
from tests.factories import CompteurFactory, ConsommableFactory, EquipementFactory


@pytest.mark.django_db
def test_should_convert_ordinal_to_iso_string_and_fallback_for_invalid_value():
    compteur = CompteurFactory(type="Calendaire")
    declenchement = Declencher.objects.create(
        compteur=compteur,
        planMaintenance=None,
        derniereIntervention=739000,
        prochaineMaintenance=739010,
        ecartInterventions=5,
        estGlissant=False,
    )

    assert declenchement.ordinalToISOString(739000).count("-") == 2
    assert declenchement.ordinalToISOString("not-a-number") == "—"


@pytest.mark.django_db
def test_should_render_declencher_string_for_calendaire_counter():
    compteur = CompteurFactory(type="Calendaire", nomCompteur="Compteur Date", unite="jours")
    declenchement = Declencher.objects.create(
        compteur=compteur,
        planMaintenance=None,
        derniereIntervention=739000,
        prochaineMaintenance=739010,
        ecartInterventions=5,
        estGlissant=True,
    )

    result = str(declenchement)

    assert "Compteur Date" in result
    assert "Glissant: Oui" in result
    assert "Seuil:" in result


@pytest.mark.django_db
def test_should_render_declencher_string_for_non_calendaire_counter():
    compteur = CompteurFactory(type="General", nomCompteur="Compteur Heures", unite="h")
    declenchement = Declencher.objects.create(
        compteur=compteur,
        planMaintenance=None,
        derniereIntervention=10,
        prochaineMaintenance=40,
        ecartInterventions=15,
        estGlissant=False,
    )

    result = str(declenchement)

    assert "Compteur Heures" in result
    assert "Seuil: 40" in result
    assert "Glissant: Non" in result


@pytest.mark.django_db
def test_should_render_constituer_string_with_equipment_and_consommable_ids():
    equipement = EquipementFactory()
    consommable = ConsommableFactory()

    constituer = Constituer.objects.create(equipement=equipement, consommable=consommable)

    result = str(constituer)

    assert f"Equipement {equipement.id}" in result
    assert f"Consommable {consommable.id}" in result


@pytest.mark.django_db
def test_should_render_document_equipement_string_with_ids():
    equipement = EquipementFactory()
    type_document = TypeDocument.objects.create(nomTypeDocument="Notice")
    document = Document.objects.create(
        nomDocument="Doc equipement",
        cheminAcces=SimpleUploadedFile("equip_doc.txt", b"abc", content_type="text/plain"),
        typeDocument=type_document,
    )

    association = DocumentEquipement.objects.create(equipement=equipement, document=document)

    result = str(association)

    assert f"Equipement {equipement.id}" in result
    assert f"Document {document.id}" in result
