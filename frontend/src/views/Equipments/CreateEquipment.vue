<template>
  <v-app>
    <v-main>
      <v-container>
        <BaseForm v-model="formData" title="Créer un Équipement" :loading="loading" :error-message="errorMessage"
          :success-message="successMessage" :loading-message="loadingData ? 'Chargement des données...' : ''"
          :validation-schema="validationSchema" submit-button-text="Créer un Équipement" :handleSubmit="handleSubmit"
          actions-container-class="d-flex justify-end gap-2" :showActions="step === 6">
          <template #default="{ formData, validation }">
            <v-stepper v-model="step" :steps="6" justify="center" alt-labels>
              <v-stepper-header class="justify-center">
                <v-stepper-item v-for="(label, index) in EQUIPMENT_CREATE_STEPS" :key="index" :value="index + 1"
                  :complete="isStepComplete(index + 1)" :editable="isStepEditable(index + 1)"
                  :color="isStepEditable(index + 1) ? 'primary' : undefined" @click="goToStep(index + 1)">
                  <template #title>
                    <span class="step-label">{{ label }}</span>
                  </template>
                </v-stepper-item>
              </v-stepper-header>

              <v-stepper-window v-model="step" :steps="6" class="mb-4">
                <!-- Étape 1: Informations générales -->
                <v-stepper-window-item :value="1">
                  <v-row>
                    <v-col cols="12" md="6">
                      <FormField v-model="formData.numSerie" field-name="numSerie" :step="1" label="Numéro de série"
                        placeholder="Saisir le numéro de série" counter="100" />
                    </v-col>

                    <v-col cols="12" md="6">
                      <FormField v-model="formData.reference" field-name="reference" :step="1" label="Référence"
                        placeholder="Saisir la référence" counter="100" />
                    </v-col>

                    <v-col cols="12" md="6">
                      <FormField v-model="formData.designation" field-name="designation" :step="1" label="Désignation"
                        placeholder="Saisir la désignation" counter="100" />
                    </v-col>

                    <v-col cols="12" md="6">
                      <FormField v-model="formData.dateMiseEnService" field-name="dateMiseEnService" :step="1"
                        label="Date de mise en service" type="date" />
                    </v-col>

                    <v-col cols="12" md="6">
                      <FormField v-model="formData.prixAchat" field-name="prixAchat" :step="1" label="Prix d'achat"
                        type="number" placeholder="0.00" suffix="€" step="0.01" min="0" />
                    </v-col>

                    <v-col cols="12" md="6">
                      <label class="field-label">Image de l'équipement</label>
                      <v-file-input placeholder="Sélectionner une image" @change="handleFileUpload" accept="image/*"
                        variant="outlined" density="comfortable" prepend-icon="" prepend-inner-icon="mdi-camera"
                        hide-details="auto" />
                    </v-col>
                  </v-row>
                </v-stepper-window-item>

                <!-- Étape 2: Fournisseur et Fabricant -->
                <v-stepper-window-item :value="2">
                  <v-row>
                    <v-col cols="12" md="6">
                      <FormSelect v-model="formData.fournisseur" field-name="fournisseur" :step="2" label="Fournisseur"
                        :items="fournisseurs" item-title="nom" item-value="id" clearable />
                    </v-col>

                    <v-col cols="12" md="6">
                      <FormSelect v-model="formData.fabricant" field-name="fabricant" :step="2" label="Fabricant"
                        :items="fabricants" item-title="nom" item-value="id" clearable />
                    </v-col>

                    <v-col cols="12" md="6">
                      <FormSelect v-model="formData.famille" field-name="famille" :step="2" label="Famille"
                        :items="familles" item-title="nom" item-value="id" clearable />
                    </v-col>

                    <v-col cols="12" md="6">
                      <FormSelect v-model="formData.modeleEquipement" field-name="modeleEquipement" :step="2"
                        label="Modèle" :items="equipmentModels" item-title="nom" item-value="id" clearable />
                    </v-col>
                  </v-row>
                </v-stepper-window-item>

                <!-- Étape 3: Localisation -->
                <v-stepper-window-item :value="3">
                  <LocationTreeView :items="locations" v-model:selected="formData.lieu" />
                </v-stepper-window-item>

                <!-- Étape 4: Statut -->
                <v-stepper-window-item :value="4">
                  <FormSelect v-model="formData.statut" field-name="statut" :step="4" label="Statut"
                    :items="equipmentStatuses" item-title="label" item-value="value" />
                </v-stepper-window-item>

                <!-- Étape 5: Consommables -->
                <v-stepper-window-item :value="5">
                  <v-select v-model="formData.consommables" :items="consumables" item-title="designation"
                    item-value="id" multiple chips label="Consommables" />
                </v-stepper-window-item>

                <!-- Étape 6: Compteurs -->
                <v-stepper-window-item :value="6">
                  <!-- Liste des compteurs déjà ajoutés -->
                  <v-sheet v-if="formData.compteurs.length > 0 && !showCounterForm" class="pa-4 mb-4" elevation="2" rounded>
                    <h4 class="mb-3">Compteurs ajoutés ({{ formData.compteurs.length }})</h4>
                    
                    <v-list dense>
                      <v-list-item v-for="(compteur, index) in formData.compteurs" :key="index" class="mb-2 pa-3"
                        elevation="1" rounded>
                        <template #prepend>
                          <v-icon color="primary">mdi-counter</v-icon>
                        </template>

                        <v-list-item-title class="font-weight-medium">
                          {{ compteur.nom }}
                        </v-list-item-title>

                        <v-list-item-subtitle>
                          Intervalle: {{ compteur.intervalle }} {{ compteur.unite }} | 
                          Plan: {{ compteur.planMaintenance?.nom || 'Aucun' }}
                          <v-chip v-if="compteur.estPrincipal" size="x-small" color="primary" class="ml-2">Principal</v-chip>
                          <v-chip v-if="compteur.estGlissant" size="x-small" color="info" class="ml-1">Glissant</v-chip>
                        </v-list-item-subtitle>

                        <template #append>
                          <v-btn icon="mdi-pencil" size="small" variant="text" color="primary"
                            @click="handleCounterEdit(compteur)" />
                          <v-btn icon="mdi-delete" size="small" variant="text" color="error"
                            @click="handleCounterDelete(compteur)" />
                        </template>
                      </v-list-item>
                    </v-list>

                    <v-divider class="my-4" />
                    
                    <!-- Boutons d'action -->
                    <v-row class="mt-4" justify="center">
                      <v-btn color="primary" size="large" @click="handleCounterAdd" class="mr-2">
                        <v-icon left>mdi-plus</v-icon>
                        Ajouter un autre compteur
                      </v-btn>
                    </v-row>
                  </v-sheet>

                  <!-- Formulaire pour ajouter/éditer un compteur -->
                  <CounterInlineForm 
                    v-if="showCounterForm" 
                    v-model="currentCounter" 
                    :existingPMs="existingPMs" 
                    :typesPM="typesPM" 
                    :consumables="consumables"
                    :typesDocuments="typesDocuments" 
                    :isEditMode="isEditMode"
                    :isFirstCounter="formData.compteurs.length === 0"
                    @save="saveCurrentCounter"
                    @cancel="cancelCounterForm" 
                  />
                </v-stepper-window-item>

                <!-- Navigation -->
                <v-row justify="space-between" class="mt-4">
                  <v-btn type="button" variant="text" @click="prevStep" :disabled="step === 1">
                    Précédent
                  </v-btn>

                  <v-btn type="button" variant="text" color="primary" v-if="step < 6" @click="nextStep"
                    :disabled="!canGoToNextStep(validation)">
                    Suivant
                  </v-btn>
                </v-row>
              </v-stepper-window>
            </v-stepper>
          </template>
        </BaseForm>
      </v-container>
    </v-main>

    <v-dialog v-model="showCounterDialog" max-width="1000px" @click:outside="closeCounterDialog">
      <v-card>
        <v-card-title>
          {{ isEditMode ? 'Modifier un compteur' : 'Ajouter un compteur' }}
        </v-card-title>
        <v-card-text>
          <CounterInlineForm v-model="currentCounter" :existingPMs="existingPMs" :typesPM="typesPM" :consumables="consumables"
            :typesDocuments="typesDocuments" @save="saveCurrentCounter" @cancel="closeCounterDialog" />
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showFabricantDialog" max-width="80%">
      <FabricantForm @created="handleFabricantCreated" @close="closeFabricantDialog" />
    </v-dialog>

    <v-dialog v-model="showFournisseurDialog" max-width="80%">
      <FournisseurForm @created="handleFournisseurCreated" @close="closeFournisseurDialog" />
    </v-dialog>

    <v-dialog v-model="showModeleDialog" max-width="80%">
      <ModeleEquipementForm :fabricants="fabricants" @created="handleModeleCreated" @close="closeModeleDialog"
        @fabricant-created="handleFabricantCreated" />
    </v-dialog>

    <v-dialog v-model="showFamilleDialog" max-width="50%">
      <FamilleEquipementForm :families="familles" @created="handleFamilleCreated" @close="closeFamilleDialog" />
    </v-dialog>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { BaseForm, FormField, FormSelect } from '@/components/common';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL, EQUIPMENT_CREATE_STEPS } from '@/utils/constants';
import LocationTreeView from '@/components/LocationTreeView.vue';
import { EQUIPMENT_STATUS } from '@/utils/constants.js';
import CounterInlineForm from '@/components/Forms/CounterInlineForm.vue';
import FabricantForm from '@/components/Forms/FabricantForm.vue';
import FournisseurForm from '@/components/Forms/FournisseurForm.vue';
import ModeleEquipementForm from '@/components/Forms/ModeleEquipementForm.vue';
import FamilleEquipementForm from '@/components/Forms/FamilleEquipementForm.vue';

const router = useRouter();
const store = useStore();
const api = useApi(API_BASE_URL);

const loading = ref(false);
const loadingData = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const isEditMode = ref(false);
const editingCounterIndex = ref(-1);
const step = ref(1);
const visitedSteps = ref([1]);

const validationSchema = {
  step1: {
    numSerie: [{ name: 'minLength', params: [1] }, { name: 'maxLength', params: [100] }],
    designation: ['required', { name: 'maxLength', params: [100] }],
    reference: [{ name: 'maxLength', params: [100] }],
    dateMiseEnService: [],
    prixAchat: ['numeric', 'positive'],
  },
  step2: {

    modeleEquipement: ['required'],
    fournisseur: ['required'],
    fabricant: ['required'],
    famille: ['required'],
  },
  step3: {
    lieu: ['required'],
  },
  step4: {
    statut: ['required'],
  },
  step5: {
  },
  step6: {
  }
};

// Récupérer l'ID de l'utilisateur connecté
const getCurrentUserId = () => {
  const currentUser = store.getters.currentUser;
  console.log('Current user from store:', currentUser);

  if (currentUser && currentUser.id) {
    console.log('Using user ID from store:', currentUser.id);
    return currentUser.id;
  }

  // Fallback: lire depuis localStorage
  const userFromStorage = localStorage.getItem('user');
  if (userFromStorage) {
    try {
      const userData = JSON.parse(userFromStorage);
      console.log('User data from localStorage:', userData);
      console.log('Using user ID from localStorage:', userData.id);
      return userData.id;
    } catch (e) {
      console.error('Error parsing user from localStorage:', e);
    }
  }

  console.error('Aucun utilisateur connecté trouvé');
  return null;
};

let formData = ref({
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
  createurEquipement: getCurrentUserId()
});



const locations = ref([]);
const equipmentModels = ref([]);
const fournisseurs = ref([]);
const fabricants = ref([]);
const consumables = ref([]);
const familles = ref([]);
const typesPM = ref([]);
const typesDocuments = ref([]);

// Modales et formulaires inline
const showCounterDialog = ref(false);
const showCounterForm = ref(true); // true par défaut pour afficher le formulaire au premier chargement
const showFabricantDialog = ref(false);
const showFournisseurDialog = ref(false);
const showModeleDialog = ref(false);
const showFamilleDialog = ref(false);

const existingPMs = ref([
]);

const equipmentStatuses = computed(() => {
  return Object.entries(EQUIPMENT_STATUS).map(([value, label]) => ({
    value,
    label
  }));
});

const getEmptyCounter = () => ({
  nom: '',
  description: '',
  intervalle: '',
  unite: '',
  valeurCourante: null,
  derniereIntervention: null,
  estGlissant: false,
  estPrincipal: false,
  habElec: false,
  permisFeu: false,
  planMaintenance: {
    nom: '',
    type: null,
    consommables: [],
    documents: []
  }
});

const currentCounter = ref(getEmptyCounter());

const handleFileUpload = (event) => {
  const file = event.target.files ? event.target.files[0] : event;
  if (file) {
    formData.value.lienImageEquipement = file;
  }
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

const handleSubmit = async () => {
  // Validation basique : au moins un compteur requis
  if (formData.value.compteurs.length === 0) {
    errorMessage.value = 'Au moins un compteur est requis';
    step.value = 6;  // Rediriger vers l'étape des compteurs
    return;
  }

  // Validation des compteurs
  const invalidCounters = formData.value.compteurs.filter(c =>
    !c.nom || !c.unite || c.intervalle === null || c.intervalle === undefined || c.intervalle <= 0
  );

  if (invalidCounters.length > 0) {
    errorMessage.value = 'Tous les compteurs doivent avoir un nom, une unité et un intervalle positif';
    step.value = 6;
    return;
  }

  // Validation que le statut est défini
  if (!formData.value.statut) {
    errorMessage.value = 'Le statut de l\'équipement est requis';
    step.value = 4;
    return;
  }

  loading.value = true;
  errorMessage.value = '';

  console.log('FormData avant envoi:', formData.value);
  console.log('createurEquipement ID:', formData.value.createurEquipement);

  try {
    const fd = new FormData();

    // Ajouter les champs simples
    for (const key in formData.value) {
      if (key === 'lieu') {
        fd.append('lieu', formData.value.lieu?.id ?? '');
      } else if (key === 'consommables') {
        fd.append(key, JSON.stringify(formData.value[key]));
      } else if (key === 'compteurs') {
        const compteursData = formData.value.compteurs.map(c => ({
          ...c,
          // S'assurer que les valeurs numériques ne sont pas null
          valeurCourante: c.valeurCourante ?? 0,
          derniereIntervention: c.derniereIntervention ?? 0,
          intervalle: c.intervalle ?? 0,
          planMaintenance: {
            ...c.planMaintenance,
            documents: c.planMaintenance.documents.map(d => ({
              titre: d.titre,
              type: d.type
            }))
          }
        }));
        fd.append(key, JSON.stringify(compteursData));
      } else if (key === 'lienImageEquipement') {
        if (formData.value[key] instanceof File) {
          fd.append('lienImageEquipement', formData.value[key]);
        }
      } else if (formData.value[key] !== null && formData.value[key] !== undefined) {
        fd.append(key, formData.value[key]);
      }
    }

    // Ajouter les fichiers des documents des plans de maintenance
    formData.value.compteurs.forEach((compteur, compteurIndex) => {
      compteur.planMaintenance.documents.forEach((doc, docIndex) => {
        if (doc.file instanceof File) {
          const fileKey = `compteur_${compteurIndex}_document_${docIndex}`;
          fd.append(fileKey, doc.file);
        }
      });
    });

    await api.post('equipements/', fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    successMessage.value = 'Équipement créé avec succès';

    setTimeout(() => router.back(), 1500);

  } catch (e) {
    console.error('Erreur lors de la création:', e);
    console.error('Détails de l\'erreur:', e.response?.data);
    errorMessage.value = 'L\'équipement n\'a pas pu être créé. Veuillez vérifier les informations saisies.';
  } finally {
    loading.value = false;
  }
};

const counterTableHeaders = [
  { title: 'Nom du compteur', value: 'nom' },
  { title: 'Intervalle de maintenance', value: 'intervalle' },
  { title: 'Unité', value: 'unite' },
  { title: 'Valeur actuelle', value: 'valeurCourante' },
  { title: 'Dernière intervention', value: 'derniereIntervention' },
  { title: 'Plan de maintenance', value: 'planMaintenance' },
  { title: 'Options', value: 'options', sortable: false },
  { title: 'Actions', value: 'actions', sortable: false }
];

const handleCounterAdd = () => {
  editingCounterIndex.value = -1;
  isEditMode.value = false;
  currentCounter.value = getEmptyCounter();
  showCounterForm.value = true;
};

const handleCounterEdit = (counter) => {
  editingCounterIndex.value = formData.value.compteurs.indexOf(counter);
  isEditMode.value = true;

  console.log("Compteur à modifier: ", counter);

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

  showCounterForm.value = true;
};

const handleCounterDelete = (counter) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer ce compteur ?')) {
    formData.value.compteurs = formData.value.compteurs.filter(c => c !== counter);
  }
};

const saveCurrentCounter = () => {
  // Validation déléguée au CounterForm, on suppose que les données sont valides ici

  const counterToSave = {
    ...currentCounter.value,
    planMaintenance: {
      ...currentCounter.value.planMaintenance,
      consommables: currentCounter.value.planMaintenance.consommables
        .filter(c => c.consommable)
        .map(c => ({ ...c })),
      documents: currentCounter.value.planMaintenance.documents
        .filter(d => d.titre || d.file)
        .map(d => ({
          titre: d.titre,
          type: d.type,
          file: d.file
        }))
    }
  };

  if (editingCounterIndex.value >= 0) {
    // Modification
    formData.value.compteurs[editingCounterIndex.value] = counterToSave;
    updateExistingPM(counterToSave);
  } else {
    // Ajout
    formData.value.compteurs.push(counterToSave);

    if (counterToSave.planMaintenance.nom &&
      !existingPMs.value.some(pm => pm.nom === counterToSave.planMaintenance.nom)) {
      existingPMs.value.push({
        nom: counterToSave.planMaintenance.nom,
        type: counterToSave.planMaintenance.type,
        consommables: [...counterToSave.planMaintenance.consommables],
        documents: [...counterToSave.planMaintenance.documents]
      });
    }
  }

  // Fermer le formulaire inline après la sauvegarde
  showCounterForm.value = false;
  isEditMode.value = false;
  editingCounterIndex.value = -1;
  currentCounter.value = getEmptyCounter();
};

const cancelCounterForm = () => {
  // Ne permettre l'annulation que s'il y a déjà au moins un compteur
  if (formData.value.compteurs.length > 0) {
    showCounterForm.value = false;
    isEditMode.value = false;
    editingCounterIndex.value = -1;
    currentCounter.value = getEmptyCounter();
  }
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

// -------------------------------
// Modales Fabricant, Fournisseur, Modele, Famille Equipement
// -------------------------------
// Fabricant
const closeFabricantDialog = () => {
  showFabricantDialog.value = false
}

const handleFabricantCreated = (newFabricant) => {
  fabricants.value.push(newFabricant)
  formData.value.fabricant = newFabricant.id
}

// Fournisseur
const closeFournisseurDialog = () => {
  showFournisseurDialog.value = false
}

const handleFournisseurCreated = (newFournisseur) => {
  fournisseurs.value.push(newFournisseur)
  formData.value.fournisseur = newFournisseur.id
}

// Modèle Equipement
const closeModeleDialog = () => {
  showModeleDialog.value = false;
};

const handleModeleCreated = (newModele) => {
  console.log(JSON.stringify(newModele));
  equipmentModels.value.push(newModele);
  formData.value.modeleEquipement = newModele.id;
  formData.value.fabricant = newModele.fabricant;
};

// Famille Equipement
const closeFamilleDialog = () => {
  showFamilleDialog.value = false;
};

const handleFamilleCreated = (newFamille) => {
  console.log('Nouvelle famille créée:', newFamille);
  familles.value.push(newFamille);
  formData.value.famille = newFamille.id;
};

const closeCounterDialog = () => {
  showCounterDialog.value = false;
  editingCounterIndex.value = -1;
  isEditMode.value = false;
  currentCounter.value = getEmptyCounter();
  errorMessage.value = '';
};

// Navigation entre les steps
const nextStep = () => {
  if (step.value < 6) {
    const nextStepValue = step.value + 1;
    step.value = nextStepValue;
    // Ajouter la nouvelle étape aux étapes visitées
    if (!visitedSteps.value.includes(nextStepValue)) {
      visitedSteps.value.push(nextStepValue);
    }
  }
};

const prevStep = () => {
  if (step.value > 1) step.value--;
};

const goToStep = (targetStep) => {
  // Permet de naviguer vers n'importe quelle étape déjà visitée
  if (isStepEditable(targetStep)) {
    step.value = targetStep;
  }
};

const isStepComplete = (stepNumber) => {
  // Une étape est complète si on est passé au-delà
  return visitedSteps.value.includes(stepNumber) && step.value > stepNumber;
};

const isStepEditable = (stepNumber) => {
  // Une étape est éditable si elle a déjà été visitée
  return visitedSteps.value.includes(stepNumber);
};

const canGoToNextStep = (validation) => {
  if (!validation) return true;
  return validation.isStepValid(step.value, formData.value);
};

onMounted(async () => {
  await fetchData()
});
</script>

<style scoped>
.step-label {
  font-size: 0.875rem;
  font-weight: 500;
}

.field-label {
  display: block;
  margin-bottom: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.87);
}

:deep(.v-stepper-item--editable) {
  cursor: pointer;
}

:deep(.v-stepper-item--editable .v-stepper-item__avatar) {
  background-color: rgb(var(--v-theme-primary)) !important;
  color: white !important;
}

:deep(.v-stepper-item--complete .v-stepper-item__avatar) {
  background-color: rgb(var(--v-theme-primary)) !important;
}

:deep(.v-stepper-item--editable .step-label) {
  color: rgb(var(--v-theme-primary));
  font-weight: 600;
}
</style>