from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch, Q
from django.utils import timezone
from django.db import transaction
import json
from donnees.models import Document
from equipement.models import Equipement
from utilisateur.models import Utilisateur, Log
from maintenance.models import DemandeIntervention, BonTravail, Utilisateur



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

    @action(detail=True, methods=['patch'])
    def delink_document(self, request, pk=None):
        demande = self.get_object()
        document_id = request.data.get('document_id')
        
        if not document_id:
            document_id = request.query_params.get('document_id')
            
        if not document_id:
            return Response(
                {'error': 'Le paramètre document_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Vérification si le document est bien lié à la demande
        if not demande.documents.filter(id=document_id).exists():
            return Response(
                {'error': 'Ce document n\'est pas lié à cette demande'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        demande.documents.remove(document_id)
        
        # On utilise le serializer détaillé pour renvoyer la liste des documents mise à jour
        serializer = DemandeInterventionDetailSerializer(demande, context={'request': request})
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
    - GET /bons-travail/mes_bons/ : Bons assignés à l'utilisateur connecté
    - PATCH /bons-travail/{id}/updateStatus/ : Change le statut (endpoint unique)
    """
    queryset = BonTravail.objects.select_related(
        'demande_intervention',
        'demande_intervention__equipement',
        'responsable'
    ).prefetch_related('utilisateur_assigne')
    serializer_class = BonTravailSerializer

    def _create_log_entry(self, type_action, nom_table, id_cible, champs_modifies, utilisateur_id=None):
        """Crée une entrée de log"""
        Log.objects.create(
            type=type_action,
            nomTable=nom_table,
            idCible=id_cible,
            champsModifies=champs_modifies,
            utilisateur_id=utilisateur_id
        )

    def _build_champs_modifies(self, bon_avant, bon_apres, fields):
        def _to_json_value(value):
            if value is None:
                return None
            if hasattr(value, 'isoformat'):
                return value.isoformat()
            return value

        champs = {}
        for field in fields:
            avant = getattr(bon_avant, field, None)
            apres = getattr(bon_apres, field, None)
            if avant != apres:
                champs[field] = {
                    'ancien': _to_json_value(avant),
                    'nouveau': _to_json_value(apres)
                }
        return champs

    def get_serializer_class(self):
        """Utilise le serializer détaillé pour retrieve"""
        if self.action == 'retrieve':
            return BonTravailDetailSerializer
        return BonTravailSerializer

    def get_queryset(self):
        """Par défaut, on n'affiche pas les BT clôturés.

        Query param: cloture (optionnel)
        - cloture=true (ou 1) => inclut les BT au statut CLOTURE
        """
        queryset = super().get_queryset()

        if getattr(self, 'action', None) != 'list':
            return queryset

        cloture_raw = str(self.request.query_params.get('cloture', 'false')).strip().lower()
        include_cloture = cloture_raw in ['true', '1']
        if include_cloture:
            return queryset

        return queryset.exclude(statut='CLOTURE')

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

    @action(detail=True, methods=['patch'])
    @transaction.atomic
    def updateStatus(self, request, pk=None):
        """Endpoint unique pour gérer les changements de statut d'un bon de travail.

        Payload attendu: {"statut": "EN_COURS"|"TERMINE"|"CLOTURE"|...}
        - EN_COURS (démarrer): date_debut = now
        - TERMINE (terminer): date_fin = now
        - CLOTURE (clôturer): date_cloture = now (et date_fin si manquante)
        """
        bon = self.get_object()
        new_statut = request.data.get('statut')
        if not new_statut:
            return Response(
                {'error': 'Le champ statut est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        utilisateur_id = request.data.get('user')

        bon_avant = BonTravail.objects.get(pk=bon.pk)

        # Règles spécifiques (on étendra au fur et à mesure)
        if new_statut == 'EN_COURS':
            # Deux cas :
            # - Démarrage: EN_ATTENTE/EN_RETARD -> EN_COURS (date_debut = now)
            # - Refus de clôture: TERMINE -> EN_COURS (date_fin = null + commentaire_refus_cloture)
            if bon.statut in ['EN_ATTENTE', 'EN_RETARD']:
                bon.statut = 'EN_COURS'
                bon.date_debut = timezone.now()
            elif bon.statut == 'TERMINE':
                commentaire_refus_cloture = request.data.get('commentaire_refus_cloture')
                if not commentaire_refus_cloture or not str(commentaire_refus_cloture).strip():
                    return Response(
                        {'error': 'Le commentaire de refus de clôture est requis'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                bon.statut = 'EN_COURS'
                bon.date_fin = None
                bon.date_cloture = None
                bon.commentaire_refus_cloture = str(commentaire_refus_cloture).strip()
            else:
                return Response(
                    {'error': 'Le bon doit être en attente, en retard ou terminé pour passer en cours'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif new_statut == 'TERMINE':
            # Terminer l'intervention (date_fin = now)
            if bon.statut != 'EN_COURS':
                return Response(
                    {'error': 'Le bon doit être en cours pour être terminé'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            bon.statut = 'TERMINE'
            bon.date_fin = timezone.now()
        elif new_statut == 'CLOTURE':
            # Clôturer le bon de travail
            bon.statut = 'CLOTURE'
            bon.date_cloture = timezone.now()
            if not bon.date_fin:
                bon.date_fin = timezone.now()
        else:
            bon.statut = new_statut

        bon.save()

        champs_modifies = self._build_champs_modifies(
            bon_avant,
            bon,
            fields=['statut', 'date_debut', 'date_fin', 'date_cloture', 'commentaire_refus_cloture']
        )
        if champs_modifies:
            self._create_log_entry(
                type_action='modification',
                nom_table='bon_travail',
                id_cible={'bon_travail_id': bon.id},
                champs_modifies=champs_modifies,
                utilisateur_id=utilisateur_id
            )

        serializer = self.get_serializer(bon)
        return Response(serializer.data)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """Ajoute un log si le statut est modifié via PATCH /bons-travail/{id}/."""
        instance = self.get_object()
        bon_avant = BonTravail.objects.get(pk=instance.pk)
        response = super().partial_update(request, *args, **kwargs)

        # Recharger l'instance après save
        bon_apres = BonTravail.objects.get(pk=instance.pk)
        if 'statut' in request.data and bon_avant.statut != bon_apres.statut:
            utilisateur_id = request.data.get('user')
            champs_modifies = self._build_champs_modifies(
                bon_avant,
                bon_apres,
                fields=['statut', 'date_debut', 'date_fin', 'date_cloture', 'commentaire_refus_cloture']
            )
            if champs_modifies:
                self._create_log_entry(
                    type_action='modification',
                    nom_table='bon_travail',
                    id_cible={'bon_travail_id': bon_apres.id},
                    champs_modifies=champs_modifies,
                    utilisateur_id=utilisateur_id
                )

        return response


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




class DashboardStatsViewset(viewsets.ViewSet):

    def list(self, request):
        role = request.query_params.get("role")
        user_id = request.query_params.get("userId")

        if not role:
            return Response({"detail": "role is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        stats = []

        if role == "Responsable GMAO":
            stats = [
                {"label": "Nombre de DI", "value": DemandeIntervention.objects.count()},
                {"label": "DI en attente", "value": DemandeIntervention.objects.filter(statut="EN_ATTENTE").count()},
                {"label": "DI acceptés", "value": DemandeIntervention.objects.filter(statut="ACCEPTEE").count()},
                {"label": "Nombre de BT", "value": BonTravail.objects.count()},
                {"label": "BT en retard", "value": BonTravail.objects.filter(statut="EN_RETARD").count()},
                {"label": "BT en cours", "value": BonTravail.objects.filter(statut="EN_COURS").count()},
            ]

        elif role in ["Technicien", "Opérateur"]:
            if not user_id:
                return Response({"detail": "userId is required"},
                                status=status.HTTP_400_BAD_REQUEST)

            user = Utilisateur.objects.filter(pk=user_id).first()
            if not user:
                return Response({"detail": "Utilisateur not found"},
                                status=status.HTTP_404_NOT_FOUND)

            if role == "Technicien":
                bt = BonTravail.objects.filter(utilisateur_assigne=user)
                stats = [
                    {"label": "Vos BT", "value": bt.count()},
                    {"label": "Vos BT en cours", "value": bt.filter(statut="EN_COURS").count()},
                    {"label": "Vos BT terminés", "value": bt.filter(statut="TERMINE").count()},
                ]

            if role == "Opérateur":
                di = DemandeIntervention.objects.filter(utilisateur=user)
                stats = [
                    {"label": "Vos BT", "value": BonTravail.objects.filter(demande_intervention__utilisateur=user).count()},
                    {"label": "Vos DI en attente", "value": di.filter(statut="EN_ATTENTE").count()},
                    {"label": "Vos DI acceptées", "value": di.filter(statut="ACCEPTEE").count()},
                ]

        else:
            return Response({"detail": "Invalid role"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"stats": stats}, status=status.HTTP_200_OK)
