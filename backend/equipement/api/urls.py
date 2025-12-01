from django.urls import path, include
from rest_framework.routers import DefaultRouter
from equipement.api.viewsets import (
    EquipementViewSet,
    StatutEquipementViewSet,
    ConstituerViewSet,
    EquipementAvecDernierStatutViewSet,
    EquipementDetailViewSet,
    EquipementAffichageViewSet,
    ModeleEquipementViewSet,    
)

router = DefaultRouter()
router.register(r'equipements', EquipementViewSet, basename='equipement')
router.register(r'information-statuts', StatutEquipementViewSet, basename='information-statut')
router.register(r'constituer', ConstituerViewSet, basename='constituer')
router.register(r'modele-equipements', ModeleEquipementViewSet, basename='modele-equipement')  


urlpatterns = [
    path('', include(router.urls)),
    
    # Routes spécifiques pour les affichages détaillés
    path('equipements-detail/', EquipementDetailViewSet.as_view({'get': 'list'}), name='equipement-detail-list'),
    path('equipements-detail/<str:reference>/', EquipementDetailViewSet.as_view({'get': 'retrieve'}), name='equipement-detail'),
    path('equipement/<str:reference>/avec-statut/', EquipementAvecDernierStatutViewSet.as_view({'get': 'retrieve'}), name='equipement-avec-statut'),
    path('equipement/<str:reference>/affichage/', EquipementAffichageViewSet.as_view({'get': 'retrieve'}), name='equipement-affichage'),
]
