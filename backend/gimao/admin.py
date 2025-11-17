from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
     Role, Avoir, Fabricant, Fournisseur, Consommable,
    StockConsommable, ModeleEquipement, EstCompatible, Lieu, Equipement,
    Constituer, InformationStatut, DocumentTechnique, Correspondre,
    Defaillance, DocumentDefaillance, Intervention, DocumentIntervention
)
admin.site.register(Role)
admin.site.register(Avoir)
admin.site.register(Fabricant)
admin.site.register(Fournisseur)
admin.site.register(Consommable)
admin.site.register(StockConsommable)
admin.site.register(ModeleEquipement)
admin.site.register(EstCompatible)
admin.site.register(Lieu)
admin.site.register(Equipement)
admin.site.register(Constituer)
admin.site.register(InformationStatut)
admin.site.register(DocumentTechnique)
admin.site.register(Correspondre)
admin.site.register(Defaillance)
admin.site.register(DocumentDefaillance)
admin.site.register(Intervention)
admin.site.register(DocumentIntervention)
