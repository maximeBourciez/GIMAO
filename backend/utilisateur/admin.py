from django.contrib import admin

from .models import Role, Utilisateur, Log

admin.site.register(Role)
admin.site.register(Utilisateur)
admin.site.register(Log)