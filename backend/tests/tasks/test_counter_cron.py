import pytest
from django.utils import timezone

from tasks.counterCron import update_counter
from maintenance.models import DemandeIntervention, BonTravail
from tests.factories import (
    RoleFactory, 
    UtilisateurFactory, 
    EquipementFactory, 
    PlanMaintenanceFactory, 
    CompteurFactory, 
    DeclencherFactory,
    DemandeInterventionFactory,
    BonTravailFactory,
)

@pytest.mark.django_db
def test_should_create_bt_when_counter_reaches_85_percent():
    """
    Test la règle métier critique : 
    Si un compteur dépasse 85% de son seuil (ecartInterventions), 
    le système doit générer automatiquement une Demande d'Intervention et un Bon de Travail.
    """
    
    # ==========================================
    # GIVEN (Arrangement des données)
    # ==========================================
    # 1. Utilisateur système (requis par le script)
    role_resp = RoleFactory(nomRole="Responsable GMAO")
    admin = UtilisateurFactory(role=role_resp)
    
    # 2. Equipement et plan de maintenance
    equipement = EquipementFactory(designation="Moteur Principal")
    plan = PlanMaintenanceFactory(nom="Graissage Roulements", equipement=equipement)
    
    # 3. Compteur simulé à 86% du seuil (86 unités sur un seuil de 100)
    compteur = CompteurFactory(equipement=equipement, valeurCourante=86.0)
    
    # 4. Paramétrage du déclenchement
    DeclencherFactory(
        compteur=compteur,
        planMaintenance=plan,
        derniereIntervention=0,
        ecartInterventions=100.0,      # Le seuil à atteindre est 100
        prochaineMaintenance=100.0
    )

    # ==========================================
    # WHEN (Action exercée)
    # ==========================================
    # On déclenche manuellement la tâche CRON
    update_counter()

    # ==========================================
    # THEN (Vérification des conséquences)
    # ==========================================
    
    # 1. Vérification de la Demande d'Intervention (DI)
    di = DemandeIntervention.objects.filter(equipement=equipement).first()
    assert di is not None, "Une demande d'intervention aurait dû être créée (86% > 85%)."
    assert "Graissage Roulements" in di.nom
    assert di.statut == 'TRANSFORMEE'
    assert di.utilisateur.id == admin.id

    # 2. Vérification du Bon de Travail (BT) automatiquement rattaché
    bt = BonTravail.objects.filter(demande_intervention=di).first()
    assert bt is not None, "Un bon de travail aurait dû être créé en même temps que la DI."
    assert "Graissage Roulements" in bt.nom
    assert bt.type == 'PREVENTIF'
    assert bt.statut == 'EN_ATTENTE'
    assert bt.responsable.id == admin.id


@pytest.mark.django_db
def test_should_not_create_duplicate_bt_when_active_bt_exists():
    """
    Si un BT actif (EN_ATTENTE, EN_COURS ou EN_RETARD) existe déjà pour ce
    plan de maintenance, un deuxième appel à update_counter() ne doit pas
    créer de nouvelles DI/BT.
    """
    # GIVEN
    role_resp = RoleFactory(nomRole="Responsable GMAO")
    UtilisateurFactory(role=role_resp)

    equipement = EquipementFactory()
    plan = PlanMaintenanceFactory(nom="Vidange Huile", equipement=equipement)
    compteur = CompteurFactory(equipement=equipement, valeurCourante=90.0)
    DeclencherFactory(
        compteur=compteur,
        planMaintenance=plan,
        derniereIntervention=0,
        ecartInterventions=100.0,
        prochaineMaintenance=100.0,
    )

    # Un premier appel crée le BT
    update_counter()
    assert BonTravail.objects.filter(
        demande_intervention__equipement=equipement
    ).count() == 1

    # WHEN — deuxième appel
    update_counter()

    # THEN — toujours 1 seul BT, pas de doublon
    assert BonTravail.objects.filter(
        demande_intervention__equipement=equipement
    ).count() == 1


@pytest.mark.django_db
def test_should_not_create_bt_when_counter_is_below_threshold():
    """
    Si le compteur est sous 85% du seuil, aucune DI ni BT ne doit être créé.
    """
    # GIVEN
    role_resp = RoleFactory(nomRole="Responsable GMAO")
    UtilisateurFactory(role=role_resp)

    equipement = EquipementFactory()
    plan = PlanMaintenanceFactory(nom="Contrôle Filtre", equipement=equipement)
    # 50 unités sur un seuil de 100 = 50% < 85%
    compteur = CompteurFactory(equipement=equipement, valeurCourante=50.0)
    DeclencherFactory(
        compteur=compteur,
        planMaintenance=plan,
        derniereIntervention=0,
        ecartInterventions=100.0,
        prochaineMaintenance=100.0,
    )

    # WHEN
    update_counter()

    # THEN — aucune DI ni BT créé
    assert DemandeIntervention.objects.filter(equipement=equipement).count() == 0
    assert BonTravail.objects.count() == 0
