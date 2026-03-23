import datetime

import pytest

from tasks.updateCalendarDates import update_calendar_counters
from tests.factories import CompteurFactory, EquipementFactory


@pytest.mark.django_db
def test_should_print_message_and_exit_when_no_calendary_counter(capsys):
    update_calendar_counters()

    captured = capsys.readouterr()
    assert "Aucun compteur calendaire trouvé." in captured.out


@pytest.mark.django_db
def test_should_update_only_active_calendary_counters_to_elapsed_days():
    active_equipement = EquipementFactory(archive=False)
    archived_equipement = EquipementFactory(archive=True)

    cal_active_1 = CompteurFactory(
        equipement=active_equipement,
        type="Calendaire",
        valeurCourante=10.0,
    )
    cal_active_2 = CompteurFactory(
        equipement=active_equipement,
        type="Calendaire",
        valeurCourante=20.0,
    )
    cal_archived = CompteurFactory(
        equipement=archived_equipement,
        type="Calendaire",
        valeurCourante=30.0,
    )
    non_cal = CompteurFactory(
        equipement=active_equipement,
        type="Heures",
        valeurCourante=40.0,
    )

    update_calendar_counters()

    expected_days = (datetime.datetime.now() - datetime.datetime(1, 1, 1)).days

    cal_active_1.refresh_from_db()
    cal_active_2.refresh_from_db()
    cal_archived.refresh_from_db()
    non_cal.refresh_from_db()

    assert cal_active_1.valeurCourante == expected_days
    assert cal_active_2.valeurCourante == expected_days
    assert cal_archived.valeurCourante == 30.0
    assert non_cal.valeurCourante == 40.0


@pytest.mark.django_db
def test_should_print_success_summary_after_bulk_update(capsys):
    equipement = EquipementFactory(archive=False)
    CompteurFactory(equipement=equipement, type="Calendaire", valeurCourante=0.0)
    CompteurFactory(equipement=equipement, type="Calendaire", valeurCourante=0.0)

    update_calendar_counters()

    captured = capsys.readouterr()
    assert "Nombre de compteurs à mettre à jour: 2" in captured.out
    assert "compteur(s) calendaire(s) mis à jour avec succès" in captured.out
