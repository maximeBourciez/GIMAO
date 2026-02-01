from django.contrib import admin
from django.contrib import messages
from django.utils.crypto import get_random_string
from .models import Role, Utilisateur, Log , Permission, RolePermission


class RoleAdmin(admin.ModelAdmin):
    list_display = ('nomRole', 'rang')
    list_filter = ('rang',)
    search_fields = ('nomRole',)
    ordering = ('rang',)


class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('nomUtilisateur', 'prenom', 'nomFamille', 'email', 'role', 'actif', 'a_mot_de_passe', 'derniereConnexion')
    list_filter = ('actif', 'role', 'dateCreation')
    search_fields = ('nomUtilisateur', 'prenom', 'nomFamille', 'email')
    readonly_fields = ('dateCreation', 'derniereConnexion', 'a_mot_de_passe')
    ordering = ('nomFamille', 'prenom')
    
    fieldsets = (
        ('Informations de connexion', {
            'fields': ('nomUtilisateur', 'email', 'role')
        }),
        ('Informations personnelles', {
            'fields': ('prenom', 'nomFamille')
        }),
        ('Statut du compte', {
            'fields': ('actif', 'a_mot_de_passe', 'derniereConnexion', 'dateCreation')
        }),
    )
    
    add_fieldsets = (
        ('Informations de connexion', {
            'fields': ('nomUtilisateur', 'email', 'role')
        }),
        ('Informations personnelles', {
            'fields': ('prenom', 'nomFamille')
        }),
        ('Statut du compte', {
            'fields': ('actif',)
        }),
    )
    
    def a_mot_de_passe(self, obj):
        """Indique si l'utilisateur a défini un mot de passe"""
        return obj.has_usable_password()
    a_mot_de_passe.boolean = True
    a_mot_de_passe.short_description = 'Mot de passe défini'
    
    def save_model(self, request, obj, form, change):
        """
        Surcharge pour créer des utilisateurs SANS mot de passe.
        L'utilisateur devra le définir à sa première connexion.
        """
        if not change:  # Si c'est une création
            # Ne définit PAS de mot de passe, laisse à None
            obj.motDePasse = None
            
            # Sauvegarde l'utilisateur
            super().save_model(request, obj, form, change)
            
            # Message d'information
            messages.success(
                request,
                f"Utilisateur '{obj.nomUtilisateur}' créé avec succès ! "
                f"L'utilisateur devra définir son mot de passe lors de sa première connexion."
            )
        else:
            # Si c'est une modification, sauvegarde normalement
            super().save_model(request, obj, form, change)
    
    def get_fieldsets(self, request, obj=None):
        """
        Retourne des fieldsets différents pour la création et la modification
        """
        if not obj:  # Si c'est une création
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


class LogAdmin(admin.ModelAdmin):
    list_display = ('type', 'nomTable', 'date', 'utilisateur')
    list_filter = ('type', 'nomTable', 'date')
    search_fields = ('type', 'nomTable')
    readonly_fields = ('type', 'nomTable', 'idCible', 'champsModifies', 'date', 'utilisateur')
    ordering = ('-date',)
    
    def has_add_permission(self, request):
        """Les logs ne peuvent pas être créés manuellement"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Les logs ne peuvent pas être modifiés"""
        return False
    
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('nomPermission', 'description')
    search_fields = ('nomPermission',)
    ordering = ('nomPermission',)

class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission')
    list_filter = ('role',)
    search_fields = ('role__nomRole', 'permission__nomPermission')
    ordering = ('role', 'permission')


admin.site.register(Role, RoleAdmin)
admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(RolePermission, RolePermissionAdmin)