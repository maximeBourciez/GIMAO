from django.contrib import admin

from .models import *

class BonTravailDocumentInline(admin.TabularInline):
	model = BonTravailDocument
	extra = 0


class BonTravailConsommableInline(admin.TabularInline):
	model = BonTravailConsommable
	extra = 0


@admin.register(BonTravail)
class BonTravailAdmin(admin.ModelAdmin):
	inlines = [BonTravailDocumentInline, BonTravailConsommableInline]

admin.site.register(BonTravailDocument)
admin.site.register(BonTravailConsommable)

admin.site.register(TypePlanMaintenance)
admin.site.register(PlanMaintenance)
admin.site.register(DemandeIntervention)
admin.site.register(PlanMaintenanceConsommable)
admin.site.register(PlanMaintenanceDocument)
admin.site.register(DemandeInterventionDocument)