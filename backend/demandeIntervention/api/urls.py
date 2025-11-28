from django.urls import path, include
from rest_framework.routers import DefaultRouter
from demandeIntervention.api.viewsets import (
    DefaillanceViewSet,
    DocumentDefaillanceViewSet,
    DefaillanceAfficherViewSet,
)

router = DefaultRouter()
router.register(r'defaillances', DefaillanceViewSet, basename='defaillance')
router.register(r'document-defaillances', DocumentDefaillanceViewSet, basename='document-defaillance')

urlpatterns = [
    path('', include(router.urls)),
    
    # Route pour l'affichage détaillé d'une défaillance
    path('defaillance/<int:pk>/affichage/', DefaillanceAfficherViewSet.as_view({'get': 'retrieve'}), name='defaillance-affichage'),
]
