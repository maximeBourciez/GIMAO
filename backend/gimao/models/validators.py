from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError


# Validateur pour les numéros de téléphone
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Le numéro de téléphone doit être entré au format: '+999999999'. Jusqu'à 15 chiffres autorisés.")

# Valideur pour le champ 'niveau' dans la table 'Defaillance'.
def validate_niveau_de_defaillance(value):
    niveaux_valid = ["Critique", "Majeur", "Mineur"]
    
    if value not in niveaux_valid:
        raise ValidationError(f"Le niveau de défaillance doit être l'une des valeurs suivantes: {', '.join(niveaux_valid)}.")


def validate_etat_equipement(value):
    etat_valid = ["Rebuté", "En fonctionnement", "Dégradé", "A l'arrêt"]
    
    if value not in etat_valid:
        raise ValidationError(f"Le statut du modèle doit être l'une des valeurs suivantes :  {', '.join(etat_valid)}.")

