from django.urls import path, include
from rest_framework.routers import DefaultRouter
from equipement.api.viewsets import (
    EquipementViewSet,
    StatutEquipementViewSet,
    ConstituerViewSet,
    ModeleEquipementViewSet,
    CompteurViewSet,
    FamilleEquipementViewSet,
)

router = DefaultRouter()
router.register(r'equipements', EquipementViewSet, basename='equipement')
router.register(r'statut-equipements', StatutEquipementViewSet, basename='statut-equipement')
router.register(r'constituer', ConstituerViewSet, basename='constituer')
router.register(r'modele-equipements', ModeleEquipementViewSet, basename='modele-equipement')
router.register(r'compteurs', CompteurViewSet, basename='compteur')
router.register(r'famille-equipements', FamilleEquipementViewSet, basename='famille-equipement')

urlpatterns = [
    path('', include(router.urls)),
]
