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


class EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return EquipementCreateSerializer
        return EquipementSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        data = dict(request.data)
        
        # Extraire les valeurs uniques des listes (QueryDict met tout en liste)
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        # -------------------------
        # Normalisation des champs simples
        # -------------------------

        # lieu : objet -> id
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

        # Champs JSON envoyés en string
        for field in ["consommables", "compteurs"]:
            if field in data and isinstance(data[field], str):
                data[field] = json.loads(data[field])

        print("\n✅ DONNÉES NORMALISÉES:", data)

        # -------------------------
        # Validation serializer
        # -------------------------
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # -------------------------
        # Récupération des dépendances
        # -------------------------
        user = Utilisateur.objects.get(id=data["createurEquipement"])
        modele = ModeleEquipement.objects.get(id=data["modeleEquipement"])
        fabricant = Fabricant.objects.get(id=data["fabricant"])
        fournisseur = Fournisseur.objects.get(id=data["fournisseur"])
        famille = FamilleEquipement.objects.get(id=data["famille"])
        lieu = Lieu.objects.get(id=data["lieu"])

        # -------------------------
        # Création de l'équipement
        # -------------------------
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

        # -------------------------
        # Statut de l'équipement
        # -------------------------
        statut = data.get("statut") 
        if statut:
            StatutEquipement.objects.create(
                equipement=equipement,
                statut=statut,
                dateChangement=timezone.now()
            )

        # -------------------------
        # Consommables
        # -------------------------
        for consommable_id in data.get("consommables", []):
            Constituer.objects.create(
                equipement=equipement,
                consommable_id=consommable_id
            )

        # -------------------------
        # Compteurs & plans de maintenance
        # -------------------------
        for compteur_index, cp in enumerate(data.get("compteurs", [])):
            print(f"\n🔧 Traitement compteur #{compteur_index}: {cp.get('nom')}")
            
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
                derniereIntervention= cp.get("derniereIntervention", 0)
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

            # Associer le plan au compteur
            compteur.planMaintenance = plan

            # Consommables du plan
            for cpm in pm.get("consommables", []):
                PlanMaintenanceConsommable.objects.create(
                    plan_maintenance=plan,
                    consommable_id=cpm["consommable"],
                    quantite_necessaire=cpm["quantite"]
                )

            # -------------------------
            # Documents du plan
            # -------------------------
            for doc_index, doc in enumerate(pm.get("documents", [])):
                # Cherche le fichier avec le nouveau format
                file_key = f"compteur_{compteur_index}_document_{doc_index}"
                uploaded_file = request.FILES.get(file_key)

                if not uploaded_file:
                    continue

                # Créer le document
                document = Document.objects.create(
                    nomDocument=doc.get("titre", uploaded_file.name),
                    cheminAcces=uploaded_file,
                    typeDocument_id=doc.get("type")
                )

                # Lier au plan de maintenance
                PlanMaintenanceDocument.objects.create(
                    plan_maintenance=plan,
                    document=document
                )

        return Response(
            EquipementSerializer(equipement).data,
            status=status.HTTP_201_CREATED
        )


    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Méthode PUT pour mettre à jour un équipement.
        Gère les modifications, créations et suppressions.
        """
        equipement = self.get_object()
        utilisateur = self._get_utilisateur(request)
        
        # -------------------------
        # Normalisation des données
        # -------------------------
        data = dict(request.data)
        
        # Extraire les valeurs uniques des listes
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]

        # Normalisation lieu
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

        # Décoder les champs JSON
        for field in ["consommables", "compteurs"]:
            if field in data and isinstance(data[field], str):
                data[field] = json.loads(data[field])

        # Récupérer les changements détectés par le frontend
        changes_data = data.get("changes")
        if changes_data:
            changes = json.loads(changes_data)
        else:
            changes = {}

        print(f"\n📝 CHANGEMENTS DÉTECTÉS: {changes}")
        
        # Collecteur de modifications pour le log
        all_modifications = {}

        # -------------------------
        # 1. Mise à jour des champs simples de l'équipement
        # -------------------------
        equipement_modifications = {}
        
        # Mise à jour des champs directs
        field_mapping = {
            'numSerie': 'numSerie',
            'reference': 'reference',
            'designation': 'designation',
            'prixAchat': 'prixAchat',
        }
        
        for field, model_field in field_mapping.items():
            if field in data:
                old_value = getattr(equipement, model_field)
                new_value = data[field]
                
                # Conversion pour comparaison
                if field == 'prixAchat':
                    old_value = float(old_value) if old_value else None
                    new_value = float(new_value) if new_value not in ['', None] else None
                
                if old_value != new_value:
                    setattr(equipement, model_field, new_value)
                    equipement_modifications[field] = {
                        'ancien': old_value,
                        'nouveau': new_value
                    }
        
        # -------------------------
        # 2. Mise à jour des relations ForeignKey
        # -------------------------
        relations_mapping = {
            'modeleEquipement': ('modele', ModeleEquipement),
            'fabricant': ('fabricant', Fabricant),
            'fournisseur': ('fournisseur', Fournisseur),
            'famille': ('famille', FamilleEquipement),
            'lieu': ('lieu', Lieu)
        }
        
        for field, (relation_name, model_class) in relations_mapping.items():
            if field in data and data[field] not in ['', None]:
                old_id = getattr(equipement, f"{relation_name}_id")
                new_id = int(data[field])
                
                if old_id != new_id:
                    try:
                        new_instance = model_class.objects.get(id=new_id)
                        setattr(equipement, relation_name, new_instance)
                        equipement_modifications[field] = {
                            'ancien': old_id,
                            'nouveau': new_id
                        }
                    except model_class.DoesNotExist:
                        print(f"⚠️ {relation_name} avec ID {new_id} introuvable")
        
        # Sauvegarder l'équipement
        if equipement_modifications:
            equipement.save()
            all_modifications['equipement'] = equipement_modifications
        
        # -------------------------
        # 3. Mise à jour du statut
        # -------------------------
        if 'statut' in data:
            dernier_statut = equipement.statuts.order_by('-dateChangement').first()
            old_statut = dernier_statut.statut if dernier_statut else None
            new_statut = data['statut']
            
            if old_statut != new_statut:
                StatutEquipement.objects.create(
                    equipement=equipement,
                    statut=new_statut,
                    dateChangement=timezone.now()
                )
                all_modifications['statut'] = {
                    'ancien': old_statut,
                    'nouveau': new_statut
                }
        
        # -------------------------
        # 4. Mise à jour des consommables
        # -------------------------
        if 'consommables' in data:
            old_consommables = set(equipement.constituer_set.values_list('consommable_id', flat=True))
            new_consommables = set([int(c) for c in data['consommables']])
            
            if old_consommables != new_consommables:
                # Supprimer les anciennes associations
                to_remove = old_consommables - new_consommables
                if to_remove:
                    equipement.constituer_set.filter(consommable_id__in=to_remove).delete()
                
                # Ajouter les nouvelles associations
                to_add = new_consommables - old_consommables
                for consommable_id in to_add:
                    Constituer.objects.create(
                        equipement=equipement,
                        consommable_id=consommable_id
                    )
                
                all_modifications['consommables'] = {
                    'anciens': list(old_consommables),
                    'nouveaux': list(new_consommables),
                    'ajoutes': list(to_add),
                    'retires': list(to_remove)
                }
        
        # -------------------------
        # 5. Traitement des compteurs
        # -------------------------
        compteur_modifications = {
            'ajoutes': [],
            'modifies': [],
            'supprimes': []
        }
        
        # Récupérer les IDs des compteurs existants
        existing_counter_ids = set(equipement.compteurs.values_list('id', flat=True))
        
        # Liste pour stocker les IDs à conserver
        counters_to_keep = []
        
        if 'compteurs' in data:
            for compteur_data in data['compteurs']:
                counter_id = compteur_data.get('id')
                
                if counter_id and counter_id in existing_counter_ids:
                    # Mise à jour d'un compteur existant
                    try:
                        counter = Compteur.objects.get(id=counter_id, equipement=equipement)
                        counter_changes = self._update_counter(counter, compteur_data)
                        
                        if counter_changes:
                            compteur_modifications['modifies'].append({
                                'id': counter_id,
                                'nom': counter.nomCompteur,
                                'modifications': counter_changes
                            })
                        
                        counters_to_keep.append(counter_id)
                        
                    except Compteur.DoesNotExist:
                        # Cas improbable : ID existe mais pas dans la DB
                        new_counter = self._create_counter(equipement, compteur_data)
                        compteur_modifications['ajoutes'].append({
                            'id': new_counter.id,
                            'nom': new_counter.nomCompteur
                        })
                        counters_to_keep.append(new_counter.id)
                else:
                    # Création d'un nouveau compteur
                    new_counter = self._create_counter(equipement, compteur_data)
                    compteur_modifications['ajoutes'].append({
                        'id': new_counter.id,
                        'nom': new_counter.nomCompteur
                    })
                    counters_to_keep.append(new_counter.id)
        
        # Supprimer les compteurs non conservés
        counters_to_delete = existing_counter_ids - set(counters_to_keep)
        
        # Vérifier aussi les suppressions explicites depuis les changes
        if 'compteurs' in changes:
            explicit_deletions = changes['compteurs'].get('supprimes', [])
            counters_to_delete.update(set(explicit_deletions))
        
        if counters_to_delete:
            deleted_counters = equipement.compteurs.filter(id__in=counters_to_delete)
            for counter in deleted_counters:
                compteur_modifications['supprimes'].append({
                    'id': counter.id,
                    'nom': counter.nomCompteur
                })
            
            # Supprimer les compteurs
            deleted_counters.delete()
        
        # Ajouter aux modifications globales seulement si il y a des changements
        if any([compteur_modifications['ajoutes'], 
                compteur_modifications['modifies'], 
                compteur_modifications['supprimes']]):
            all_modifications['compteurs'] = compteur_modifications
        
        # -------------------------
        # 6. Gestion de l'image
        # -------------------------
        if 'lienImageEquipement' in request.FILES:
            old_image = equipement.lienImage
            equipement.lienImage = request.FILES['lienImageEquipement']
            equipement.save()
            
            all_modifications['image'] = {
                'ancienne': str(old_image) if old_image else None,
                'nouvelle': 'Nouvelle image uploadée'
            }
        
        # -------------------------
        # 7. Log des modifications
        # -------------------------
        if all_modifications:
            self._create_log_entry(
                type_action="modification",
                nom_table="equipement_equipement",
                id_cible=equipement.id,
                champs_modifies=all_modifications,
                utilisateur=utilisateur
            )
        
        print(f"\n✅ Mise à jour terminée. Modifications: {all_modifications}")
        
        return Response(
            EquipementSerializer(equipement).data,
            status=status.HTTP_200_OK
        )

    def _get_utilisateur(self, request):
        """Récupère l'utilisateur à partir de la requête"""
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                return Utilisateur.objects.get(user=request.user)
            except Utilisateur.DoesNotExist:
                return None
        return None

    def _create_log_entry(self, type_action, nom_table, id_cible, champs_modifies, utilisateur):
        """Crée une entrée dans le journal"""
        Log.objects.create(
            type=type_action,
            nomTable=nom_table,
            idCible=id_cible,
            champsModifies=champs_modifies,
            utilisateur=utilisateur,
            date=timezone.now()
        )

    def _update_counter(self, counter, data):
        """Met à jour un compteur existant"""
        modifications = {}
        
        # Mise à jour des champs de base
        field_mapping = {
            'nom': ('nomCompteur', 'Nom'),
            'description': ('descriptifMaintenance', 'Description'),
            'valeurCourante': ('valeurCourante', 'Valeur courante'),
            'intervalle': ('ecartInterventions', 'Intervalle'),
            'unite': ('unite', 'Unité'),
            'derniereIntervention': ('derniereIntervention', 'Dernière intervention'),
            'estPrincipal': ('estPrincipal', 'Principal'),
            'estGlissant': ('estGlissant', 'Glissant'),
            'habElec': ('necessiteHabilitationElectrique', 'Habilitation électrique'),
            'permisFeu': ('necessitePermisFeu', 'Permis feu')
        }
        
        for data_field, (model_field, display_name) in field_mapping.items():
            if data_field in data:
                old_value = getattr(counter, model_field)
                new_value = data[data_field]
                
                # Conversion pour comparaison
                if isinstance(old_value, bool) or isinstance(new_value, bool):
                    old_value = bool(old_value)
                    new_value = bool(new_value)
                elif data_field in ['valeurCourante', 'intervalle', 'derniereIntervention']:
                    old_value = int(old_value) if old_value is not None else None
                    new_value = int(new_value) if new_value not in ['', None] else None
                
                if old_value != new_value:
                    setattr(counter, model_field, new_value)
                    modifications[data_field] = {
                        'ancien': old_value,
                        'nouveau': new_value,
                        'display_name': display_name
                    }
        
        # Mettre à jour la prochaine maintenance si nécessaire
        if 'derniereIntervention' in data and 'intervalle' in data:
            counter.prochaineMaintenance = int(data['derniereIntervention']) + int(data['intervalle'])
        
        # Sauvegarder les modifications
        if modifications:
            counter.save()
        
        # Traiter le plan de maintenance
        pm_data = data.get('planMaintenance')
        if pm_data:
            pm_modifications = self._update_plan_maintenance(counter, pm_data)
            if pm_modifications:
                modifications['planMaintenance'] = pm_modifications
        
        return modifications

    def _create_counter(self, equipement, data):
        """Crée un nouveau compteur"""
        counter = Compteur.objects.create(
            equipement=equipement,
            nomCompteur=data['nom'],
            descriptifMaintenance=data.get('description', ''),
            valeurCourante=data['valeurCourante'],
            ecartInterventions=data['intervalle'],
            unite=data['unite'],
            estPrincipal=data.get('estPrincipal', False),
            estGlissant=data.get('estGlissant', False),
            necessiteHabilitationElectrique=data.get('habElec', False),
            necessitePermisFeu=data.get('permisFeu', False),
            prochaineMaintenance=int(data.get('derniereIntervention', 0)) + int(data['intervalle']),
            derniereIntervention=data.get('derniereIntervention', 0)
        )
        
        # Créer le plan de maintenance si présent
        pm_data = data.get('planMaintenance')
        if pm_data:
            self._create_plan_maintenance(counter, pm_data)
        
        return counter

    def _update_plan_maintenance(self, counter, pm_data):
        """Met à jour ou crée un plan de maintenance"""
        modifications = {}
        
        if not pm_data:
            # Supprimer le plan existant s'il y en a un
            if counter.planMaintenance:
                old_plan = counter.planMaintenance
                counter.planMaintenance = None
                counter.save()
                old_plan.delete()
                return {'plan_supprime': {'id': old_plan.id, 'nom': old_plan.nom}}
            return {}
        
        if counter.planMaintenance:
            # Mettre à jour le plan existant
            plan = counter.planMaintenance
            old_nom = plan.nom
            old_type = plan.type_plan_maintenance_id
            
            if 'nom' in pm_data and plan.nom != pm_data['nom']:
                plan.nom = pm_data['nom']
                modifications['nom'] = {
                    'ancien': old_nom,
                    'nouveau': pm_data['nom']
                }
            
            if 'type' in pm_data and plan.type_plan_maintenance_id != pm_data['type']:
                plan.type_plan_maintenance_id = pm_data['type']
                modifications['type'] = {
                    'ancien': old_type,
                    'nouveau': pm_data['type']
                }
            
            plan.save()
        else:
            # Créer un nouveau plan
            plan = PlanMaintenance.objects.create(
                compteur=counter,
                equipement=counter.equipement,
                nom=pm_data['nom'],
                type_plan_maintenance_id=pm_data['type']
            )
            counter.planMaintenance = plan
            counter.save()
            modifications['plan_cree'] = {'nom': plan.nom}
        
        return modifications if modifications else None

    def _create_plan_maintenance(self, counter, pm_data):
        """Crée un nouveau plan de maintenance"""
        if not pm_data:
            return None
        
        plan = PlanMaintenance.objects.create(
            compteur=counter,
            equipement=counter.equipement,
            nom=pm_data['nom'],
            type_plan_maintenance_id=pm_data['type']
        )
        
        counter.planMaintenance = plan
        counter.save()
        
        # Ajouter les consommables du plan
        for cpm in pm_data.get('consommables', []):
            PlanMaintenanceConsommable.objects.create(
                plan_maintenance=plan,
                consommable_id=cpm['consommable'],
                quantite_necessaire=cpm['quantite']
            )
        
        return plan




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