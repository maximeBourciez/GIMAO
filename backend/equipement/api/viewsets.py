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
        # Récupération des changements
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

        print(f"\n📝 CHANGEMENTS REÇUS: {changes}")

        # -------------------------
        # Traitement des modifications
        # -------------------------
        modifications_appliquees = {}

        # 1. Champs simples de l'équipement
        if 'prixAchat' in changes:
            ancien = equipement.prixAchat
            nouveau = changes['prixAchat']['nouvelle']
            if str(ancien) != str(nouveau):
                equipement.prixAchat = nouveau
                modifications_appliquees['prixAchat'] = {
                    'ancien': ancien,
                    'nouveau': nouveau
                }

        if 'fabricant' in changes:
            ancien = equipement.fabricant_id
            nouveau = changes['fabricant']['nouvelle']
            if ancien != nouveau:
                try:
                    fabricant = Fabricant.objects.get(id=nouveau)
                    equipement.fabricant = fabricant
                    modifications_appliquees['fabricant'] = {
                        'ancien': ancien,
                        'nouveau': nouveau
                    }
                except Fabricant.DoesNotExist:
                    pass

        # 2. Statut
        if 'statut' in changes:
            dernier_statut = equipement.statuts.order_by('-dateChangement').first()
            ancien_statut = dernier_statut.statut if dernier_statut else None
            nouveau_statut = changes['statut']['nouvelle']
            
            if ancien_statut != nouveau_statut:
                StatutEquipement.objects.create(
                    equipement=equipement,
                    statut=nouveau_statut,
                    dateChangement=timezone.now()
                )
                modifications_appliquees['statut'] = {
                    'ancien': ancien_statut,
                    'nouveau': nouveau_statut
                }

        # 3. Consommables
        if 'consommables' in changes:
            old_consommables = set(equipement.constituer_set.values_list('consommable_id', flat=True))
            new_consommables = set(changes['consommables']['nouvelle'])
            
            if old_consommables != new_consommables:
                # Supprimer
                to_remove = old_consommables - new_consommables
                if to_remove:
                    equipement.constituer_set.filter(consommable_id__in=to_remove).delete()
                
                # Ajouter
                to_add = new_consommables - old_consommables
                for consommable_id in to_add:
                    Constituer.objects.create(
                        equipement=equipement,
                        consommable_id=consommable_id
                    )
                
                modifications_appliquees['consommables'] = {
                    'ajoutes': list(to_add),
                    'retires': list(to_remove)
                }

        # 4. Compteurs
        if 'compteurs' in changes:
            compteurs_data = changes['compteurs']
            
            # Initialiser la structure pour les modifications de compteurs
            compteur_modifications = {
                'ajoutes': [],
                'modifies': [],
                'supprimes': []
            }
            
            # Compteurs à supprimer
            if 'supprimes' in compteurs_data:
                for compteur_id in compteurs_data['supprimes']:
                    try:
                        compteur = Compteur.objects.get(id=compteur_id, equipement=equipement)
                        nom_compteur = compteur.nomCompteur
                        
                        # Supprimer le compteur
                        compteur.delete()
                        
                        # Ajouter au log
                        compteur_modifications['supprimes'].append({
                            'id': compteur_id,
                            'nom': nom_compteur
                        })
                        
                        print(f"🗑️ Compteur supprimé: {nom_compteur} (ID: {compteur_id})")
                        
                    except Compteur.DoesNotExist:
                        print(f"⚠️ Compteur à supprimer introuvable: ID {compteur_id}")
            
            # Compteurs à ajouter
            if 'ajoutes' in compteurs_data:
                for nouveau_compteur in compteurs_data['ajoutes']:
                    try:
                        compteur = self._create_compteur_from_data(equipement, nouveau_compteur, request)
                        
                        # Ajouter au log
                        compteur_modifications['ajoutes'].append({
                            'id': compteur.id,
                            'nom': compteur.nomCompteur,
                            'donnees': {
                                'valeurCourante': nouveau_compteur.get('valeurCourante'),
                                'intervalle': nouveau_compteur.get('intervalle'),
                                'unite': nouveau_compteur.get('unite')
                            }
                        })
                        
                        print(f"➕ Compteur ajouté: {compteur.nomCompteur} (ID: {compteur.id})")
                        
                    except Exception as e:
                        print(f"❌ Erreur lors de l'ajout du compteur: {e}")
            
            # Compteurs à modifier
            if 'modifies' in compteurs_data:
                for compteur_modifie in compteurs_data['modifies']:
                    if 'id' in compteur_modifie:
                        try:
                            compteur = Compteur.objects.get(id=compteur_modifie['id'], equipement=equipement)
                            
                            # Capturer l'état avant modification
                            etat_avant = {
                                'nom': compteur.nomCompteur,
                                'valeurCourante': compteur.valeurCourante,
                                'intervalle': compteur.ecartInterventions,
                                'unite': compteur.unite,
                                'derniereIntervention': compteur.derniereIntervention,
                                'estPrincipal': compteur.estPrincipal,
                                'estGlissant': compteur.estGlissant,
                                'habElec': compteur.necessiteHabilitationElectrique,
                                'permisFeu': compteur.necessitePermisFeu
                            }
                            
                            # Appliquer les modifications
                            modifications_detaillees = self._update_compteur_from_changes(
                                compteur, 
                                compteur_modifie['modifications']
                            )
                            
                            # Ajouter au log si des modifications ont été appliquées
                            if modifications_detaillees:
                                compteur_modifications['modifies'].append({
                                    'id': compteur.id,
                                    'nom': compteur.nomCompteur,
                                    'modifications': modifications_detaillees
                                })
                                
                                print(f"✏️ Compteur modifié: {compteur.nomCompteur} (ID: {compteur.id})")
                            
                        except Compteur.DoesNotExist:
                            print(f"⚠️ Compteur à modifier introuvable: ID {compteur_modifie['id']}")
                        except Exception as e:
                            print(f"❌ Erreur lors de la modification du compteur: {e}")
            
            # Ajouter les modifications de compteurs au log global si il y a eu des changements
            if any([compteur_modifications['ajoutes'], 
                    compteur_modifications['modifies'], 
                    compteur_modifications['supprimes']]):
                
                modifications_appliquees['compteurs'] = compteur_modifications

        # Sauvegarder l'équipement si des modifications ont été faites
        if modifications_appliquees:
            equipement.save()

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

    def _create_compteur_from_data(self, equipement, compteur_data, request):
        """Crée un nouveau compteur à partir des données"""
        compteur = Compteur.objects.create(
            equipement=equipement,
            nomCompteur=compteur_data['nom'],
            descriptifMaintenance=compteur_data.get('description', ''),
            valeurCourante=compteur_data['valeurCourante'],
            ecartInterventions=compteur_data['intervalle'],
            unite=compteur_data['unite'],
            estPrincipal=compteur_data.get('estPrincipal', False),
            estGlissant=compteur_data.get('estGlissant', False),
            necessiteHabilitationElectrique=compteur_data.get('habElec', False),
            necessitePermisFeu=compteur_data.get('permisFeu', False),
            prochaineMaintenance=int(compteur_data.get('derniereIntervention', 0)) + int(compteur_data['intervalle']),
            derniereIntervention=compteur_data.get('derniereIntervention', 0)
        )
        
        # Gérer le plan de maintenance si présent
        if 'planMaintenance' in compteur_data:
            self._create_plan_maintenance(compteur, compteur_data['planMaintenance'], request)
        
        return compteur

    def _update_compteur_from_changes(self, compteur, modifications):
        """Met à jour un compteur existant"""
        # Mise à jour des champs simples
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
        
        for field, model_field in field_mapping.items():
            if field in modifications:
                nouvelle_valeur = modifications[field]['nouveau']
                setattr(compteur, model_field, nouvelle_valeur)
        
        # Mettre à jour la prochaine maintenance
        if 'derniereIntervention' in modifications and 'intervalle' in modifications:
            compteur.prochaineMaintenance = (
                int(modifications['derniereIntervention']['nouveau']) + 
                int(modifications['intervalle']['nouveau'])
            )
        
        compteur.save()
        
        # Gérer le plan de maintenance si modifié
        if 'planMaintenance' in modifications:
            self._update_plan_maintenance(compteur, modifications['planMaintenance'])

    def _create_plan_maintenance(self, compteur, pm_data, request):
        """Crée un nouveau plan de maintenance"""
        if not pm_data:
            return None
        
        plan = PlanMaintenance.objects.create(
            compteur=compteur,
            equipement=compteur.equipement,
            nom=pm_data['nom'],
            type_plan_maintenance_id=pm_data['type']
        )
        
        compteur.planMaintenance = plan
        compteur.save()
        
        # Consommables
        for cpm in pm_data.get('consommables', []):
            PlanMaintenanceConsommable.objects.create(
                plan_maintenance=plan,
                consommable_id=cpm['consommable'],
                quantite_necessaire=cpm['quantite']
            )
        
        # Documents (simplifié - fichiers non gérés dans les changements)
        
        return plan

    def _update_plan_maintenance(self, compteur, pm_modifications):
        """Met à jour un plan de maintenance existant"""
        if not compteur.planMaintenance:
            return
        
        plan = compteur.planMaintenance
        
        if 'nom' in pm_modifications:
            plan.nom = pm_modifications['nom']['nouveau']
        
        if 'type' in pm_modifications:
            plan.type_plan_maintenance_id = pm_modifications['type']['nouveau']
        
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