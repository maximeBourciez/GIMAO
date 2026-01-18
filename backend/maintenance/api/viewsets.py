import os
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
    PlanMaintenanceDocument,
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
        'equipement'
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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Création d'un nouveau plan de maintenance"""
        data = dict(request.data)

        print(data)

        # Extraire les valeurs uniques des listes
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        try:
            seuil_data = json.loads(data.get('seuil', '{}'))
            pm_data = seuil_data.get('planMaintenance', {})
        except (json.JSONDecodeError, TypeError):
            return Response(
                {"error": "Format JSON invalide pour le seuil ou le plan de maintenance"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try: 
            # Vérifier que type_id existe et n'est pas null
            type_id = pm_data.get('type_id')
            if not type_id:
                return Response(
                    {"error": "Le type de plan de maintenance est obligatoire"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Vérifier que equipment_id existe
            equipment_id = seuil_data.get('equipmentId') 
            if not equipment_id:
                return Response(
                    {"error": "L'équipement est obligatoire"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            plan = PlanMaintenance.objects.create(
                nom=pm_data.get('nom', ''),
                commentaire=pm_data.get('commentaire', ''),
                necessiteHabilitationElectrique=pm_data.get('necessiteHabilitationElectrique', False),
                necessitePermisFeu=pm_data.get('necessitePermisFeu', False),
                type_plan_maintenance_id=type_id, 
                equipement_id=equipment_id 
            )

            # Créer les consommables associés si fournis
            for consommable in pm_data.get('consommables', []):
                PlanMaintenanceConsommable.objects.create(
                    plan_maintenance=plan,
                    consommable_id=consommable.get('consommable_id'),
                    quantite_necessaire=consommable.get('quantite', 1)
                )

        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la création du plan de maintenance: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try: 
            from equipement.models import Declencher

            # Vérifier que compteur_id existe
            compteur_id = seuil_data.get('compteurId')
            if not compteur_id:
                return Response(
                    {"error": "Le compteur est obligatoire pour le déclenchement"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            Declencher.objects.create(
                derniereIntervention=seuil_data.get('derniereIntervention', 0),
                prochaineMaintenance=seuil_data.get('prochaineMaintenance', 0),
                ecartInterventions=seuil_data.get('ecartInterventions', 0),
                estGlissant=seuil_data.get('estGlissant', False),
                compteur_id=compteur_id,
                planMaintenance=plan
            )

        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la création du seuil de déclenchement: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer les documents associés si fournis
        uploaded_files = request.FILES.getlist('documents')
        document_metadata_list = pm_data.get('documents', [])
        
        # Dans la partie création des documents :
        try:
            for index, uploaded_file in enumerate(uploaded_files):
                # Récupérer les métadonnées correspondantes si elles existent
                metadata = None
                if index < len(document_metadata_list):
                    metadata = document_metadata_list[index]
                
                # Nom du document : depuis les métadonnées ou le nom du fichier
                nom_document = ""
                if metadata and metadata.get('nomDocument'):
                    nom_document = metadata.get('nomDocument')
                else:
                    # Utiliser le nom du fichier sans extension comme nom par défaut
                    nom_document = os.path.splitext(uploaded_file.name)[0]
                
                # Type de document : depuis les métadonnées ou valeur par défaut
                type_document_id = 1  # Valeur par défaut
                if metadata and metadata.get('typeDocument_id'):
                    type_document_id = metadata.get('typeDocument_id')
                
                # Créer le Document avec le nom de fichier original
                document = Document.objects.create(
                    nomDocument=nom_document,
                    typeDocument_id=type_document_id,
                    cheminAcces=uploaded_file  # Django utilise le nom original du fichier
                )
                
                # Puis créer l'association avec le plan de maintenance
                PlanMaintenanceDocument.objects.create(
                    plan_maintenance=plan,
                    document=document
                )
        
        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la création des documents: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Sérialiser et retourner la réponse
        serializer = self.get_serializer(plan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """Mise à jour d'un plan de maintenance existant"""
        data = dict(request.data)
        
        print("Données reçues pour update:", data)
        
        # Extraire les valeurs uniques des listes
        for key, value in data.items():  
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]
        
        # Parser le JSON des changements
        try:
            changes_json = data.get('changes')
            if changes_json:
                changes = json.loads(changes_json)
                print("Changements détectés:", changes)
            else:
                changes = {}
                print("Aucun changement détecté")
        except json.JSONDecodeError as e:
            print(f"Erreur parsing changes JSON: {e}")
            changes = {}
        
        # Parser le JSON du seuil si présent
        try:
            seuil_json = data.get('seuil')
            if seuil_json:
                seuil_data = json.loads(seuil_json)
                print("Données seuil:", seuil_data)
            else:
                seuil_data = {}
        except json.JSONDecodeError as e:
            print(f"Erreur parsing seuil JSON: {e}")
            seuil_data = {}
        
        plan = self.get_object()
        modifications_log = {}  # Pour regrouper toutes les modifications
        
        # 1. Mettre à jour les champs simples du plan de maintenance
        simple_fields = ['nom', 'commentaire', 'necessiteHabilitationElectrique', 
                        'necessitePermisFeu', 'type_plan_maintenance_id']
        
        for field in simple_fields:
            if field in data:
                old_value = getattr(plan, field, None)
                new_value = data[field]
                if old_value != new_value:
                    setattr(plan, field, new_value)
                    modifications_log[field] = {
                        'old': old_value,
                        'new': new_value
                    }
        
        # 2. Gérer les modifications détectées depuis le frontend
        if changes:
            for field_path, change_data in changes.items():
                # Pour les champs simples du seuil
                if field_path in ['derniereIntervention', 'prochaineMaintenance', 
                                'ecartInterventions', 'estGlissant', 'planMaintenanceId']:
                    # Ces champs concernent le déclenchement, pas le plan
                    print(f"Changement dans le déclenchement: {field_path}")
                    continue
                
                # Pour les champs du plan de maintenance
                elif field_path.startswith('planMaintenance.'):
                    field_name = field_path.replace('planMaintenance.', '')
                    if field_name == 'type_id':
                        field_name = 'type_plan_maintenance_id'
                    
                    # Vérifier si le champ existe dans le modèle
                    if hasattr(plan, field_name):
                        old_value = getattr(plan, field_name, None)
                        new_value = change_data.get('nouvelle')
                        
                        # Pour les champs booléens, s'assurer du type
                        if field_name in ['necessiteHabilitationElectrique', 'necessitePermisFeu']:
                            new_value = bool(new_value)
                        
                        if old_value != new_value:
                            setattr(plan, field_name, new_value)
                            modifications_log[field_name] = {
                                'old': old_value,
                                'new': new_value
                            }
        
        # Sauvegarder les modifications du plan
        if modifications_log:
            plan.save()
            
            # Créer un seul log pour toutes les modifications du plan
            Log.objects.create(
                utilisateur=request.user,
                type_action='MODIFICATION',
                idCible=plan.id,
                champs_modifies=modifications_log,
                date_action=timezone.now(),
                modele_cible='PlanMaintenance'
            )
        
        # 3. Mettre à jour les consommables si nécessaire
        if changes and 'planMaintenance.consommables' in changes:
            consommable_change = changes['planMaintenance.consommables']
            print("Changement des consommables détecté")
            
            # Récupérer les anciens consommables
            old_consommables = consommable_change.get('ancienne', [])
            new_consommables = consommable_change.get('nouvelle', [])
            
            # Supprimer les anciennes associations
            plan.consommables.all().delete()
            
            # Créer les nouvelles associations
            for cons in new_consommables:
                PlanMaintenanceConsommable.objects.create(
                    plan_maintenance=plan,
                    consommable_id=cons.get('consommable_id'),
                    quantite_necessaire=cons.get('quantite', 1)
                )
            
            # Log pour les consommables
            Log.objects.create(
                utilisateur=request.user,
                type_action='MODIFICATION',
                idCible=plan.id,
                champs_modifies={'consommables': {
                    'old': old_consommables,
                    'new': new_consommables
                }},
                date_action=timezone.now(),
                modele_cible='PlanMaintenance'
            )
        
        # 4. Mettre à jour le déclenchement associé
        try:
            if seuil_data:
                from equipement.models import Declencher
                
                # Chercher le déclenchement associé à ce plan
                declencher = Declencher.objects.filter(planMaintenance=plan).first()
                
                if declencher:
                    declencher_modifications = {}
                    
                    # Mettre à jour les champs du déclenchement
                    fields_to_update = ['derniereIntervention', 'prochaineMaintenance', 
                                    'ecartInterventions', 'estGlissant']
                    
                    for field in fields_to_update:
                        if field in seuil_data:
                            old_value = getattr(declencher, field, None)
                            new_value = seuil_data[field]
                            if old_value != new_value:
                                setattr(declencher, field, new_value)
                                declencher_modifications[field] = {
                                    'old': old_value,
                                    'new': new_value
                                }
                    
                    # Sauvegarder les modifications du déclenchement
                    if declencher_modifications:
                        declencher.save()
                        
                        # Log pour le déclenchement
                        Log.objects.create(
                            utilisateur=request.user,
                            type_action='MODIFICATION',
                            idCible=declencher.id,
                            champs_modifies=declencher_modifications,
                            date_action=timezone.now(),
                            modele_cible='Declencher'
                        )
                    
                    # Mettre à jour le compteur si changement
                    compteur_id = seuil_data.get('compteurId')
                    if compteur_id and declencher.compteur_id != compteur_id:
                        old_compteur = declencher.compteur_id
                        declencher.compteur_id = compteur_id
                        declencher.save()
                        
                        Log.objects.create(
                            utilisateur=request.user,
                            type_action='MODIFICATION',
                            idCible=declencher.id,
                            champs_modifies={'compteur_id': {
                                'old': old_compteur,
                                'new': compteur_id
                            }},
                            date_action=timezone.now(),
                            modele_cible='Declencher'
                        )
        
        except Exception as e:
            print(f"Erreur lors de la mise à jour du déclenchement: {e}")
        
        # 5. Mettre à jour les documents si fichiers uploadés
        try:
            uploaded_files = request.FILES.getlist('documents')
            if uploaded_files:
                print(f"{len(uploaded_files)} fichiers uploadés")
                
                # Récupérer les métadonnées des documents
                documents_metadata = []
                if seuil_data.get('planMaintenance', {}).get('documents'):
                    documents_metadata = seuil_data['planMaintenance']['documents']
                
                for index, uploaded_file in enumerate(uploaded_files):
                    metadata = None
                    if index < len(documents_metadata):
                        metadata = documents_metadata[index]
                    
                    nom_document = metadata.get('nomDocument', '') if metadata else ''
                    type_document_id = metadata.get('typeDocument_id', 1) if metadata else 1
                    
                    if not nom_document:
                        nom_document = os.path.splitext(uploaded_file.name)[0]
                    
                    # Créer le document
                    document = Document.objects.create(
                        nomDocument=nom_document,
                        typeDocument_id=type_document_id,
                        cheminAcces=uploaded_file
                    )
                    
                    # Créer l'association
                    PlanMaintenanceDocument.objects.create(
                        plan_maintenance=plan,
                        document=document
                    )
                
                # Log pour l'ajout de documents
                if uploaded_files:
                    Log.objects.create(
                        utilisateur=request.user,
                        type_action='AJOUT_DOCUMENTS',
                        idCible=plan.id,
                        champs_modifies={
                            'documents_ajoutes': len(uploaded_files)
                        },
                        date_action=timezone.now(),
                        modele_cible='PlanMaintenance'
                    )
        
        except Exception as e:
            print(f"Erreur lors de la création des documents: {e}")
        
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