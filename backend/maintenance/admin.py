from django.contrib import admin

from .models import *

admin.site.register(BonTravail)
admin.site.register(TypePlanMaintenance)
admin.site.register(PlanMaintenance)
admin.site.register(DemandeIntervention)
admin.site.register(PlanMaintenanceConsommable)
admin.site.register(PlanMaintenanceDocument)