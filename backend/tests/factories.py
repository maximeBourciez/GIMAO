import factory
from factory.django import DjangoModelFactory
from django.utils import timezone

from utilisateur.models import Role, Utilisateur
from equipement.models import Equipement, Compteur, ModeleEquipement, FamilleEquipement, Declencher
from donnees.models import Lieu, Fabricant, Fournisseur
from maintenance.models import PlanMaintenance, TypePlanMaintenance

# ==========================================
# UTILISATEUR & ROLES
# ==========================================

class RoleFactory(DjangoModelFactory):
    class Meta:
        model = Role
    
    nomRole = factory.Sequence(lambda n: f"Role_{n}")
    rang = 10


class UtilisateurFactory(DjangoModelFactory):
    class Meta:
        model = Utilisateur

    nomUtilisateur = factory.Sequence(lambda n: f"technicien_{n}")
    prenom = "Jean"
    nomFamille = "Dupont"
    email = factory.Sequence(lambda n: f"jean.dupont{n}@gimao.local")
    actif = True
    role = factory.SubFactory(RoleFactory)


# ==========================================
# REFERENTIEL DONNEES
# ==========================================

class LieuFactory(DjangoModelFactory):
    class Meta:
        model = Lieu
    nomLieu = factory.Sequence(lambda n: f"Atelier_{n}")

class FabricantFactory(DjangoModelFactory):
    class Meta:
        model = Fabricant
    nom = factory.Sequence(lambda n: f"Fabricant_{n}")

class FournisseurFactory(DjangoModelFactory):
    class Meta:
        model = Fournisseur
    nom = factory.Sequence(lambda n: f"Fournisseur_{n}")

class ModeleEquipementFactory(DjangoModelFactory):
    class Meta:
        model = ModeleEquipement
    nom = factory.Sequence(lambda n: f"Modele_{n}")
    fabricant = factory.SubFactory(FabricantFactory)

class FamilleEquipementFactory(DjangoModelFactory):
    class Meta:
        model = FamilleEquipement
    nom = factory.Sequence(lambda n: f"Famille_{n}")

# ==========================================
# EQUIPEMENTS & COMPTEURS
# ==========================================

class EquipementFactory(DjangoModelFactory):
    class Meta:
        model = Equipement

    designation = factory.Sequence(lambda n: f"Equipement_Test_{n}")
    lieu = factory.SubFactory(LieuFactory)
    modele = factory.SubFactory(ModeleEquipementFactory)
    famille = factory.SubFactory(FamilleEquipementFactory)
    fournisseur = factory.SubFactory(FournisseurFactory)
    fabricant = factory.SelfAttribute('modele.fabricant')
    createurEquipement = factory.SubFactory(UtilisateurFactory)


class CompteurFactory(DjangoModelFactory):
    class Meta:
        model = Compteur

    nomCompteur = factory.Sequence(lambda n: f"Compteur_{n}")
    valeurCourante = 0.0
    unite = "Heures"
    equipement = factory.SubFactory(EquipementFactory)


# ==========================================
# MAINTENANCE
# ==========================================

class TypePlanMaintenanceFactory(DjangoModelFactory):
    class Meta:
        model = TypePlanMaintenance
    libelle = factory.Sequence(lambda n: f"Type_Plan_{n}")

class PlanMaintenanceFactory(DjangoModelFactory):
    class Meta:
        model = PlanMaintenance
        
    nom = factory.Sequence(lambda n: f"Plan_Maintenance_{n}")
    equipement = factory.SubFactory(EquipementFactory)
    type_plan_maintenance = factory.SubFactory(TypePlanMaintenanceFactory)


class DeclencherFactory(DjangoModelFactory):
    class Meta:
        model = Declencher

    compteur = factory.SubFactory(CompteurFactory)
    planMaintenance = factory.SubFactory(PlanMaintenanceFactory)
    derniereIntervention = 0
    prochaineMaintenance = 100
    ecartInterventions = 100
    estGlissant = False
