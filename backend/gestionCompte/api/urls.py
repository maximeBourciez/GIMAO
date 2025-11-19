from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gestionCompte.api.viewsets import UserViewSet, RoleViewSet, AvoirViewSet

router = DefaultRouter()
router.register(r'utilisateurs', UserViewSet, basename='utilisateur')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'avoir', AvoirViewSet, basename='avoir')

urlpatterns = [
    path('', include(router.urls)),
]
