from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch, Q
from django.utils import timezone
from django.db import transaction
import json
from donnees.models import Document
from equipement.models import Equipement
from utilisateur.models import Utilisateur

from maintenance.models import (
    DemandeIntervention,
    BonTravail,
    TypePlanMaintenance,
    PlanMaintenance,
    PlanMaintenanceConsommable,
    DemandeInterventionDocument
)
from maintenance.api.serializers import (
    DemandeInterventionSerializer,
    DemandeInterventionDetailSerializer,
    BonTravailSerializer,
    BonTravailDetailSerializer,
    TypePlanMaintenanceSerializer,
    PlanMaintenanceSerializer,
    PlanMaintenanceDetailSerializer,
    PlanMaintenanceConsommableSerializer
)


class DemandeInterventionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les demandes d'intervention.
    
    Liste des endpoints:
    - GET /demandes-intervention/ : Liste toutes les demandes
    - POST /demandes-intervention/ : Crée une nouvelle demande
    - GET /demandes-intervention/{id}/ : Détail d'une demande
    - PUT/PATCH /demandes-intervention/{id}/ : Modifie une demande
    - DELETE /demandes-intervention/{id}/ : Supprime une demande
    - GET /demandes-intervention/en_attente/ : Demandes non traitées
    - GET /demandes-intervention/traitees/ : Demandes traitées
    - GET /demandes-intervention/par_equipement/?equipement_id=X : Filtre par équipement
    - POST /demandes-intervention/{id}/traiter/ : Marque comme traitée
    """
    queryset = DemandeIntervention.objects.select_related(
        'utilisateur', 'equipement'
    ).prefetch_related('bons_travail')
    serializer_class = DemandeInterventionSerializer

    def get_serializer_class(self):
        """Utilise le serializer détaillé pour retrieve"""
        if self.action == 'retrieve':
            return DemandeInterventionDetailSerializer
        return DemandeInterventionSerializer

    @action(detail=False, methods=['get'])
    def en_attente(self, request):
        """Retourne les demandes d'intervention en attente de traitement"""
        demandes = self.queryset.filter(date_traitement__isnull=True)
        serializer = self.get_serializer(demandes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def traitees(self, request):
        """Retourne les demandes d'intervention traitées"""
        demandes = self.queryset.filter(date_traitement__isnull=False)
        serializer = self.get_serializer(demandes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def par_equipement(self, request):
        """
        Filtre les demandes par équipement
        Query param: equipement_id
        """
        equipement_id = request.query_params.get('equipement_id')
        if not equipement_id:
            return Response(
                {'error': 'Le paramètre equipement_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        demandes = self.queryset.filter(equipement_id=equipement_id)
        serializer = self.get_serializer(demandes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def traiter(self, request, pk=None):
        """Marque une demande comme traitée"""
        demande = self.get_object()
        demande.date_traitement = timezone.now()
        demande.save()
        serializer = self.get_serializer(demande)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def updateStatus(self, request, pk=None):
        demande = self.get_object()
        demande.statut = request.data.get('statut', demande.statut)
        demande.date_changementStatut = timezone.now()
        demande.save()
        serializer = self.get_serializer(demande)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def transform_to_bon_travail(self, request, *args, **kwargs):
        demande = self.get_object()
        print(demande, request.data.get('responsable'))

        # Création du bon de travail
        bon_travail = BonTravail.objects.create(
            demande_intervention=demande,
            nom=demande.nom,
            type="CORRECTIF",
            commentaire=demande.commentaire,
            responsable_id=request.data.get('responsable'),
            statut='EN_ATTENTE'
        )

        demande.statut = 'TRANSFORMEE'
        demande.date_changementStatut = timezone.now()
        demande.save()
        serializer = self.get_serializer(bon_travail)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Création d'une nouvelle demande d'intervention"""
        data = dict(request.data)

        # Extraire les valeurs uniques des listes
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        # Validation serializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Récupération de l'utilisateur
        utilisateur_id = data.get("utilisateur_id")
        utilisateur = None
        if utilisateur_id:
            try:
                utilisateur = Utilisateur.objects.get(id=utilisateur_id)
            except (Utilisateur.DoesNotExist, ValueError):
                pass
        
        if not utilisateur and request.user.is_authenticated:
            utilisateur = request.user
            
        if not utilisateur:
            return Response(
                {'error': 'Utilisateur non identifié'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Récupération de l'équipement
        equipement_id = data.get("equipement_id")
        try:
            equipement = Equipement.objects.get(id=equipement_id)
        except Equipement.DoesNotExist:
            return Response(
                {'error': 'Équipement invalide'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Création de la demande
        demande = DemandeIntervention.objects.create(
            nom=data["nom"],
            commentaire=data.get("commentaire", ""),
            statut="EN_ATTENTE",
            date_creation=timezone.now(),
            date_changementStatut=timezone.now(),
            utilisateur=utilisateur,
            equipement=equipement
        )

        # Gestion des documents
        documents_data = data.get("documents", [])
        if isinstance(documents_data, str):
            try:
                documents_data = json.loads(documents_data)
            except ValueError:
                documents_data = []

        if documents_data:
            for index, doc_data in enumerate(documents_data):
                if not isinstance(doc_data, dict):
                    continue
                
                type_doc_id = doc_data.get("typeDocument_id")
                if not type_doc_id:
                    continue

                # Récupération du fichier
                # On check 'document_{index}' (convention possible) ou directement dans data si parsé
                uploaded_file = request.FILES.get(f"document_{index}")
                if not uploaded_file:
                    # Fallback: check si 'cheminAcces' contient le fichier (si parsé par DRF)
                    file_obj = doc_data.get("cheminAcces")
                    if hasattr(file_obj, 'read'):
                        uploaded_file = file_obj

                if uploaded_file:
                    document = Document.objects.create(
                        nomDocument=doc_data.get("nomDocument", uploaded_file.name),
                        cheminAcces=uploaded_file,
                        typeDocument_id=type_doc_id
                    )
                    
                    DemandeInterventionDocument.objects.create(
                        demande_intervention=demande,
                        document=document
                    )

        return Response(
            DemandeInterventionSerializer(demande).data,
            status=status.HTTP_201_CREATED
        )


class BonTravailViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les bons de travail.
    
    Liste des endpoints:
    - GET /bons-travail/ : Liste tous les bons
    - POST /bons-travail/ : Crée un nouveau bon
    - GET /bons-travail/{id}/ : Détail d'un bon
    - PUT/PATCH /bons-travail/{id}/ : Modifie un bon
    - DELETE /bons-travail/{id}/ : Supprime un bon
    - GET /bons-travail/par_statut/?statut=EN_COURS : Filtre par statut
    - GET /bons-travail/par_type/?type=PREVENTIF : Filtre par type
    - GET /bons-travail/mes_bons/ : Bons assignés à l'utilisateur connecté
    - POST /bons-travail/{id}/cloturer/ : Clôture un bon
    - POST /bons-travail/{id}/demarrer/ : Démarre un bon
    - POST /bons-travail/{id}/annuler/ : Annule un bon
    """
    queryset = BonTravail.objects.select_related(
        'demande_intervention',
        'demande_intervention__equipement',
        'responsable'
    ).prefetch_related('utilisateur_assigne')
    serializer_class = BonTravailSerializer

    def get_serializer_class(self):
        """Utilise le serializer détaillé pour retrieve"""
        if self.action == 'retrieve':
            return BonTravailDetailSerializer
        return BonTravailSerializer

    @action(detail=False, methods=['get'])
    def par_statut(self, request):
        """
        Filtre les bons de travail par statut
        Query param: statut (EN_ATTENTE, EN_COURS, TERMINE, ANNULE, REFUSE)
        """
        statut = request.query_params.get('statut')
        if not statut:
            return Response(
                {'error': 'Le paramètre statut est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        bons = self.queryset.filter(statut=statut)
        serializer = self.get_serializer(bons, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def par_type(self, request):
        """
        Filtre les bons de travail par type
        Query param: type (CORRECTIF, PREVENTIF, AMELIORATIF)
        """
        type_bt = request.query_params.get('type')
        if not type_bt:
            return Response(
                {'error': 'Le paramètre type est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        bons = self.queryset.filter(type=type_bt)
        serializer = self.get_serializer(bons, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def mes_bons(self, request):
        """Retourne les bons de travail assignés à l'utilisateur connecté"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentification requise'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        bons = self.queryset.filter(
            Q(utilisateur_assigne=request.user) | Q(responsable=request.user)
        ).distinct()
        serializer = self.get_serializer(bons, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cloturer(self, request, pk=None):
        """Clôture un bon de travail"""
        bon = self.get_object()
        bon.statut = 'TERMINE'
        bon.date_cloture = timezone.now()
        if not bon.date_fin:
            bon.date_fin = timezone.now()
        bon.save()
        serializer = self.get_serializer(bon)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def demarrer(self, request, pk=None):
        """Démarre un bon de travail"""
        bon = self.get_object()
        if bon.statut == 'EN_ATTENTE':
            bon.statut = 'EN_COURS'
            bon.date_debut = timezone.now()
            bon.save()
            serializer = self.get_serializer(bon)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Le bon doit être en attente pour être démarré'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def annuler(self, request, pk=None):
        """Annule un bon de travail"""
        bon = self.get_object()
        commentaire = request.data.get('commentaire', '')
        bon.statut = 'ANNULE'
        bon.commentaire_refus_cloture = commentaire
        bon.save()
        serializer = self.get_serializer(bon)
        return Response(serializer.data)


class TypePlanMaintenanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les types de plans de maintenance.
    
    Liste des endpoints:
    - GET /types-plan-maintenance/ : Liste tous les types
    - POST /types-plan-maintenance/ : Crée un nouveau type
    - GET /types-plan-maintenance/{id}/ : Détail d'un type
    - PUT/PATCH /types-plan-maintenance/{id}/ : Modifie un type
    - DELETE /types-plan-maintenance/{id}/ : Supprime un type
    """
    queryset = TypePlanMaintenance.objects.all()
    serializer_class = TypePlanMaintenanceSerializer


class PlanMaintenanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les plans de maintenance.
    
    Liste des endpoints:
    - GET /plans-maintenance/ : Liste tous les plans
    - POST /plans-maintenance/ : Crée un nouveau plan
    - GET /plans-maintenance/{id}/ : Détail d'un plan
    - PUT/PATCH /plans-maintenance/{id}/ : Modifie un plan
    - DELETE /plans-maintenance/{id}/ : Supprime un plan
    - GET /plans-maintenance/par_equipement/?equipement_id=X : Filtre par équipement
    - GET /plans-maintenance/par_type/?type_id=X : Filtre par type
    - POST /plans-maintenance/{id}/ajouter_consommable/ : Ajoute un consommable
    - POST /plans-maintenance/{id}/retirer_consommable/ : Retire un consommable
    - POST /plans-maintenance/{id}/ajouter_document/ : Ajoute un document
    - POST /plans-maintenance/{id}/retirer_document/ : Retire un document
    """
    queryset = PlanMaintenance.objects.select_related(
        'type_plan_maintenance',
        'equipement',
        'compteur'
    ).prefetch_related('documents', 'consommables')
    serializer_class = PlanMaintenanceSerializer

    def get_serializer_class(self):
        """Utilise le serializer détaillé pour retrieve"""
        if self.action == 'retrieve':
            return PlanMaintenanceDetailSerializer
        return PlanMaintenanceSerializer

    @action(detail=False, methods=['get'])
    def par_equipement(self, request):
        """
        Filtre les plans de maintenance par équipement
        Query param: equipement_id
        """
        equipement_id = request.query_params.get('equipement_id')
        if not equipement_id:
            return Response(
                {'error': 'Le paramètre equipement_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plans = self.queryset.filter(equipement_id=equipement_id)
        serializer = self.get_serializer(plans, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def par_type(self, request):
        """
        Filtre les plans de maintenance par type
        Query param: type_id
        """
        type_id = request.query_params.get('type_id')
        if not type_id:
            return Response(
                {'error': 'Le paramètre type_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plans = self.queryset.filter(type_plan_maintenance_id=type_id)
        serializer = self.get_serializer(plans, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def ajouter_consommable(self, request, pk=None):
        """
        Ajoute un consommable au plan de maintenance
        Body: {"consommable_id": 1, "quantite_necessaire": 5}
        """
        plan = self.get_object()
        consommable_id = request.data.get('consommable_id')
        quantite = request.data.get('quantite_necessaire', 1)
        
        if not consommable_id:
            return Response(
                {'error': 'Le paramètre consommable_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier si l'association existe déjà
        assoc, created = PlanMaintenanceConsommable.objects.get_or_create(
            plan_maintenance=plan,
            consommable_id=consommable_id,
            defaults={'quantite_necessaire': quantite}
        )
        
        if not created:
            # Mettre à jour la quantité si l'association existe déjà
            assoc.quantite_necessaire = quantite
            assoc.save()
        
        serializer = PlanMaintenanceConsommableSerializer(assoc)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def retirer_consommable(self, request, pk=None):
        """
        Retire un consommable du plan de maintenance
        Body: {"consommable_id": 1}
        """
        plan = self.get_object()
        consommable_id = request.data.get('consommable_id')
        
        if not consommable_id:
            return Response(
                {'error': 'Le paramètre consommable_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            assoc = PlanMaintenanceConsommable.objects.get(
                plan_maintenance=plan,
                consommable_id=consommable_id
            )
            assoc.delete()
            return Response({'message': 'Consommable retiré avec succès'}, status=status.HTTP_204_NO_CONTENT)
        except PlanMaintenanceConsommable.DoesNotExist:
            return Response(
                {'error': 'Association non trouvée'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def ajouter_document(self, request, pk=None):
        """
        Ajoute un document au plan de maintenance
        Body: {"document_id": 1}
        """
        plan = self.get_object()
        document_id = request.data.get('document_id')
        
        if not document_id:
            return Response(
                {'error': 'Le paramètre document_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plan.documents.add(document_id)
        serializer = self.get_serializer(plan)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def retirer_document(self, request, pk=None):
        """
        Retire un document du plan de maintenance
        Body: {"document_id": 1}
        """
        plan = self.get_object()
        document_id = request.data.get('document_id')
        
        if not document_id:
            return Response(
                {'error': 'Le paramètre document_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        plan.documents.remove(document_id)
        serializer = self.get_serializer(plan)
        return Response(serializer.data)


class PlanMaintenanceConsommableViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les associations consommables/plans de maintenance.
    
    Liste des endpoints:
    - GET /plan-maintenance-consommables/ : Liste toutes les associations
    - POST /plan-maintenance-consommables/ : Crée une nouvelle association
    - GET /plan-maintenance-consommables/{id}/ : Détail d'une association
    - PUT/PATCH /plan-maintenance-consommables/{id}/ : Modifie une association
    - DELETE /plan-maintenance-consommables/{id}/ : Supprime une association
    """
    queryset = PlanMaintenanceConsommable.objects.select_related(
        'plan_maintenance', 'consommable'
    )
    serializer_class = PlanMaintenanceConsommableSerializer