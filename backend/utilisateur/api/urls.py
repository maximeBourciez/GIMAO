from django.urls import path, include
from rest_framework.routers import DefaultRouter
from utilisateur.api.viewsets import (
    RoleViewSet,
    UtilisateurViewSet,
    LogViewSet,
)

# Créer le router
router = DefaultRouter()

# Enregistrer les ViewSets
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'utilisateurs', UtilisateurViewSet, basename='utilisateur')
router.register(r'logs', LogViewSet, basename='log')

# URLs
urlpatterns = [
    path('', include(router.urls)),
]