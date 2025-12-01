from django.contrib import admin

from .models import *

admin.site.register(Equipement)
admin.site.register(FamilleEquipement)
admin.site.register(ModeleEquipement)
admin.site.register(StatutEquipement)
admin.site.register(Compteur)