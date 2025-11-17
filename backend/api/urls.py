# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    RoleViewSet,
    AvoirViewSet,
    FabricantViewSet,
    FournisseurViewSet,
    ConsommableViewSet,
    StockConsommableViewSet,
    ModeleEquipementViewSet,
    EstCompatibleViewSet,
    LieuViewSet,
    EquipementViewSet,
    ConstituerViewSet,
    InformationStatutViewSet,
    DocumentTechniqueViewSet,
    CorrespondreViewSet,
    DefaillanceViewSet,
    DocumentDefaillanceViewSet,
    InterventionViewSet,
    DocumentInterventionViewSet,

    EquipementAvecDernierStatutViewSet,
    EquipementDetailViewSet,
    get_lieux_hierarchy,
    EquipementAffichageViewSet,
    InterventionAfficherViewSet,
    DefaillanceAfficherViewSet,
)

router = DefaultRouter()
router.register(r'utilisateurs', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'avoir', AvoirViewSet)
router.register(r'fabricants', FabricantViewSet)
router.register(r'fournisseurs', FournisseurViewSet)
router.register(r'consommables', ConsommableViewSet)
router.register(r'stock-consommables', StockConsommableViewSet)
router.register(r'modele-equipements', ModeleEquipementViewSet)
router.register(r'est-compatibles', EstCompatibleViewSet)
router.register(r'lieux', LieuViewSet)
router.register(r'equipements', EquipementViewSet)
router.register(r'constituer', ConstituerViewSet)
router.register(r'information-statuts', InformationStatutViewSet)
router.register(r'document-techniques', DocumentTechniqueViewSet)
router.register(r'correspondre', CorrespondreViewSet)
router.register(r'defaillances', DefaillanceViewSet)
router.register(r'document-defaillances', DocumentDefaillanceViewSet)
router.register(r'interventions', InterventionViewSet)
router.register(r'document-interventions', DocumentInterventionViewSet)







urlpatterns = [
    path('', include(router.urls)),
    path('lieux-hierarchy/', get_lieux_hierarchy, name='lieux-hierarchy'),
    path('equipements-detail/', EquipementDetailViewSet.as_view({'get': 'list'}), name='equipement-detail-list'),
    path('equipement/<str:reference>/avec-statut/', EquipementAvecDernierStatutViewSet.as_view({'get': 'retrieve'}), name='equipement-avec-statut'),
    path('equipements-detail/<str:reference>/', EquipementDetailViewSet.as_view({'get': 'retrieve'}), name='equipement-detail'),
    path('equipement/<str:reference>/affichage/', EquipementAffichageViewSet.as_view({'get': 'retrieve'}), name='equipement-detail'),
    path('intervention/<int:pk>/affichage/', InterventionAfficherViewSet.as_view({'get': 'retrieve'}), name='intervention-detail'),
    path('defaillance/<int:pk>/affichage/', DefaillanceAfficherViewSet.as_view({'get': 'retrieve'}), name='defaillance-detail'),

]