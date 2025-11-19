from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gestionDonnee.api.viewsets import (
    FabricantViewSet,
    FournisseurViewSet,
    ModeleEquipementViewSet,
    LieuViewSet,
    DocumentTechniqueViewSet,
    CorrespondreViewSet,
    get_lieux_hierarchy,
)

router = DefaultRouter()
router.register(r'fabricants', FabricantViewSet, basename='fabricant')
router.register(r'fournisseurs', FournisseurViewSet, basename='fournisseur')
router.register(r'modele-equipements', ModeleEquipementViewSet, basename='modele-equipement')
router.register(r'lieux', LieuViewSet, basename='lieu')
router.register(r'document-techniques', DocumentTechniqueViewSet, basename='document-technique')
router.register(r'correspondre', CorrespondreViewSet, basename='correspondre')

urlpatterns = [
    path('', include(router.urls)),
    
    # Route pour la hiérarchie des lieux
    path('lieux-hierarchy/', get_lieux_hierarchy, name='lieux-hierarchy'),
]
