from utilisateur.models import Role
from maintenance.models import TypePlanMaintenance
from donnees.models import TypeDocument

def create_initial_data():
    # Création des rôles par défaut
    roles = ['Responsable GMAO', 'Technicien','Magasinier', 'Opérateur' ]
    for role_name in roles:
        Role.objects.get_or_create(
            nomRole=role_name,
            defaults={'rang': 10 - (roles.index(role_name) * 2)}
        )

    # Création des types de plans de maintenance par défaut
    types_plan_maintenance = ['Préventive', 'Corrective']
    for type_name in types_plan_maintenance:
        TypePlanMaintenance.objects.get_or_create(libelle=type_name)

    # Création des types de documents par défaut
    types_document = [
        "Manuel d'utilisation",
        "Manuel de maintenance",
        "Notice technique",
        "Schéma technique",

        "Contrat de maintenance",
        "Garantie",

        "Procédure de maintenance",
        "Consigne de sécurité",

        "Rapport d'intervention",
        "Rapport de contrôle",

        "Certificat de conformité",

        "Devis / Facture"
    ]
    for doc_type in types_document:
        TypeDocument.objects.get_or_create(nomTypeDocument=doc_type)
