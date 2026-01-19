import logging
import datetime
from django.db import DatabaseError
from django.utils import timezone

from equipement.models import Compteur, Declencher
from maintenance.models import PlanMaintenance, DemandeIntervention, BonTravail, BonTravailConsommable
from utilisateur.models import Utilisateur

logger = logging.getLogger('tasks')

ALERT_THRESHOLD = 0.85


def update_counter():
    try:
        counters = Compteur.objects.all()
        counters_on_alert = 0
        BT_created = 0

        # Attempt to get a default system user or admin for auto-generated requests
        # In a real scenario, you might have a dedicated 'system' user.
        system_user = Utilisateur.objects.filter(role__nomRole__icontains='Responsable GMAO').first()
        if not system_user:
            system_user = Utilisateur.objects.first()

        for counter in counters:
            if counter.valeurCourante is None:
                logger.warning(f"Counter {counter.id} ignoré (valeurCourante nulle)")
                continue

            # Récupérer les déclenchements associés (table declencher)
            declenchements = counter.declenchements.all()

            for declencher in declenchements:
                # Récupérer le plan de maintenance associé
                plan_maintenance = declencher.planMaintenance

                if (
                    declencher.derniereIntervention is None
                    or declencher.ecartInterventions is None
                    or declencher.prochaineMaintenance is None
                ): continue

                since_last = counter.valeurCourante - declencher.derniereIntervention
                alert_value = ALERT_THRESHOLD * declencher.ecartInterventions

                # Debug log
                # msg = f"Counter {since_last}/{declencher.ecartInterventions} = {since_last/declencher.ecartInterventions}"
                # logger.info(msg)

                if since_last >= alert_value:
                    if plan_maintenance:

                        # Check if a BT already exists and is active for this PlanMaintenance
                        existing_bt = BonTravail.objects.filter(
                            demande_intervention__equipement=counter.equipement,
                            nom__icontains=plan_maintenance.nom,
                            statut__in=['EN_ATTENTE', 'EN_COURS', 'EN_RETARD']
                        ).exists()

                        if existing_bt: continue

                        if not system_user:
                             logger.error("Aucun utilisateur trouvé pour créer la demande d'intervention.")
                             continue

                        # Create DemandeIntervention
                        demande = DemandeIntervention.objects.create(
                            nom=f"Maintenance Préventive : {plan_maintenance.nom}",
                            statut='TRANSFORMEE', # Immediately transformed to BT
                            date_creation=timezone.now(),
                            date_changementStatut=timezone.now(),
                            utilisateur=system_user,
                            equipement=counter.equipement,
                            commentaire=f"Généré automatiquement par le compteur {counter.nomCompteur} (Valeur: {counter.valeurCourante})"
                        )

                        # Create BonTravail
                        bt = BonTravail.objects.create(
                            nom=f"Intervention : {plan_maintenance.nom}",
                            type='PREVENTIF',
                            statut='EN_ATTENTE',
                            demande_intervention=demande,
                            responsable=system_user,
                            commentaire=plan_maintenance.commentaire,
                            
                        )
                        
                        # Copy consumables with quantities
                        for pm_conso in plan_maintenance.planmaintenanceconsommable_set.all():
                            BonTravailConsommable.objects.create(
                                bon_travail=bt,
                                consommable=pm_conso.consommable,
                                quantite_utilisee=pm_conso.quantite_necessaire
                            )


                        BT_created += 1
                    counters_on_alert += 1

        logger.info(f"[{datetime.datetime.now().strftime('%Y-%m-%d')}] Compteurs en alerte: {counters_on_alert}; BonTravail crees: {BT_created}")

    except Exception as e:
        logger.exception("Erreur dans le cron update_counter")
