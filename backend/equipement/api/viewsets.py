import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone

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
    EquipementCreateSerializer
)

from maintenance.models import PlanMaintenance, PlanMaintenanceConsommable, PlanMaintenanceDocument
from donnees.models import Lieu, Document


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
        Log.objects.create(
            type=type_action,
            nomTable=nom_table,
            idCible=id_cible,
            champsModifies=champs_modifies,
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

        for field in ["consommables", "compteurs"]:
            if field in data and isinstance(data[field], str):
                data[field] = json.loads(data[field])

        # Validation serializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Récupération des dépendances
        user = Utilisateur.objects.get(id=data["createurEquipement"])
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
            createurEquipement=user,
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

        # Compteurs & plans de maintenance
        for compteur_index, cp in enumerate(data.get("compteurs", [])):
            compteur = Compteur.objects.create(
                equipement=equipement,
                nomCompteur=cp["nom"],
                descriptifMaintenance=cp.get("description", ""),
                valeurCourante=cp["valeurCourante"],
                ecartInterventions=cp["intervalle"],
                unite=cp["unite"],
                estPrincipal=cp.get("estPrincipal", False),
                estGlissant=cp.get("estGlissant", False),
                necessiteHabilitationElectrique=cp.get("habElec", False),
                necessitePermisFeu=cp.get("permisFeu", False),
                prochaineMaintenance=(
                    int(cp["derniereIntervention"]) + int(cp["intervalle"])
                ),
                derniereIntervention=cp.get("derniereIntervention", 0)
            )

            pm = cp.get("planMaintenance")
            if not pm:
                continue

            plan = PlanMaintenance.objects.create(
                compteur=compteur,
                equipement=equipement,
                nom=pm["nom"],
                type_plan_maintenance_id=pm["type"]
            )

            compteur.planMaintenance = plan
            compteur.save()

            # Consommables du plan
            for cpm in pm.get("consommables", []):
                PlanMaintenanceConsommable.objects.create(
                    plan_maintenance=plan,
                    consommable_id=cpm["consommable"],
                    quantite_necessaire=cpm["quantite"]
                )

            # Documents du plan
            for doc_index, doc in enumerate(pm.get("documents", [])):
                file_key = f"compteur_{compteur_index}_document_{doc_index}"
                uploaded_file = request.FILES.get(file_key)

                if uploaded_file:
                    document = Document.objects.create(
                        nomDocument=doc.get("titre", uploaded_file.name),
                        cheminAcces=uploaded_file,
                        typeDocument_id=doc.get("type")
                    )

                    PlanMaintenanceDocument.objects.create(
                        plan_maintenance=plan,
                        document=document
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

        # Récupérer les données JSON
        json_data = data.get("data")
        if not json_data:
            return Response(
                {"error": "Aucune donnée JSON fournie"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            equipement_data = json.loads(json_data)
        except json.JSONDecodeError:
            return Response(
                {"error": "Format JSON invalide pour les données de l'équipement"},
                status=status.HTTP_400_BAD_REQUEST
            )

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
        print(f"  JSON: {equipement_data}")
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

        # 3. Compteurs
        if 'compteurs' in changes:
            compteurs_data = changes['compteurs']
            
            # Compteurs à supprimer
            if 'supprimes' in compteurs_data:
                for compteur_id in compteurs_data['supprimes']:
                    try:
                        compteur = Compteur.objects.get(id=compteur_id, equipement=equipement)
                        nom_compteur = compteur.nomCompteur
                        
                        # Supprimer le compteur
                        compteur.delete()
                        
                        print(f"Compteur supprimé: {nom_compteur} (ID: {compteur_id})")
                        
                        # Log de suppression
                        self._create_log_entry(
                            type_action='suppression',
                            nom_table='compteur',
                            id_cible={'compteur_id': compteur_id},
                            champs_modifies={'compteur_deleted': True, 'equipmentId': equipement.id, 'nomCompteur': nom_compteur},
                            utilisateur=utilisateur
                        )
                        
                    except Compteur.DoesNotExist:
                        print(f"Compteur à supprimer introuvable: ID {compteur_id}")
            
            # Compteurs à modifier
            if 'modifies' in compteurs_data:
                for compteur_mod in compteurs_data['modifies']:
                    compteur_id = compteur_mod.get('id')
                    if not compteur_id:
                        continue
                    
                    try:
                        compteur = Compteur.objects.get(id=compteur_id, equipement=equipement)
                        modifications = compteur_mod.get('modifications', {})
                        
                        # Mettre à jour les champs du compteur
                        self._update_compteur_from_changes(compteur, modifications, request)
                        
                        print(f"Compteur modifié: {compteur.nomCompteur} (ID: {compteur_id})")
                        
                        # Log de modification
                        self._create_log_entry(
                            type_action='modification',
                            nom_table='compteur',
                            id_cible={'compteur_id': compteur_id},
                            champs_modifies={'modifications': modifications},
                            utilisateur=utilisateur
                        )
                        
                    except Compteur.DoesNotExist:
                        print(f"Compteur à modifier introuvable: ID {compteur_id}")
                    except Exception as e:
                        print(f"Erreur lors de la modification du compteur {compteur_id}: {e}")

        # 4. Gestion des fichiers d'image de l'équipement
        if 'lienImageEquipement' in request.FILES:
            uploaded_file = request.FILES['lienImageEquipement']
            # Supprimer l'ancienne image si elle existe
            if equipement.lienImage:
                try:
                    equipement.lienImage.delete(save=False)
                except:
                    pass
            
            # Sauvegarder la nouvelle image
            equipement.lienImage = uploaded_file
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
        
        field_mapping = {
            'nom': 'nomCompteur',
            'description': 'descriptifMaintenance',
            'valeurCourante': 'valeurCourante',
            'intervalle': 'ecartInterventions',
            'unite': 'unite',
            'derniereIntervention': 'derniereIntervention',
            'estPrincipal': 'estPrincipal',
            'estGlissant': 'estGlissant',
            'habElec': 'necessiteHabilitationElectrique',
            'permisFeu': 'necessitePermisFeu'
        }
        
        # Mise à jour des champs simples
        for field, model_field in field_mapping.items():
            if field in modifications:
                field_data = modifications[field]
                nouvelle_valeur = field_data.get('nouvelle')
                if nouvelle_valeur is not None:
                    old_value = getattr(compteur, model_field)
                    if str(old_value) != str(nouvelle_valeur):
                        setattr(compteur, model_field, nouvelle_valeur)
                        print(f"  {field}: {old_value} -> {nouvelle_valeur}")
        
        # Mettre à jour la prochaine maintenance
        if 'derniereIntervention' in modifications and 'intervalle' in modifications:
            derniere = modifications['derniereIntervention'].get('nouvelle')
            intervalle = modifications['intervalle'].get('nouvelle')
            if derniere is not None and intervalle is not None:
                try:
                    compteur.prochaineMaintenance = int(derniere) + int(intervalle)
                    print(f"  Prochaine maintenance: {compteur.prochaineMaintenance}")
                except (ValueError, TypeError):
                    pass
        
        compteur.save()
        
        # Gérer le plan de maintenance si présent dans les modifications
        plan_keys = [k for k in modifications.keys() if k.startswith('planMaintenance')]
        if plan_keys:
            print(f"  Modification du plan de maintenance: {plan_keys}")
            self._update_plan_maintenance_from_changes(compteur, modifications, request)

    def _update_plan_maintenance_from_changes(self, compteur, modifications, request):
        """Met à jour le plan de maintenance d'un compteur"""
        print(f"Traitement du plan de maintenance pour compteur {compteur.id}")
        
        # Vérifier si un plan existe, sinon en créer un
        if not compteur.planMaintenance:
            print("  Création d'un nouveau plan de maintenance")
            # Extraire les données du plan depuis equipement_data
            # (Vous devrez passer les données complètes depuis l'update)
            # Pour l'instant, on va créer un plan vide
            plan = PlanMaintenance.objects.create(
                compteur=compteur,
                equipement=compteur.equipement,
                nom="Nouveau plan",
                type_plan_maintenance_id=1  # Type par défaut
            )
            compteur.planMaintenance = plan
            compteur.save()
        
        plan = compteur.planMaintenance
        
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
                print(f"  Type du plan: {plan.type_plan_maintenance_id} -> {new_type})")
                plan.type_plan_maintenance_id = new_type
        
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
                    if isinstance(conso, dict) and conso.get('consommable') == consommable_id:
                        quantite = conso.get('quantite', 1)
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


class CompteurViewSet(viewsets.ModelViewSet):
    queryset = Compteur.objects.all()
    serializer_class = CompteurSerializer

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """Mise à jour d'un compteur - gère aussi le plan de maintenance"""
        compteur = self.get_object()
        data = request.data

        compteurData = data.get("compteur")
        rawChanges = data.get("changes")

        print(f" Changes - {rawChanges}")
        print(f"📁 Fichiers reçus - {list(request.FILES.keys())}")

        try:
            changes = json.loads(rawChanges) if rawChanges else {}
        except json.JSONDecodeError:
            changes = {}

        PLAN_MAINTENANCE_KEYS = [
            'planMaintenance.nom',
            'planMaintenance.type',
            'planMaintenance.consommables',
            'planMaintenance.documents' 
        ]

        COMPTEUR_KEYS = [
            'nom',
            'description',
            'valeurCourante',
            'intervalle',
            'unite',
            'derniereIntervention',
            'estPrincipal',
            'estGlissant',
            'habElec',
            'permisFeu'
        ]

        field_mapping = {
            'nom': 'nomCompteur',
            'description': 'descriptifMaintenance',
            'valeurCourante': 'valeurCourante',
            'intervalle': 'ecartInterventions',
            'unite': 'unite',
            'derniereIntervention': 'derniereIntervention',
            'estPrincipal': 'estPrincipal',
            'estGlissant': 'estGlissant',
            'habElec': 'necessiteHabilitationElectrique',
            'permisFeu': 'necessitePermisFeu'
        }

        # Mise à jour des champs du compteur
        for field in COMPTEUR_KEYS:
            if field in changes:
                field_data = changes[field]
                print(f" Champ à mettre à jour: {field} - {field_data}")
                nouvelle_valeur = field_data.get('nouvelle')
                if nouvelle_valeur is not None:
                    old_value = getattr(compteur, field_mapping.get(field, field))
                    print(f"  Ancienne valeur: {old_value}, Nouvelle valeur: {nouvelle_valeur}")
                    if str(old_value) != str(nouvelle_valeur):
                        setattr(compteur, field_mapping.get(field, field), nouvelle_valeur)
                        print(f"  {field}: {old_value} -> {nouvelle_valeur}")
                        # Créer un log
                        self._create_log_entry(
                            type_action='modification',
                            nom_table='compteur',
                            id_cible={'compteur_id': compteur.id},
                            champs_modifies={field: {'ancien': old_value, 'nouveau': nouvelle_valeur}},
                            utilisateur=Utilisateur.objects.get(id=3)
                        )
        

        self._update_plan_maintenance_from_changes(compteur, changes, request)

        

        return Response(
            CompteurSerializer(compteur).data,
            status=status.HTTP_200_OK
        )
    
    def _update_plan_maintenance_from_changes(self, compteur, modifications, request):
        """Met à jour le plan de maintenance d'un compteur"""
        print(f" Traitement du plan de maintenance pour compteur {compteur.id}")
    
        # Vérifier si un plan existe, sinon en créer un
        if not compteur.planMaintenance or compteur.planMaintenance is None:
            print(" Création d'un nouveau plan de maintenance")
            self._createNewPlan(compteur, modifications, request)
        
        plan = compteur.planMaintenance
        
        # Mise à jour du nom
        if 'planMaintenance.nom' in modifications:
            new_name = modifications['planMaintenance.nom'].get('nouvelle')
            if new_name and plan.nom != new_name:
                print(f"  Nom du plan: {plan.nom} -> {new_name}")
                plan.nom = new_name

                self._create_log_entry(
                    type_action='modification',
                    nom_table='plan_maintenance',
                    id_cible={'plan_maintenance_id': plan.id},
                    champs_modifies={'nom': {'ancien': plan.nom , 'nouveau': new_name}},
                    utilisateur=Utilisateur.objects.get(id=3)
                )
        
        # Mise à jour du type
        if 'planMaintenance.type' in modifications:
            new_type = modifications['planMaintenance.type'].get('nouvelle')
            if new_type and plan.type_plan_maintenance_id != new_type:
                print(f"  📝 Type du plan: {plan.type_plan_maintenance_id} -> {new_type}")
                plan.type_plan_maintenance_id = new_type
                self._create_log_entry(
                    type_action='modification',
                    nom_table='plan_maintenance',
                    id_cible={'plan_maintenance_id': plan.id},
                    champs_modifies={'type_plan_maintenance': {'ancien': plan.type_plan_maintenance_id  , 'nouveau': new_type}},
                    utilisateur=Utilisateur.objects.get(id=3)
                )
        
        # Mise à jour des consommables
        if 'planMaintenance.consommables' in modifications:
            consommables_data = modifications['planMaintenance.consommables']
            
            consommables_existants = plan.planmaintenanceconsommable_set.all()
            consommables_existants_ids = set(consommable.consommable_id for consommable in consommables_existants)

            nouveaux_consommables = consommables_data.get('nouvelle', [])

            for conso in nouveaux_consommables:
                conso_id = conso.get('consommable')
                quantite = conso.get('quantite', 1)

                if conso_id not in consommables_existants_ids:
                    # Ajouter le nouveau consommable
                    PlanMaintenanceConsommable.objects.create(
                        plan_maintenance=plan,
                        consommable_id=conso_id,
                        quantite_necessaire=quantite
                    )
                    print(f"  Consommable ajouté: {conso_id} (Quantité: {quantite})")

                    self._create_log_entry(
                        type_action='ajout',
                        nom_table='plan_maintenance_consommable',
                        id_cible={'plan_maintenance_id': plan.id, 'consommable_id': conso_id},
                        champs_modifies={'quantite_necessaire': quantite},
                        utilisateur=Utilisateur.objects.get(id=3)   
                    )

                else:
                    # Mettre à jour la quantité si nécessaire
                    conso_obj = consommables_existants.get(consommable_id=conso_id)
                    if conso_obj.quantite_necessaire != quantite:
                        old_quantity = conso_obj.quantite_necessaire
                        conso_obj.quantite_necessaire = quantite
                        conso_obj.save()
                        print(f"  Consommable mis à jour: {conso_id} (Quantité: {old_quantity} -> {quantite})")

                        self._create_log_entry(
                            type_action='modification',
                            nom_table='plan_maintenance_consommable',
                            id_cible={'plan_maintenance_id': plan.id, 'consommable_id': conso_id},
                            champs_modifies={'quantite_necessaire': {'ancien': old_quantity, 'nouveau': quantite}},
                            utilisateur=Utilisateur.objects.get(id=3)   
                        )
                
            for old_conso in consommables_existants:
                if old_conso.consommable_id not in [c.get('consommable') for c in nouveaux_consommables]:
                    # Supprimer le consommable retiré
                    old_conso.delete()
                    print(f"  Consommable supprimé: {old_conso.consommable_id}")

                    self._create_log_entry(
                        type_action='suppression',
                        nom_table='plan_maintenance_consommable',
                        id_cible={'plan_maintenance_id': plan.id, 'consommable_id': old_conso.consommable_id},
                        champs_modifies={},
                        utilisateur=Utilisateur.objects.get(id=3)   
                    )

        # Mise à jour des documents
        if 'planMaintenance.documents' in modifications:
            documents_data = modifications['planMaintenance.documents']

            ajouts = documents_data.get('ajouts', [])
            modifications_docs = documents_data.get('modifications', [])
            suppressions = documents_data.get('suppressions', [])

            print(f"  Documents: {len(ajouts)} ajout(s), {len(modifications_docs)} modification(s), {len(suppressions)} suppression(s)")

            # ====== Mapping des fichiers reçus ======
            file_mapping = {}
            for key, file in request.FILES.items():
                if key.startswith('file_planMaintenance.documents_'):
                    try:
                        index = int(key.split('_')[-1])
                        file_mapping[index] = file
                    except ValueError:
                        continue

            # ====== AJOUTS ======
            for index, doc_data in enumerate(ajouts):
                file = file_mapping.get(index)

                if not file:
                    print(f"  Ajout sans fichier ignoré: {doc_data}")
                    continue

                document = Document.objects.create( 
                    nomDocument=doc_data.get('titre', file.name),
                    cheminAcces=file,
                    typeDocument_id=doc_data.get('type')
                )

                PlanMaintenanceDocument.objects.create(
                    plan_maintenance=plan,
                    document=document
                )

                self._create_log_entry(
                    type_action='ajout',
                    nom_table='document',
                    id_cible={'document_id': document.id},
                    champs_modifies={'titre': doc_data.get('titre')},
                    utilisateur=Utilisateur.objects.get(id=3)
                )

                print(f"  📎 Document ajouté: {document.nomDocument}")

            # ====== MODIFICATIONS ======
            for index, modif in enumerate(modifications_docs):
                ancienne = modif.get('ancienne')
                nouvelle = modif.get('nouvelle')

                if not ancienne or not nouvelle:
                    continue

                doc_id = nouvelle.get('id')
                file = file_mapping.get(index)

                try:
                    document = Document.objects.get(id=doc_id)
                except Document.DoesNotExist:
                    continue

                if file:
                    document.cheminAcces = file

                if ancienne.get('titre') != nouvelle.get('titre'):
                    document.nomDocument = nouvelle.get('titre')

                if ancienne.get('type') != nouvelle.get('type'):
                    document.typeDocument_id = nouvelle.get('type')

                document.save()

                self._create_log_entry(
                    type_action='modification',
                    nom_table='document',
                    id_cible={'document_id': document.id},
                    champs_modifies={'avant': ancienne, 'apres': nouvelle},
                    utilisateur=Utilisateur.objects.get(id=3)
                )

                print(f"  Document modifié: {document.nomDocument}")

            # ====== SUPPRESSIONS ======
            for doc_id in suppressions:
                try:
                    document = Document.objects.get(id=doc_id)
                    document.delete()

                    self._create_log_entry(
                        type_action='suppression',
                        nom_table='document',
                        id_cible={'document_id': doc_id},
                        champs_modifies={},
                        utilisateur=Utilisateur.objects.get(id=3)
                    )

                    print(f"  Document supprimé ID={doc_id}")
                except Document.DoesNotExist:
                    continue

        plan.save()                
    
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