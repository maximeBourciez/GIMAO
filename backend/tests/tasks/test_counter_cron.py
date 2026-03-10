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
    DeclencherFactory
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
