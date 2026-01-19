import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL, MEDIA_BASE_URL } from '@/utils/constants';
import { EQUIPMENT_STATUS } from '@/utils/constants.js';

export function useEquipmentForm(isEditMode = false) {
  const router = useRouter();
  const store = useStore();
  const api = useApi(API_BASE_URL);

  const loading = ref(false);
  const loadingData = ref(false);
  const errorMessage = ref('');
  const successMessage = ref('');
  const editingCounterIndex = ref(-1);
  const isCounterEditMode = ref(false);

  const getCurrentUserId = () => {
    const currentUser = store.getters.currentUser;
    if (currentUser?.id) return currentUser.id;

    const userFromStorage = localStorage.getItem('user');
    if (userFromStorage) {
      try {
        const userData = JSON.parse(userFromStorage);
        return userData.id;
      } catch (e) {
        console.error('Error parsing user from localStorage:', e);
      }
    }

    console.error('Aucun utilisateur connecté trouvé');
    return null;
  };

  const formData = ref({
    numSerie: '',
    reference: '',
    designation: '',
    dateMiseEnService: '',
    prixAchat: null,
    lienImageEquipement: null,
    modeleEquipement: null,
    fournisseur: null,
    fabricant: null,
    famille: null,
    lieu: null,
    statut: null,
    consommables: [],
    compteurs: [],
    plansMaintenance : [],
    createurEquipement: getCurrentUserId()
  });

  

  const initialData = ref(null);

  const locations = ref([]);
  const equipmentModels = ref([]);
  const fournisseurs = ref([]);
  const fabricants = ref([]);
  const consumables = ref([]);
  const familles = ref([]);
  const typesPM = ref([]);
  const typesDocuments = ref([]);

  const showCounterDialog = ref(false);
  const showFabricantDialog = ref(false);
  const showFournisseurDialog = ref(false);
  const showModeleDialog = ref(false);
  const showFamilleDialog = ref(false);

  const existingPMs = ref([]);

  const equipmentStatuses = computed(() => {
    return Object.entries(EQUIPMENT_STATUS).map(([value, label]) => ({
      value,
      label
    }));
  });
  
  const getEmptyCounter = () => ({
    id: null,
    nom: '',
    valeurCourante: null,
    unite: 'heures',
    estPrincipal: false
  });
  const currentCounter = ref(getEmptyCounter());

  const getEmptyPlan = () => ({
    id: null,
    nom: '',
    type_id: null,
    description: '',
    compteurIndex: null,
    consommables: [],
    documents: [],
    necessiteHabilitationElectrique: false,
    necessitePermisFeu: false,
    seuil: {
      estGlissant: false,
      derniereIntervention: null,
      ecartInterventions: null,
      prochaineMaintenance: null
    }
  });
  const currentPlan = ref(getEmptyPlan());
  const isPlanEditMode = ref(false);
  const editingPlanIndex = ref(-1);
  const showPlanDialog = ref(false);

  const validateForm = () => {
    const requiredFields = ['numSerie', 'reference', 'designation', 'modeleEquipement', 'lieu', 'statut'];
    let isValid = true;

    requiredFields.forEach(field => {
      if (!formData.value[field]) {
        isValid = false;
      }
    });

    if (isEditMode) {
      const compteursSansId = formData.value.compteurs.filter(c => !c.id);
      if (compteursSansId.length > 0) {
        errorMessage.value = `Les compteurs suivants n'ont pas d'ID: ${compteursSansId.map(c => c.nom).join(', ')}`;
        isValid = false;
      }
    }

    return isValid;
  };

  const handleFileUpload = (file) => {
    formData.value.lienImageEquipement = file;
  };

  const fetchData = async () => {
    loadingData.value = true;
    errorMessage.value = '';

    try {
      const formDataApi = useApi(API_BASE_URL);
      await formDataApi.get('equipements/form-data/');
      const data = formDataApi.data.value;

      locations.value = data.locations;
      equipmentModels.value = data.equipmentModels;
      fournisseurs.value = data.fournisseurs;
      fabricants.value = data.fabricants;
      consumables.value = data.consumables;
      familles.value = data.familles;
      typesPM.value = data.typesPM;
      typesDocuments.value = data.typesDocuments;
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
      errorMessage.value = 'Erreur lors du chargement des données. Veuillez réessayer.';
    } finally {
      loadingData.value = false;
    }
  };

  const fetchEquipment = async (equipmentId) => {
    if (!equipmentId) return;

    try {
      loadingData.value = true;
      errorMessage.value = '';
      const res = await api.get(`equipement/${equipmentId}/affichage/`);
      const eq = res;

      // Formater la date de mise en service pour l'input type="date" (format YYYY-MM-DD)
      let formattedDate = '';
      if (eq.dateMiseEnService) {
        const date = new Date(eq.dateMiseEnService);
        if (!isNaN(date.getTime())) {
          formattedDate = date.toISOString().split('T')[0];
        }
      }

      const equipmentData = {
        numSerie: eq.numSerie || '',
        reference: eq.reference || '',
        designation: eq.designation || '',
        dateMiseEnService: formattedDate,
        prixAchat: eq.prixAchat || null,
        modeleEquipement: eq.modele?.id || null,
        fournisseur: eq.fournisseur?.id || null,
        fabricant: eq.fabricant?.id || null,
        famille: eq.famille?.id || null,
        lieu: eq.lieu?.id || eq.lieu || null,
        statut: eq.dernier_statut?.statut || null,
        consommables: eq.consommables?.map(c => c.id) || [],
        compteurs: eq.compteurs || []
      };

      initialData.value = JSON.parse(JSON.stringify(equipmentData));
      formData.value = equipmentData;
    } catch (e) {
      console.error("Erreur détaillée fetchEquipment:", e);
      console.error("Response:", e.response?.data);
      console.error("Status:", e.response?.status);
      errorMessage.value = "Erreur lors du chargement de l'équipement: " + (e.response?.data?.detail || e.message);
    } finally {
      loadingData.value = false;
    }
  };

  const fetchDocs = async () => {
    try {
      // Ne rien faire si pas de compteurs
      if (!formData.value.compteurs || formData.value.compteurs.length === 0) {
        return;
      }

      const fetchPromises = [];

      formData.value.compteurs.forEach(counter => {
        if (counter.planMaintenance && counter.planMaintenance.documents) {
          counter.planMaintenance.documents.forEach(doc => {
            if (doc.path) {
              const promise = fetch(MEDIA_BASE_URL + doc.path)
                .then(res => res.blob())
                .then(blob => {
                  const filename = doc.titre || 'document';
                  const file = new File([blob], filename, { type: blob.type });
                  doc.file = file;
                  return file;
                })
                .catch(err => {
                  console.error(`Erreur pour ${doc.path}:`, err);
                });

              fetchPromises.push(promise);
            }
          });
        }
      });

      await Promise.all(fetchPromises);
    } catch (error) {
      console.error('Erreur lors du chargement des documents:', error);
    }
  };

  const handleCounterAdd = () => {
    editingCounterIndex.value = -1;
    isCounterEditMode.value = false;
    currentCounter.value = getEmptyCounter();
    showCounterDialog.value = true;
  };

  const handleCounterEdit = (counter) => {
    editingCounterIndex.value = formData.value.compteurs.indexOf(counter);
    isCounterEditMode.value = true;

    currentCounter.value = {
      ...counter,
      planMaintenance: {
        ...counter.planMaintenance,
        consommables: counter.planMaintenance?.consommables
          ? counter.planMaintenance.consommables.map(c => ({ ...c }))
          : [],
        documents: counter.planMaintenance?.documents
          ? counter.planMaintenance.documents.map(d => ({ ...d }))
          : []
      }
    };

    showCounterDialog.value = true;
  };

  const handleCounterDelete = (counter) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer ce compteur ?')) {
      formData.value.compteurs = formData.value.compteurs.filter(c => c !== counter);
    }
  };

  const saveCurrentCounter = () => {
    if (editingCounterIndex.value >= 0) {
      // Mode édition
      formData.value.compteurs[editingCounterIndex.value] = { ...currentCounter.value };
    } else {
      // Mode ajout
      formData.value.compteurs.push({ ...currentCounter.value });
    }
    closeCounterDialog();
  };

  const handlePlanAdd = () => {
    editingPlanIndex.value = -1;
    isPlanEditMode.value = false;
    currentPlan.value = getEmptyPlan();
    if (formData.value.compteurs.length > 0) {
      currentPlan.value.compteurIndex = 0;
    }
    showPlanDialog.value = true;
  };

  const handlePlanEdit = (plan) => {
    editingPlanIndex.value = formData.value.plansMaintenance.indexOf(plan);
    isPlanEditMode.value = true;
    currentPlan.value = { 
      ...plan,
      seuil: { ...plan.seuil },
      consommables: [...plan.consommables]
    };
    showPlanDialog.value = true;
  };

  const handlePlanDelete = (plan) => {
    if (confirm('Êtes-vous sûr de vouloir supprimer ce plan de maintenance ?')) {
      formData.value.plansMaintenance = formData.value.plansMaintenance.filter(p => p !== plan);
    }
  };

  const savePlan = () => {
    if (editingPlanIndex.value >= 0) {
      formData.value.plansMaintenance[editingPlanIndex.value] = { ...currentPlan.value };
    } else {
      formData.value.plansMaintenance.push({ ...currentPlan.value });
    }
    closePlanDialog();
  };

  const closePlanDialog = () => {
    showPlanDialog.value = false;
    editingPlanIndex.value = -1;
    isPlanEditMode.value = false;
    currentPlan.value = getEmptyPlan();
  };

  const updateExistingPM = (counterToSave) => {
    const pmNom = counterToSave.planMaintenance.nom;
    if (!pmNom) return;

    const existingPMIndex = existingPMs.value.findIndex(pm => pm.nom === pmNom);

    if (existingPMIndex >= 0) {
      existingPMs.value[existingPMIndex] = {
        nom: pmNom,
        type: counterToSave.planMaintenance.type || null,
        consommables: [...counterToSave.planMaintenance.consommables],
        documents: [...counterToSave.planMaintenance.documents]
      };
    } else {
      existingPMs.value.push({
        nom: pmNom,
        type: counterToSave.planMaintenance.type || null,
        consommables: [...counterToSave.planMaintenance.consommables],
        documents: [...counterToSave.planMaintenance.documents]
      });
    }
  };

  const closeCounterDialog = () => {
    showCounterDialog.value = false;
    editingCounterIndex.value = -1;
    isCounterEditMode.value = false;
    currentCounter.value = getEmptyCounter();
    errorMessage.value = '';
  };

  const handleFabricantCreated = (newFabricant) => {
    fabricants.value.push(newFabricant);
    formData.value.fabricant = newFabricant.id;
  };

  const handleFournisseurCreated = (newFournisseur) => {
    fournisseurs.value.push(newFournisseur);
    formData.value.fournisseur = newFournisseur.id;
  };

  const handleModeleCreated = (newModele) => {
    equipmentModels.value.push(newModele);
    formData.value.modeleEquipement = newModele.id;
    formData.value.fabricant = newModele.fabricant;
  };

  const handleFamilleCreated = (newFamille) => {
    familles.value.push(newFamille);
    formData.value.famille = newFamille.id;
  };

  const handleLocationCreated = (newLocation) => {
    locations.value.push(newLocation);
    formData.value.lieu = newLocation.id;
  };

  const detectChanges = () => {
    if (!initialData.value || !formData.value) return { hasChanges: false, changes: {} };

    const changes = {};
    let hasChanges = false;

    const fieldsToCheck = [
      'numSerie', 'reference', 'designation', 'dateMiseEnService', 'prixAchat',
      'modeleEquipement', 'fournisseur', 'fabricant', 'famille', 'statut'
    ];

    for (let key of fieldsToCheck) {
      if (formData.value[key] !== initialData.value[key]) {
        changes[key] = {
          ancienne: initialData.value[key],
          nouvelle: formData.value[key]
        };
        hasChanges = true;
      }
    }

    if (formData.value.lienImageEquipement instanceof File) {
      changes.lienImageEquipement = { nouvelle: 'Nouvelle image' };
      hasChanges = true;
    }

    const currentLieu = typeof formData.value.lieu === 'object' ? formData.value.lieu?.id : formData.value.lieu;
    const initialLieu = typeof initialData.value.lieu === 'object' ? initialData.value.lieu?.id : initialData.value.lieu;

    if (currentLieu !== initialLieu) {
      changes.lieu = {
        ancienne: initialLieu,
        nouvelle: currentLieu
      };
      hasChanges = true;
    }

    const currentConsos = JSON.stringify([...(formData.value.consommables || [])].sort());
    const initialConsos = JSON.stringify([...(initialData.value.consommables || [])].sort());

    if (currentConsos !== initialConsos) {
      changes.consommables = {
        ancienne: initialData.value.consommables,
        nouvelle: formData.value.consommables
      };
      hasChanges = true;
    }

    const currentCompteurs = JSON.stringify(formData.value.compteurs);
    const initialCompteurs = JSON.stringify(initialData.value.compteurs);

    if (currentCompteurs !== initialCompteurs) {
      changes.compteurs = { message: 'Compteurs modifiés' };
      hasChanges = true;
    }

    return { hasChanges, changes };
  };

  return {
    // State
    formData,
    initialData,
    loading,
    loadingData,
    errorMessage,
    successMessage,
    
    // Data
    locations,
    equipmentModels,
    fournisseurs,
    fabricants,
    consumables,
    familles,
    typesPM,
    typesDocuments,
    equipmentStatuses,
    
    // Counter state
    currentCounter,
    editingCounterIndex,
    isCounterEditMode,
    existingPMs,
    
    // Plan state
    currentPlan,
    editingPlanIndex,
    isPlanEditMode,
    
    // Dialogs
    showCounterDialog,
    showPlanDialog,
    showFabricantDialog,
    showFournisseurDialog,
    showModeleDialog,
    showFamilleDialog,
    
    // Methods
    validateForm,
    handleFileUpload,
    fetchData,
    fetchEquipment,
    fetchDocs,
    detectChanges,
    
    // Counter methods
    getEmptyCounter,
    handleCounterAdd,
    handleCounterEdit,
    handleCounterDelete,
    saveCurrentCounter,
    closeCounterDialog,
    
    // Plan methods
    getEmptyPlan,
    handlePlanAdd,
    handlePlanEdit,
    handlePlanDelete,
    savePlan,
    closePlanDialog,
    
    // Dialog handlers
    handleFabricantCreated,
    handleFournisseurCreated,
    handleModeleCreated,
    handleFamilleCreated,
    handleLocationCreated,
    
    // Utilities
    api,
    router
  };
}
