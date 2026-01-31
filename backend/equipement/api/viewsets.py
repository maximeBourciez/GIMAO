import json
import datetime
from decimal import Decimal
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404

# Models
from maintenance.models import DemandeIntervention, BonTravail
from donnees.models import Document
from stock.models import Consommable
from equipement.models import *
from utilisateur.models import Utilisateur, Log

# Serializers
from equipement.api.serializers import (
    EquipementSerializer,
    StatutEquipementSerializer,
    ConstituerSerializer,
    ModeleEquipementSerializer,
    CompteurSerializer,
    FamilleEquipementSerializer,
    EquipementAffichageSerializer,
    EquipementCreateSerializer,
    DeclenchementSerializer
)

from maintenance.models import PlanMaintenance, PlanMaintenanceConsommable, PlanMaintenanceDocument
from donnees.models import Lieu, Document, Fabricant, Fournisseur


import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone

# Models et Serializers...

class EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return EquipementCreateSerializer
        return EquipementSerializer

    def _get_utilisateur(self, request):
        """Récupère l'utilisateur à partir de la requête"""
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                return Utilisateur.objects.get(user=request.user)
            except Utilisateur.DoesNotExist:
                return None
        return None

    def _create_log_entry(self, type_action, nom_table, id_cible, champs_modifies, utilisateur):
        """Crée une entrée de log"""
        
        def make_serializable(obj):
            if isinstance(obj, Decimal):
                return str(obj)
            if isinstance(obj, (datetime.datetime, datetime.date)):
                return obj.isoformat()
            if isinstance(obj, dict):
                return {k: make_serializable(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [make_serializable(v) for v in obj]
            return obj

        Log.objects.create(
            type=type_action,
            nomTable=nom_table,
            idCible=make_serializable(id_cible),
            champsModifies=make_serializable(champs_modifies),
            utilisateur=utilisateur
        )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Création d'un nouvel équipement"""
        data = dict(request.data)
        
        # Extraire les valeurs uniques des listes
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        # Normalisation
        if "lieu" in data:
            lieu_value = data["lieu"]
            if isinstance(lieu_value, str):
                try:
                    lieu_obj = json.loads(lieu_value)
                    data["lieu"] = lieu_obj["id"]
                except (TypeError, ValueError, KeyError):
                    pass
            elif isinstance(lieu_value, dict):
                data["lieu"] = lieu_value["id"]

        for field in ["consommables", "compteurs", "plansMaintenance"]:
            if field in data and isinstance(data[field], str):
                data[field] = json.loads(data[field])

        # Validation serializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Récupération de l'utilisateur créateur
        # Priorité: utilisateur authentifié > createurEquipement fourni dans data
        utilisateur = self._get_utilisateur(request)
        if not utilisateur and "createurEquipement" in data and data["createurEquipement"]:
            try:
                utilisateur = Utilisateur.objects.get(id=data["createurEquipement"])
            except Utilisateur.DoesNotExist:
                utilisateur = None
        
        if not utilisateur:
            return Response(
                {"error": "Utilisateur non authentifié ou introuvable"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Récupération des dépendances
        modele = ModeleEquipement.objects.get(id=data["modeleEquipement"])
        fabricant = Fabricant.objects.get(id=data["fabricant"])
        fournisseur = Fournisseur.objects.get(id=data["fournisseur"])
        famille = FamilleEquipement.objects.get(id=data["famille"])
        lieu = Lieu.objects.get(id=data["lieu"])

        # Création de l'équipement
        equipement = Equipement.objects.create(
            reference=data["reference"],
            designation=data["designation"],
            dateMiseEnService=data.get("dateMiseEnService"),
            prixAchat=data.get("prixAchat", 0),
            createurEquipement=utilisateur,
            lieu=lieu,
            modele=modele,
            famille=famille,
            fournisseur=fournisseur,
            fabricant=fabricant,
            numSerie=data.get("numSerie", ""),
            lienImage=data.get("lienImageEquipement")
        )

        # Statut
        statut = data.get("statut") 
        if statut:
            StatutEquipement.objects.create(
                equipement=equipement,
                statut=statut,
                dateChangement=timezone.now()
            )

        # Consommables
        for consommable_id in data.get("consommables", []):
            Constituer.objects.create(
                equipement=equipement,
                consommable_id=consommable_id
            )

        # Créer les compteurs (sans les plans de maintenance)
        compteurs_crees = []
        for cp in data.get("compteurs", []):
            compteur = Compteur.objects.create(
                equipement=equipement,
                nomCompteur=cp["nom"],
                valeurCourante=cp.get("valeurCourante", 0),
                unite=cp.get("unite", "heures"),
                estPrincipal=cp.get("estPrincipal", False),
                type=cp.get("type", "Général")
            )
            compteurs_crees.append(compteur)

        # Créer les plans de maintenance (qui référencent les compteurs par index)
        for pm_data in data.get("plansMaintenance", []):
            compteur_index = pm_data.get("compteurIndex")
            if compteur_index is None or compteur_index >= len(compteurs_crees):
                continue
            
            compteur = compteurs_crees[compteur_index]
            
            # Créer le plan de maintenance
            plan = PlanMaintenance.objects.create(
                equipement=equipement,
                nom=pm_data.get("nom", f"Plan {compteur.nomCompteur}"),
                type_plan_maintenance_id=pm_data.get("type_id"),
                commentaire=pm_data.get("description", ""),
                necessiteHabilitationElectrique=pm_data.get("necessiteHabilitationElectrique", False),
                necessitePermisFeu=pm_data.get("necessitePermisFeu", False)
            )

            # Créer le lien Declencher entre le compteur et le plan
            seuil = pm_data.get("seuil", {})
            Declencher.objects.create(
                compteur=compteur,
                planMaintenance=plan,
                derniereIntervention=seuil.get("derniereIntervention", 0),
                ecartInterventions=seuil.get("ecartInterventions", 0),
                prochaineMaintenance=seuil.get("prochaineMaintenance", 0),
                estGlissant=seuil.get("estGlissant", False)
            )

            # Consommables du plan
            for consommable_data in pm_data.get("consommables", []):
                # Support pour nouveau format {consommable_id, quantite_necessaire}
                if isinstance(consommable_data, dict):
                    consommable_id = consommable_data.get('consommable_id')
                    quantite = consommable_data.get('quantite_necessaire', 1)
                else:
                    # Format ancien (simple ID)
                    consommable_id = consommable_data
                    quantite = 1
                
                if consommable_id:
                    PlanMaintenanceConsommable.objects.create(
                        plan_maintenance=plan,
                        consommable_id=consommable_id,
                        quantite_necessaire=quantite
                    )

        # Log de création
        utilisateur = self._get_utilisateur(request)
        self._create_log_entry(
            type_action='création',
            nom_table='equipement',
            id_cible={'equipement_id': equipement.id},
            champs_modifies={'equipement_created': True},
            utilisateur=utilisateur
        )

        return Response(
            EquipementSerializer(equipement).data,
            status=status.HTTP_201_CREATED
        )

    
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Mise à jour d'un équipement - seulement les changements sont envoyés
        """
        equipement = self.get_object()
        utilisateur = self._get_utilisateur(request)
        
        # -------------------------
        # Récupération des données
        # -------------------------
        data = dict(request.data)
        
        # Extraire les valeurs uniques des listes
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        # Récupérer les changements
        changes_data = data.get("changes")
        if not changes_data:
            return Response(
                {"error": "Aucune donnée de changement fournie"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            changes = json.loads(changes_data)
        except json.JSONDecodeError:
            return Response(
                {"error": "Format JSON invalide pour les changements"},
                status=status.HTTP_400_BAD_REQUEST
            )

        print('Données de la requête:')
        print(f"  Changements: {changes}")
        print(f"  Fichiers: {list(request.FILES.keys())}")

        # -------------------------
        # Traitement des modifications
        # -------------------------
        modifications_appliquees = {}

        # 1. Mise à jour des champs simples de l'équipement
        simple_fields = ['numSerie', 'reference', 'designation', 'dateMiseEnService', 
                        'prixAchat', 'modeleEquipement', 'fournisseur', 'fabricant', 
                        'famille', 'lieu', 'statut']
        
        for field in simple_fields:
            if field in changes:
                modification = changes[field]
                ancien = modification.get('ancienne')
                nouveau = modification.get('nouvelle')
                
                if field == 'lieu' and isinstance(nouveau, dict):
                    print(nouveau)
                    nouveau = nouveau.get('id')
                
                # Appliquer la modification
                if field == 'lieu' and nouveau:
                    try:
                        lieu = Lieu.objects.get(id=nouveau)
                        equipement.lieu = lieu
                        self._create_log_entry(
                            type_action='modification',
                            nom_table='equipement',
                            id_cible={'equipement_id': equipement.id},
                            champs_modifies={field: {'ancien': ancien, 'nouveau': nouveau}},
                            utilisateur=utilisateur
                        )
                        modifications_appliquees[field] = {'ancien': ancien, 'nouveau': nouveau}
                    except Lieu.DoesNotExist:
                        pass
                
                elif field == 'statut' and nouveau:
                    dernier_statut = equipement.statuts.order_by('-dateChangement').first()
                    ancien_statut = dernier_statut.statut if dernier_statut else None
                    
                    if ancien_statut != nouveau:
                        StatutEquipement.objects.create(
                            equipement=equipement,
                            statut=nouveau,
                            dateChangement=timezone.now()
                        )
                        self._create_log_entry(
                            type_action='modification',
                            nom_table='statut_equipement',
                            id_cible={'equipement_id': equipement.id},
                            champs_modifies={field: {'ancien': ancien, 'nouveau': nouveau}},
                            utilisateur=utilisateur
                        )
                
                elif field == 'modeleEquipement' and nouveau:
                    try:
                        modele = ModeleEquipement.objects.get(id=nouveau)
                        equipement.modele = modele
                        modifications_appliquees[field] = {'ancien': ancien, 'nouveau': nouveau}
                    except ModeleEquipement.DoesNotExist:
                        pass
                
                elif field == 'fabricant' and nouveau:
                    try:
                        fabricant = Fabricant.objects.get(id=nouveau)
                        equipement.fabricant = fabricant
                        modifications_appliquees[field] = {'ancien': ancien, 'nouveau': nouveau}
                    except Fabricant.DoesNotExist:
                        pass
                
                elif field == 'fournisseur' and nouveau:
                    try:
                        fournisseur = Fournisseur.objects.get(id=nouveau)
                        equipement.fournisseur = fournisseur
                        modifications_appliquees[field] = {'ancien': ancien, 'nouveau': nouveau}
                    except Fournisseur.DoesNotExist:
                        pass
                
                elif field == 'famille' and nouveau:
                    try:
                        famille = FamilleEquipement.objects.get(id=nouveau)
                        equipement.famille = famille
                        modifications_appliquees[field] = {'ancien': ancien, 'nouveau': nouveau}
                    except FamilleEquipement.DoesNotExist:
                        pass
                
                elif field in ['numSerie', 'reference', 'designation', 'dateMiseEnService', 'prixAchat']:
                    ancien_val = getattr(equipement, field, None)
                    if str(ancien_val) != str(nouveau):
                        setattr(equipement, field, nouveau)
                        modifications_appliquees[field] = {'ancien': ancien_val, 'nouveau': nouveau}

        # 2. Consommables
        if 'consommables' in changes:
            modification = changes['consommables']
            old_consommables = set(equipement.constituer_set.values_list('consommable_id', flat=True))
            new_consommables = set(modification.get('nouvelle', []))
            
            # Détecter les ajouts et suppressions
            ajoutes = modification.get('ajoutes', [])
            retires = modification.get('retires', [])
            
            if ajoutes or retires:
                # Supprimer
                if retires:
                    equipement.constituer_set.filter(consommable_id__in=retires).delete()

                    self._create_log_entry(
                        type_action='suppression',
                        nom_table='constituer',
                        id_cible={'equipement_id': equipement.id},
                        champs_modifies={'consommables_retires': retires},
                        utilisateur=utilisateur
                    )
                
                # Ajouter
                for consommable_id in ajoutes:
                    Constituer.objects.create(
                        equipement=equipement,
                        consommable_id=consommable_id
                    )
                
                if(len(ajoutes) > 0):
                    self._create_log_entry(
                        type_action='ajout',
                        nom_table='constituer',
                        id_cible={'equipement_id': equipement.id},
                        champs_modifies={'consommables_ajoutes': ajoutes},
                        utilisateur=utilisateur
                    )

        # 3. Gestion des fichiers d'image de l'équipement
        if 'lienImageEquipement' in request.FILES:
            uploaded_file = request.FILES['lienImageEquipement']
            # Supprimer l'ancienne image si elle existe
            print(f"Ancienne image: {equipement.lienImage}")
            print(f"Nouvelle image: {uploaded_file}")
            if equipement.lienImage:
                try:
                    equipement.lienImage.delete(save=False)
                except:
                    pass
            
            # Sauvegarder la nouvelle image
            equipement.lienImage = uploaded_file
            modifications_appliquees['lienImageEquipement'] = 'updated'
            self._create_log_entry(
                type_action='modification',
                nom_table='equipement',
                id_cible={'equipement_id': equipement.id},
                champs_modifies={'lienImageEquipement': 'updated'},
                utilisateur=utilisateur
            )

        # Sauvegarder l'équipement si des modifications ont été faites
        if modifications_appliquees:
            equipement.save()
            print(f"Équipement {equipement.id} sauvegardé avec modifications: {modifications_appliquees}")

        # -------------------------
        # Log des modifications
        # -------------------------
        if modifications_appliquees:
            self._create_log_entry(
                type_action='modification',
                nom_table='equipement',
                id_cible={'equipement_id': equipement.id},
                champs_modifies=modifications_appliquees,
                utilisateur=utilisateur
            )

        return Response(
            EquipementSerializer(equipement).data,
            status=status.HTTP_200_OK
        )

    def _update_compteur_from_changes(self, compteur, modifications, request):
        """Met à jour un compteur existant"""
        print(f"Mise à jour du compteur {compteur.id} avec modifications: {modifications}")
        
        # Mapping des champs du frontend vers le modèle Compteur
        field_mapping = {
            'nom': 'nomCompteur',
            'valeurCourante': 'valeurCourante',
            'unite': 'unite',
            'estPrincipal': 'estPrincipal',
            'type': 'type'
        }
        
        # Mise à jour des champs simples du compteur
        for field, model_field in field_mapping.items():
            if field in modifications:
                field_data = modifications[field]
                nouvelle_valeur = field_data.get('nouvelle')
                if nouvelle_valeur is not None:
                    old_value = getattr(compteur, model_field)
                    if str(old_value) != str(nouvelle_valeur):
                        setattr(compteur, model_field, nouvelle_valeur)
                        print(f"  {field}: {old_value} -> {nouvelle_valeur}")
        
        compteur.save()
        
        # Gérer les modifications du seuil (Declencher)
        seuil_fields = ['derniereIntervention', 'intervalle', 'estGlissant']
        if any(f in modifications for f in seuil_fields):
            print(f"  Modification du seuil détectée")
            self._update_declencher_from_changes(compteur, modifications, request)
        
        # Gérer le plan de maintenance si présent dans les modifications
        plan_keys = [k for k in modifications.keys() if k.startswith('planMaintenance') or k in ['habElec', 'permisFeu', 'description']]
        if plan_keys:
            print(f"  Modification du plan de maintenance: {plan_keys}")
            self._update_plan_maintenance_from_changes(compteur, modifications, request)

    def _update_declencher_from_changes(self, compteur, modifications, request):
        """Met à jour le seuil Declencher d'un compteur"""
        print(f"Mise à jour du seuil pour le compteur {compteur.id}")
        
        # Récupérer le premier Declencher (normalement il n'y en a qu'un par compteur)
        declencher = compteur.declenchements.first()
        
        if not declencher:
            print("  Aucun seuil trouvé, création d'un nouveau")
            # Si pas de Declencher, en créer un
            declencher = Declencher.objects.create(
                compteur=compteur,
                derniereIntervention=0,
                ecartInterventions=0,
                prochaineMaintenance=0,
                estGlissant=False
            )
        
        # Mise à jour des champs du Declencher
        if 'derniereIntervention' in modifications:
            nouvelle_valeur = modifications['derniereIntervention'].get('nouvelle')
            if nouvelle_valeur is not None:
                declencher.derniereIntervention = int(nouvelle_valeur)
                print(f"  derniereIntervention: -> {nouvelle_valeur}")
        
        if 'intervalle' in modifications:
            nouvelle_valeur = modifications['intervalle'].get('nouvelle')
            if nouvelle_valeur is not None:
                declencher.ecartInterventions = float(nouvelle_valeur)
                print(f"  ecartInterventions: -> {nouvelle_valeur}")
        
        if 'estGlissant' in modifications:
            nouvelle_valeur = modifications['estGlissant'].get('nouvelle')
            if nouvelle_valeur is not None:
                declencher.estGlissant = bool(nouvelle_valeur)
                print(f"  estGlissant: -> {nouvelle_valeur}")
        
        # Recalculer la prochaine maintenance
        declencher.prochaineMaintenance = declencher.derniereIntervention + declencher.ecartInterventions
        print(f"  prochaineMaintenance calculée: {declencher.prochaineMaintenance}")
        
        declencher.save()

    def _update_plan_maintenance_from_changes(self, compteur, modifications, request):
        """Met à jour le plan de maintenance d'un compteur"""
        print(f"Traitement du plan de maintenance pour compteur {compteur.id}")
        
        # Récupérer le Declencher pour trouver le PlanMaintenance associé
        declencher = compteur.declenchements.first()
        
        if not declencher or not declencher.planMaintenance:
            print("  Aucun plan de maintenance trouvé, création d'un nouveau")
            # Créer un nouveau plan de maintenance
            plan = PlanMaintenance.objects.create(
                equipement=compteur.equipement,
                nom="Nouveau plan",
                type_plan_maintenance_id=1  # Type par défaut, à ajuster selon vos besoins
            )
            
            # Créer ou mettre à jour le Declencher pour lier le compteur au plan
            if not declencher:
                Declencher.objects.create(
                    compteur=compteur,
                    planMaintenance=plan,
                    derniereIntervention=0,
                    ecartInterventions=0,
                    prochaineMaintenance=0,
                    estGlissant=False
                )
            else:
                declencher.planMaintenance = plan
                declencher.save()
        else:
            plan = declencher.planMaintenance
        
        # Mise à jour du nom
        if 'planMaintenance.nom' in modifications:
            new_name = modifications['planMaintenance.nom'].get('nouvelle')
            if new_name and plan.nom != new_name:
                print(f"  Nom du plan: {plan.nom} -> {new_name}")
                plan.nom = new_name
        
        # Mise à jour du type
        if 'planMaintenance.type' in modifications:
            new_type = modifications['planMaintenance.type'].get('nouvelle')
            if new_type and plan.type_plan_maintenance_id != new_type:
                print(f"  Type du plan: {plan.type_plan_maintenance_id} -> {new_type}")
                plan.type_plan_maintenance_id = new_type
        
        # Mise à jour du commentaire (description)
        if 'description' in modifications:
            new_desc = modifications['description'].get('nouvelle')
            if new_desc is not None:
                print(f"  Commentaire: {plan.commentaire} -> {new_desc}")
                plan.commentaire = new_desc
        
        # Mise à jour de l'habilitation électrique
        if 'habElec' in modifications:
            new_val = modifications['habElec'].get('nouvelle')
            if new_val is not None:
                print(f"  Habilitation électrique: {plan.necessiteHabilitationElectrique} -> {new_val}")
                plan.necessiteHabilitationElectrique = bool(new_val)
        
        # Mise à jour du permis feu
        if 'permisFeu' in modifications:
            new_val = modifications['permisFeu'].get('nouvelle')
            if new_val is not None:
                print(f"  Permis feu: {plan.necessitePermisFeu} -> {new_val}")
                plan.necessitePermisFeu = bool(new_val)
        
        # Mise à jour des consommables
        if 'planMaintenance.consommables' in modifications:
            consommables_data = modifications['planMaintenance.consommables']
            nouveaux_consommables = consommables_data.get('nouvelle', [])
            ajoutes = consommables_data.get('ajoutes', [])
            retires = consommables_data.get('retires', [])
            
            print(f"  Consommables: {len(nouveaux_consommables)} total, {len(ajoutes)} ajoutés, {len(retires)} retirés")
            
            # Supprimer les consommables retirés
            if retires:
                plan.planmaintenanceconsommable_set.filter(consommable_id__in=retires).delete()
            
            # Ajouter les nouveaux consommables
            for consommable_id in ajoutes:
                # Chercher la quantité dans les données complètes
                quantite = 1  # Valeur par défaut
                for conso in nouveaux_consommables:
                    # Support pour nouveau format {consommable_id, quantite_necessaire}
                    if isinstance(conso, dict):
                        conso_id = conso.get('consommable_id') or conso.get('consommable')
                        if conso_id == consommable_id:
                            quantite = conso.get('quantite_necessaire') or conso.get('quantite', 1)
                            break
                
                PlanMaintenanceConsommable.objects.create(
                    plan_maintenance=plan,
                    consommable_id=consommable_id,
                    quantite_necessaire=quantite
                )
        
        # Mise à jour des documents
        if 'planMaintenance.documents' in modifications:
            documents_data = modifications['planMaintenance.documents']
            nouveaux_documents = documents_data.get('nouvelle', [])
            anciens_documents = documents_data.get('ancienne', [])
            
            print(f"  Documents: {len(nouveaux_documents)} nouveau(x), {len(anciens_documents)} ancien(s)")
            
            # Créer un mapping pour trouver les fichiers
            file_mapping = {}
            for key, file in request.FILES.items():
                if key.startswith('document_'):
                    # Extraire les métadonnées
                    meta_key = f"{key}_meta"
                    if meta_key in request.data:
                        try:
                            meta = json.loads(request.data[meta_key])
                            compteur_id = meta.get('compteurId')
                            doc_index = meta.get('documentIndex')
                            
                            if compteur_id == compteur.id:
                                file_mapping[doc_index] = file
                        except json.JSONDecodeError:
                            continue
            
            # Pour chaque nouveau document
            for i, doc_data in enumerate(nouveaux_documents):
                if not isinstance(doc_data, dict):
                    continue
                
                # Vérifier si c'est un document existant qui a un fichier à mettre à jour
                file_to_use = file_mapping.get(i)
                
                if file_to_use:
                    # Créer un nouveau document avec le fichier
                    document = Document.objects.create(
                        nomDocument=doc_data.get('titre', file_to_use.name),
                        cheminAcces=file_to_use,
                        typeDocument_id=doc_data.get('type', 1)
                    )
                    
                    # Lier au plan de maintenance
                    PlanMaintenanceDocument.objects.create(
                        plan_maintenance=plan,
                        document=document
                    )
                    print(f"  Document ajouté: {document.nomDocument}")
                
                elif 'titre' in doc_data and 'type' in doc_data:
                    # Document sans fichier (métadonnées seulement)
                    # C'est peut-être un document qui existait déjà
                    print(f"Document métadonnées seulement: {doc_data.get('titre')}")
        
        plan.save()



class StatutEquipementViewSet(viewsets.ModelViewSet):
    queryset = StatutEquipement.objects.all()
    serializer_class = StatutEquipementSerializer


class ConstituerViewSet(viewsets.ModelViewSet):
    queryset = Constituer.objects.all()
    serializer_class = ConstituerSerializer


class ModeleEquipementViewSet(viewsets.ModelViewSet):
    queryset = ModeleEquipement.objects.all()
    serializer_class = ModeleEquipementSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Création d'un nouveau modèle d'équipement"""
        data = request.data
        print(f"Data reçue pour création modèle : {data}")
        
        # Extraire le nom et le fabricant_id
        nom = data.get('nom')
        fabricant_id = data.get('fabricant')
        
        if not nom:
            return Response(
                {"error": "Le nom du modèle est requis"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not fabricant_id:
            return Response(
                {"error": "Le fabricant est requis"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer le modèle
        try:
            modele = ModeleEquipement.objects.create(
                nom=nom,
                fabricant_id=fabricant_id
            )
            
            # Retourner le modèle créé avec le serializer
            serializer = self.get_serializer(modele)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            print(f"Erreur lors de la création du modèle : {str(e)}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """Mise à jour d'un modèle d'équipement - gère aussi les consommables associés"""
        modele = self.get_object()
        data = request.data
        print(f"Data reçue : {data}")
        
        changes = data
        print(f"Changes : {changes}")
        
        # Récupérer l'utilisateur
        user_id = changes.get('user')
        if not user_id:
            return Response(
                {"error": "User ID is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            utilisateur = Utilisateur.objects.get(id=user_id)
            print(f"Utilisateur trouvé : {utilisateur.id}")
        except Utilisateur.DoesNotExist:
            return Response(
                {"error": "User not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Mise à jour des champs du modèle
        if 'nom' in changes:
            field_data = changes['nom']
            nouvelle_valeur = field_data.get('nouvelle')
            ancienne_valeur = field_data.get('ancienne')
                        
            if nouvelle_valeur is not None:
                old_value = modele.nom
                
                if str(old_value) != str(nouvelle_valeur):
                    modele.nom = nouvelle_valeur
                    Log.objects.create(
                        type='modification',
                        nomTable='modele_equipement',
                        idCible={'modele_equipement_id': modele.id},
                        champsModifies={'nom': {'ancien': ancienne_valeur, 'nouveau': nouvelle_valeur}},
                        utilisateur=utilisateur
                    )

        
        if 'fabricant' in changes:
            field_data = changes['fabricant']
            nouvelle_valeur = field_data.get('nouvelle')
            ancienne_valeur = field_data.get('ancienne')
                        
            if nouvelle_valeur is not None:
                old_value = modele.fabricant_id
                
                if old_value != nouvelle_valeur:
                    modele.fabricant_id = nouvelle_valeur
                    Log.objects.create(
                        type='modification',
                        nomTable='modele_equipement',
                        idCible={'modele_equipement_id': modele.id},
                        champsModifies={'fabricant': {'ancien': ancienne_valeur, 'nouveau': nouvelle_valeur}},
                        utilisateur=utilisateur
                    )
        
        # Vérifier s'il y a eu des changements (excluant 'user')
        has_changes = any(key in changes for key in ['nom', 'fabricant'])
        
        if has_changes:
            modele.save()

        return Response(
            ModeleEquipementSerializer(modele).data,
            status=status.HTTP_200_OK
        )


class CompteurViewSet(viewsets.ModelViewSet):
    queryset = Compteur.objects.all()
    serializer_class = CompteurSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Création d'un nouveau compteur avec plan de maintenance optionnel"""
        try:
            # Parser les données JSON du compteur
            compteur_data = json.loads(request.data.get('compteur', '{}'))
            
            # Vérifier que l'équipement est fourni
            equipement_id = compteur_data.get('equipement')
            if not equipement_id:
                return Response(
                    {"error": "L'ID de l'équipement est requis"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Récupérer l'équipement
            try:
                equipement = Equipement.objects.get(id=equipement_id)
            except Equipement.DoesNotExist:
                return Response(
                    {"error": "Équipement introuvable"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Créer le compteur
            compteur = Compteur.objects.create(
                equipement=equipement,
                nomCompteur=compteur_data.get('nom', ''),
                valeurCourante=compteur_data.get('valeurCourante', 0),
                unite=compteur_data.get('unite', 'heures'),
                estPrincipal=compteur_data.get('estPrincipal', False),
                type=compteur_data.get('type', 'Général')
            )
            
            # Si un plan de maintenance est fourni, le créer
            plan_data = compteur_data.get('planMaintenance')
            if plan_data:
                # Créer le plan de maintenance
                plan = PlanMaintenance.objects.create(
                    equipement=equipement,
                    nom=plan_data.get('nom', f"Plan {compteur.nomCompteur}"),
                    type_plan_maintenance_id=plan_data.get('type_id'),
                    commentaire=plan_data.get('description', ''),
                    necessiteHabilitationElectrique=plan_data.get('necessiteHabilitationElectrique', False),
                    necessitePermisFeu=plan_data.get('necessitePermisFeu', False)
                )
                
                # Créer le lien Declencher entre le compteur et le plan
                Declencher.objects.create(
                    compteur=compteur,
                    planMaintenance=plan,
                    derniereIntervention=compteur_data.get('derniereIntervention', 0),
                    ecartInterventions=compteur_data.get('intervalle', 0),
                    prochaineMaintenance=compteur_data.get('prochaineMaintenance', 0),
                    estGlissant=plan_data.get('estGlissant', False)
                )
                
                # Ajouter les consommables au plan
                for consommable_id in plan_data.get('consommables', []):
                    PlanMaintenanceConsommable.objects.create(
                        plan_maintenance=plan,
                        consommable_id=consommable_id,
                        quantite_necessaire=1
                    )
                
                # Gérer les documents
                documents = plan_data.get('documents', [])
                for doc_index, doc_data in enumerate(documents):
                    # Récupérer le fichier uploadé depuis FormData
                    file_key = f'document_{doc_index}'
                    uploaded_file = request.FILES.get(file_key)
                    
                    if uploaded_file:
                        # Créer le document
                        document = Document.objects.create(
                            nomDocument=doc_data.get('titre', uploaded_file.name),
                            lienDocument=uploaded_file,
                            typeDocument_id=doc_data.get('type')
                        )
                        
                        # Lier le document au plan
                        PlanMaintenanceDocument.objects.create(
                            plan_maintenance=plan,
                            document=document
                        )
            
            # Retourner le compteur créé
            serializer = CompteurSerializer(compteur)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except json.JSONDecodeError:
            return Response(
                {"error": "Format JSON invalide"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """ Mise à jour d'un compteur """      
        changes = request.data
        compteur = self.get_object()
        print(f"Data reçue pour mise à jour du compteur {compteur.id} : {changes}")    

        # Récupérer l'utilisateur
        user_id = changes.get('user')
        utilisateur = None
        if not user_id:
            return Response(
                {"error": "User ID is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

            try:
                utilisateur = Utilisateur.objects.get(id=user_id)
                print(f"Utilisateur trouvé : {utilisateur.id}")
            except Utilisateur.DoesNotExist:
                return Response(
                    {"error": "User not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )    

        if len(changes.keys()) == 0:
            return Response(
                {"message": "Aucune modification détectée."},
                status=status.HTTP_200_OK
            )

        # Mettre à jour les champs du compteur
        field_mapping = {
            'nom': 'nomCompteur',
            'valeurCourante': 'valeurCourante',
            'unite': 'unite',
            'estPrincipal': 'estPrincipal',
            'type': 'type'
        }

        for field, model_field in field_mapping.items():
            if field in changes:
                field_data = changes[field]
                nouvelle_valeur = field_data.get('nouvelle')
                ancienne_valeur = field_data.get('ancienne')
                
                if nouvelle_valeur is not None:
                    old_value = getattr(compteur, model_field)
                    
                    if str(old_value) != str(nouvelle_valeur):
                        setattr(compteur, model_field, nouvelle_valeur)
                        
                        # Créer une entrée de log pour chaque champ modifié
                        self._create_log_entry(
                            type_action='modification',
                            nom_table='compteur',
                            id_cible={'id': compteur.id},
                            champs_modifies={field: {'ancien': ancienne_valeur, 'nouveau': nouvelle_valeur}},
                            utilisateur=utilisateur
                        )

        compteur.save()
        return Response(
            CompteurSerializer(compteur).data,
            status=status.HTTP_200_OK
        )
    
    def _create_log_entry(self, type_action, nom_table, id_cible, champs_modifies, utilisateur):
        """Crée une entrée de log"""
        Log.objects.create(
            type=type_action,
            nomTable=nom_table,
            idCible=id_cible,
            champsModifies=champs_modifies,
            utilisateur=utilisateur
        )


class FamilleEquipementViewSet(viewsets.ModelViewSet):
    queryset = FamilleEquipement.objects.all()
    serializer_class = FamilleEquipementSerializer


class EquipementAffichageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour l'affichage détaillé des équipements"""
    serializer_class = EquipementAffichageSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Equipement.objects.select_related(
            'lieu', 'modele__fabricant', 'famille'
        ).prefetch_related(
            'statuts',
            'compteurs',
            'documents'
        )




class DeclenchementViewSet(viewsets.ModelViewSet):
    """ ViewSet pour les seuils (declenchement): création/modification """

    queryset = Declencher.objects.all()
    serializer_class = DeclenchementSerializer


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """ Creation d'un Seuil avec PM & compteur """
        # Récupération et normalisation des données
        data = dict(request.data)

        # Extraire les valeurs uniques des listes (compatibilité FormData)
        for key, value in list(data.items()):
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        # Parser les objets JSON s'ils sont envoyés en tant que chaînes
        plan_data = data.get('planMaintenance') or {}
        if isinstance(plan_data, str):
            try:
                plan_data = json.loads(plan_data)
            except json.JSONDecodeError:
                plan_data = {}

        seuil = data.get('seuil') or {}
        if isinstance(seuil, str):
            try:
                seuil = json.loads(seuil)
            except json.JSONDecodeError:
                seuil = {}

        # Récupérer le compteur existant ou créer un compteur minimal si on fournit un equipmentId
        compteur_id = data.get('compteur') or data.get('compteurId')
        equipment_id = data.get('equipmentId') or data.get('equipement') or data.get('equipmentId')

        compteur = None
        if compteur_id:
            try:
                compteur = Compteur.objects.get(id=compteur_id)
            except Compteur.DoesNotExist:
                return Response({'error': 'Compteur introuvable'}, status=status.HTTP_404_NOT_FOUND)
        else:
            if not equipment_id:
                return Response({'error': 'Il faut fournir "compteur" ou "equipmentId"'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                equipment = Equipement.objects.get(id=equipment_id)
            except Equipement.DoesNotExist:
                return Response({'error': 'Équipement introuvable'}, status=status.HTTP_404_NOT_FOUND)

            # Créer un compteur par défaut lié à l'équipement
            compteur = Compteur.objects.create(
                equipement=equipment,
                nomCompteur=plan_data.get('nom', f"Compteur pour {equipment.id}"),
                valeurCourante=0,
                unite=plan_data.get('unite', 'heures'),
                estPrincipal=False,
                type=plan_data.get('type', 'Général')
            )

        # Créer le plan de maintenance
        plan = PlanMaintenance.objects.create(
            equipement=compteur.equipement,
            nom=plan_data.get('nom') or f"Plan {compteur.nomCompteur}",
            type_plan_maintenance_id=plan_data.get('type_id') or plan_data.get('type'),
            commentaire=plan_data.get('description') or plan_data.get('commentaire', ''),
            necessiteHabilitationElectrique=bool(plan_data.get('necessiteHabilitationElectrique', False)),
            necessitePermisFeu=bool(plan_data.get('necessitePermisFeu', False))
        )

        # Créer le déclencheur (seuil)
        derniere = seuil.get('derniereIntervention') or seuil.get('derniereintervention') or 0
        ecart = seuil.get('ecartInterventions') or seuil.get('intervalle') or 0
        est_glissant = seuil.get('estGlissant', False)

        try:
            derniere = int(float(derniere))
        except Exception:
            derniere = 0

        try:
            ecart = float(ecart)
        except Exception:
            ecart = 0

        prochaine = seuil.get('prochaineMaintenance')
        if prochaine is None:
            prochaine = int(derniere + ecart)
        else:
            try:
                prochaine = int(float(prochaine))
            except Exception:
                prochaine = int(derniere + ecart)

        declencher = Declencher.objects.create(
            compteur=compteur,
            planMaintenance=plan,
            derniereIntervention=derniere,
            ecartInterventions=ecart,
            prochaineMaintenance=prochaine,
            estGlissant=bool(est_glissant)
        )

        # Consommables pour le plan
        for conso in plan_data.get('consommables', []) or []:
            if isinstance(conso, dict):
                consommable_id = conso.get('consommable_id') or conso.get('consommable')
                quantite = conso.get('quantite_necessaire') or conso.get('quantite') or 1
            else:
                consommable_id = conso
                quantite = 1

            if consommable_id:
                PlanMaintenanceConsommable.objects.create(
                    plan_maintenance=plan,
                    consommable_id=consommable_id,
                    quantite_necessaire=quantite
                )

        # Documents pour le plan
        documents = plan_data.get('documents', []) or []
        for doc_index, doc_data in enumerate(documents):
            # Récupérer le fichier uploadé depuis FormData
            file_key = f'document_{doc_index}'
            uploaded_file = request.FILES.get(file_key)

            if uploaded_file:
                # Créer le document
                document = Document.objects.create(
                    nomDocument=doc_data.get('titre', uploaded_file.name),
                    cheminAcces=uploaded_file,
                    typeDocument_id=doc_data.get('type')
                )

                # Lier le document au plan
                PlanMaintenanceDocument.objects.create(
                    plan_maintenance=plan,
                    document=document
                )




        serializer = DeclenchementSerializer(declencher)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @transaction.atomic
    def partial_update(self, request, pk=None):
        declenchement = get_object_or_404(Declencher, pk=pk)
        utilisateur = request.user if request.user.is_authenticated else None

        seuil_diff = json.loads(request.data.get('seuil_diff', '{}'))
        pm_diff = json.loads(request.data.get('planMaintenance_diff', '{}'))

        logs = []

        # ============================
        # 1. MISE À JOUR DU SEUIL
        # ============================
        if seuil_diff:
            for champ, valeurs in seuil_diff.items():
                if hasattr(declenchement, champ):
                    setattr(declenchement, champ, valeurs.get('nouveau'))

            declenchement.save()

            logs.append(Log(
                type="modification",
                nomTable="gimao_declencher",
                idCible={"id": declenchement.id},
                champsModifies=seuil_diff,
                utilisateur=utilisateur
            ))

        # ============================
        # 2. MISE À JOUR PLAN MAINTENANCE
        # ============================
        plan = declenchement.planMaintenance

        if plan and pm_diff:
            for champ, valeurs in pm_diff.items():

                # Champs simples
                if champ in [
                    "nom",
                    "commentaire",
                    "necessiteHabilitationElectrique",
                    "necessitePermisFeu"
                ]:
                    setattr(plan, champ, valeurs.get("nouveau"))

                # Type de PM
                elif champ == "type_id":
                    plan.type_plan_maintenance_id = valeurs.get("nouveau")

                # Consommables
                elif champ == "consommables":
                    PlanMaintenanceConsommable.objects.filter(
                        plan_maintenance=plan
                    ).delete()

                    for c in valeurs.get("nouveau", []):
                        PlanMaintenanceConsommable.objects.create(
                            plan_maintenance=plan,
                            consommable_id=c.get("consommable_id"),
                            quantite_necessaire=c.get("quantite_necessaire", 1)
                        )

                # Documents
                elif champ == "documents":
                    PlanMaintenanceDocument.objects.filter(
                        plan_maintenance=plan
                    ).delete()

                    for index, doc in enumerate(valeurs.get("nouveau", [])):
                        fichier = request.FILES.get(f'document_{index}')

                        document = Document.objects.create(
                            titre=doc.get("titre"),
                            type_id=doc.get("type"),
                            fichier=fichier
                        )

                        PlanMaintenanceDocument.objects.create(
                            plan_maintenance=plan,
                            document=document
                        )

            plan.save()

            logs.append(Log(
                type="modification",
                nomTable="gimao_plan_maintenance",
                idCible={"id": plan.id},
                champsModifies=pm_diff,
                utilisateur=utilisateur
            ))

        # ============================
        # 3. LOGS
        # ============================
        if logs:
            Log.objects.bulk_create(logs)

        return Response(
            {"detail": "Modifications appliquées avec succès"},
            status=status.HTTP_200_OK
        )