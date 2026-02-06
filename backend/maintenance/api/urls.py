from django.urls import path, include
from rest_framework.routers import DefaultRouter
from maintenance.api.viewsets import (
    DemandeInterventionViewSet,
    BonTravailViewSet,
    TypePlanMaintenanceViewSet,
    PlanMaintenanceViewSet,
    PlanMaintenanceConsommableViewSet,
    DashboardStatsViewset
)

# Créer le router
router = DefaultRouter()

# Enregistrer les ViewSets
router.register(r'demandes-intervention', DemandeInterventionViewSet, basename='demande-intervention')
router.register(r'bons-travail', BonTravailViewSet, basename='bon-travail')
router.register(r'types-plan-maintenance', TypePlanMaintenanceViewSet, basename='type-plan-maintenance')
router.register(r'plans-maintenance', PlanMaintenanceViewSet, basename='plan-maintenance')
router.register(r'plan-maintenance-consommables', PlanMaintenanceConsommableViewSet, basename='plan-maintenance-consommable')

# URLs
urlpatterns = [
    path(
        'bons-travail/<int:pk>/update_consommable_distribution/',
        BonTravailViewSet.as_view({'patch': 'update_consommable_distribution'}),
        name='bon-travail-update-consommable-distribution',
    ),
    path('', include(router.urls)),
    path(
        "stats/",
        DashboardStatsViewset.as_view({'get': 'list'}),
        name="stats",
    ),
]
