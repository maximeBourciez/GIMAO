from django.db import models
from exportData.formatters import generateCsvResponse, generateXlsxResponse

from equipement.models import Equipement, StatutEquipement, Compteur, ModeleEquipement, Declencher
from maintenance.models import BonTravail, DemandeIntervention, BonTravailConsommable
from stock.models import Consommable, PorterSur, Stocker, Magasin
from donnees.models import Fournisseur, Fabricant, Lieu
from utilisateur.models import Utilisateur, Log

exportRegistry = {}

def registerExporter(nom):
    """
    Decorator to register an exporter strategy into the exportRegistry.
    """
    def wrapper(cls):
        exportRegistry[nom] = cls
        return cls
    return wrapper

class BaseExportStrategy:
    """
    Abstract base class for all export strategies.
    Requires `model` to be defined in subclasses.
    """
    model = None

    def __init__(self, request_params):
        """
        :param request_params: Typically request.GET dictionary containing parameters like:
            - exportType: string
            - includeArchived: 'yes', 'no', 'both'
            - columns: list of strings (comma separated in HTTP)
            - fileType: 'csv', 'xlsx'
            - equipementId: ID for filtering
            - magasinId: ID for filtering
            - utilisateurId: ID for filtering
            - consoId: ID for filtering
        """
        self.params = request_params

    def get_queryset(self):
        """
        Fetches the initial queryset and applies the `includeArchived` filter conditionally.
        Then calls `apply_filters` which can be overridden by subclasses.
        """
        if not self.model:
            raise NotImplementedError("Subclasses must define a 'model'.")
        
        qs = self.model.objects.all()
        
        # Check if model has an `archive` field safely
        has_archive = any(field.name == 'archive' for field in self.model._meta.fields)

        if has_archive:
            include_archived = self.params.get('includeArchived', 'no')
            if include_archived == 'no':
                qs = qs.filter(archive=False)
            elif include_archived == 'yes':
                qs = qs.filter(archive=True)
            # 'both' means no filter
            
        qs = self.apply_filters(qs)
        return qs

    def apply_filters(self, qs):
        """
        Hook for subclasses to override and apply specific filters (like equipementId).
        """
        return qs

    def get_columns(self):
        """
        Extracts columns from the parameters. 
        Expects a comma-separated string: 'id,nom,etat'
        """
        columns_str = self.params.get('columns', '')
        if columns_str:
            return [col.strip() for col in columns_str.split(',') if col.strip()]
        return None

    def _get_field_metadata(self):
        """
        Builds a mapping {attname: label} and a set of boolean field attnames
        from the model's meta fields.
        """
        column_labels = {}
        boolean_fields = set()
        for field in self.model._meta.fields:
            column_labels[field.attname] = str(field.verbose_name).capitalize()
            if isinstance(field, models.BooleanField):
                boolean_fields.add(field.attname)
        return column_labels, boolean_fields

    def _format_data(self, data, boolean_fields):
        """
        Converts boolean values (True/False) to 'Oui'/'Non' in the data rows.
        """
        for row in data:
            for field_name in boolean_fields:
                if field_name in row:
                    val = row[field_name]
                    if val is True:
                        row[field_name] = 'Oui'
                    elif val is False:
                        row[field_name] = 'Non'
        return data

    def export(self):
        """
        Executes the export strategy:
        1. Fetch queryset
        2. Filter by columns if requested
        3. Convert booleans to Oui/Non
        4. Format into the requested fileType with readable headers
        """
        qs = self.get_queryset()
        columns = self.get_columns()
        column_labels, boolean_fields = self._get_field_metadata()

        if columns:
            data = list(qs.values(*columns))
        else:
            # If no columns specified, fetch all fields via values()
            data = list(qs.values())
            # Use all field attnames as columns to guarantee consistent ordering
            columns = [field.attname for field in self.model._meta.fields]

        # Convert booleans True/False → Oui/Non
        data = self._format_data(data, boolean_fields)

        file_type = self.params.get('fileType', 'csv').lower()
        export_type = self.params.get('exportType', 'export')
        
        if file_type == 'xlsx':
            return generateXlsxResponse(data, filename=export_type, columns=columns, column_labels=column_labels)
        else:
            return generateCsvResponse(data, filename=export_type, columns=columns, column_labels=column_labels)


# 1. Equipement
@registerExporter('equipement')
class EquipementStrategy(BaseExportStrategy):
    model = Equipement

# 2. Statut Equipement
@registerExporter('statut_equipement')
class StatutEquipementStrategy(BaseExportStrategy):
    model = StatutEquipement
    
    def apply_filters(self, qs):
        equipement_id = self.params.get('equipementId')
        if equipement_id:
            qs = qs.filter(equipement_id=equipement_id)
        return qs

# 3. BonTravail (bt)
@registerExporter('bt')
class BonTravailStrategy(BaseExportStrategy):
    model = BonTravail
    
    def apply_filters(self, qs):
        equipement_id = self.params.get('equipementId')
        if equipement_id:
            qs = qs.filter(demande_intervention__equipement_id=equipement_id)
        return qs

# 4. DemandeIntervention (di)
@registerExporter('di')
class DemandeInterventionStrategy(BaseExportStrategy):
    model = DemandeIntervention
    
    def apply_filters(self, qs):
        equipement_id = self.params.get('equipementId')
        if equipement_id:
            qs = qs.filter(equipement_id=equipement_id)
        return qs

# 5. Consommable (conso)
@registerExporter('conso')
class ConsommableStrategy(BaseExportStrategy):
    model = Consommable

# 6. Historique Achat Consommable (PorterSur)
@registerExporter('historique_achat_conso')
class AchatConsommableStrategy(BaseExportStrategy):
    model = PorterSur
    
    def apply_filters(self, qs):
        conso_id = self.params.get('consoId')
        if conso_id:
            qs = qs.filter(consommable_id=conso_id)
        return qs

# 7. Stock (Stocker)
@registerExporter('stock')
class StockStrategy(BaseExportStrategy):
    model = Stocker
    
    def apply_filters(self, qs):
        magasin_id = self.params.get('magasinId')
        if magasin_id:
            qs = qs.filter(magasin_id=magasin_id)
        return qs

# 8. Magasins
@registerExporter('magasins')
class MagasinStrategy(BaseExportStrategy):
    model = Magasin

# 9. Historique Sortie Magasin (BonTravailConsommable)
@registerExporter('historique_sortie_magasin')
class SortieMagasinStrategy(BaseExportStrategy):
    model = BonTravailConsommable
    
    def apply_filters(self, qs):
        magasin_id = self.params.get('magasinId')
        if magasin_id:
            qs = qs.filter(magasin_reserve_id=magasin_id)
        return qs

# 10. Logs
@registerExporter('logs')
class LogStrategy(BaseExportStrategy):
    model = Log
    
    def apply_filters(self, qs):
        utilisateur_id = self.params.get('utilisateurId')
        if utilisateur_id:
            qs = qs.filter(utilisateur_id=utilisateur_id)
        return qs

# 11. Fournisseur
@registerExporter('fournisseur')
class FournisseurStrategy(BaseExportStrategy):
    model = Fournisseur

# 12. Fabricant
@registerExporter('fabricant')
class FabricantStrategy(BaseExportStrategy):
    model = Fabricant

# 13. Modele Equipement
@registerExporter('modele_equipement')
class ModeleEquipementStrategy(BaseExportStrategy):
    model = ModeleEquipement

# 14. Lieu
@registerExporter('lieu')
class LieuStrategy(BaseExportStrategy):
    model = Lieu

# 15. Compteur
@registerExporter('compteur')
class CompteurStrategy(BaseExportStrategy):
    model = Compteur
    
    def apply_filters(self, qs):
        equipement_id = self.params.get('equipementId')
        if equipement_id:
            qs = qs.filter(equipement_id=equipement_id)
        return qs

# 16. Maintenance Preventive (Seuils / Declencher)
@registerExporter('maintenance_preventive')
class SeuilStrategy(BaseExportStrategy):
    model = Declencher
    
    def apply_filters(self, qs):
        equipement_id = self.params.get('equipementId')
        if equipement_id:
            qs = qs.filter(compteur__equipement_id=equipement_id)
        return qs

# 17. Utilisateurs
@registerExporter('users')
class UtilisateurStrategy(BaseExportStrategy):
    model = Utilisateur

