from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bonTravail.api.viewsets import (
    InterventionViewSet,
    DocumentInterventionViewSet,
    InterventionAfficherViewSet,
)

router = DefaultRouter()
router.register(r'interventions', InterventionViewSet, basename='intervention')
router.register(r'document-interventions', DocumentInterventionViewSet, basename='document-intervention')

urlpatterns = [
    path('', include(router.urls)),
    
    # Route pour l'affichage détaillé d'une intervention
    path('intervention/<int:pk>/affichage/', InterventionAfficherViewSet.as_view({'get': 'retrieve'}), name='intervention-affichage'),
]
