"""
Settings de test : surcharge la base de données MySQL par SQLite en mémoire
pour permettre l'exécution des tests sans Docker ni serveur MySQL.
"""
from .settings import *  # noqa: F401, F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Désactiver les logs CRON pendant les tests
CRONTAB_COMMAND_SUFFIX = ''
