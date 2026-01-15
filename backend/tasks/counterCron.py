import logging
import datetime
from django.db import DatabaseError

from equipement.models import Compteur

logger = logging.getLogger('tasks')

ALERT_THRESHOLD = 0.85


def update_counter():
    logger.info("Cron exécuté à " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    try:
        counters = Compteur.objects.all()
        counters_on_alert = 0

        for counter in counters:
            if (
                counter.derniereIntervention is None
                or counter.valeurCourante is None
                or counter.ecartInterventions is None
            ):
                logger.warning(f"Counter {counter.id} ignoré (valeurs nulles)")
                continue

            since_last = counter.valeurCourante - counter.derniereIntervention
            alert_value = ALERT_THRESHOLD * counter.ecartInterventions

            if since_last >= alert_value:
                logger.info(
                    f"Counter {counter.id} "
                    f"(equipement={counter.equipement.designation}) "
                    f"proche maintenance"
                )
                counters_on_alert += 1

        logger.info(
            f"Total counters on alert: {counters_on_alert} / {counters.count()}"
        )

    except Exception as e:
        logger.exception("Erreur dans le cron update_counter")
