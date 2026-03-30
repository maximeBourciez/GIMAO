
import pytest
from tests.factories import UtilisateurFactory, RoleFactory
from utilisateur.models import Utilisateur, Role

@pytest.mark.django_db
class TestUtilisateurModels:
    def test_role_creation(self):
        role = RoleFactory(nomRole='Administrateur')
        assert Role.objects.filter(nomRole='Administrateur').exists()
        assert 'Administrateur' in str(role)

    def test_utilisateur_creation(self):
        user = UtilisateurFactory(nomUtilisateur='t.user')
        assert Utilisateur.objects.filter(nomUtilisateur='t.user').exists()
        assert user.actif == True

