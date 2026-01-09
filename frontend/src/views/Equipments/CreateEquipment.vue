<template>
  <v-app>
    <v-main>
      <v-container>
        <BaseForm 
          v-model="formData" 
          title="Créer un Équipement" 
          :loading="loading" 
          :error-message="errorMessage"
          :success-message="successMessage" 
          :loading-message="loadingData ? 'Chargement des données...' : ''"
          :validation-schema="validationSchema"
          submit-button-text="Créer un Équipement"
          :handleSubmit="handleSubmit" 
          actions-container-class="d-flex justify-end gap-2"
          :showActions="step === 6"
        >
          <template #default="{ formData, validation }">
            <v-stepper v-model="step" :steps="6" justify="center" alt-labels>
              <v-stepper-header class="justify-center">
                <v-stepper-item 
                  v-for="(label, index) in EQUIPMENT_CREATE_STEPS" 
                  :key="index" 
                  :value="index + 1"
                  :complete="step > index + 1" 
                  :editable="step > index + 1"
                >
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
                      <v-text-field 
                        v-model="formData.numSerie" 
                        label="Numéro de série*"
                        :rules="validation.getFieldRules('numSerie', 1)"
                      />
                    </v-col>

                    <v-col cols="12" md="6">
                      <v-text-field 
                        v-model="formData.reference" 
                        label="Référence*"
                        :rules="validation.getFieldRules('reference', 1)"
                      />
                    </v-col>

                    <v-col cols="12" md="6">
                      <v-text-field 
                        v-model="formData.designation" 
                        label="Désignation*"
                        :rules="validation.getFieldRules('designation', 1)"
                      />
                    </v-col>

                    <v-col cols="12" md="6">
                      <v-text-field 
                        v-model="formData.dateMiseEnService" 
                        type="date" 
                        label="Date de mise en service*"
                        :rules="validation.getFieldRules('dateMiseEnService', 1)"
                      />
                    </v-col>

                    <v-col cols="12" md="6">
                      <v-text-field 
                        v-model="formData.prixAchat" 
                        type="number" 
                        label="Prix d'achat*"
                        :rules="validation.getFieldRules('prixAchat', 1)"
                      />
                    </v-col>

                    <v-col cols="12" md="6">
                      <v-file-input 
                        label="Image de l'équipement" 
                        @change="handleFileUpload"
                      />
                    </v-col>
                  </v-row>
                </v-stepper-window-item>

                <!-- Étape 2: Fournisseur et Fabricant -->
                <v-stepper-window-item :value="2">
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-select 
                        v-model="formData.fournisseur" 
                        :items="fournisseurs" 
                        item-title="nom" 
                        item-value="id"
                        label="Fournisseur*"
                        :rules="validation.getFieldRules('fournisseur', 2)"
                      />
                    </v-col>

                    <v-col cols="12" md="6">
                      <v-select 
                        v-model="formData.fabricant" 
                        :items="fabricants" 
                        item-title="nom" 
                        item-value="id"
                        label="Fabricant*"
                        :rules="validation.getFieldRules('fabricant', 2)"
                      />
                    </v-col>

                    <v-col cols="12" md="6">
                      <v-select 
                        v-model="formData.famille" 
                        :items="familles" 
                        item-title="nom" 
                        item-value="id"
                        label="Famille*"
                        :rules="validation.getFieldRules('famille', 2)"
                      />
                    </v-col>

                    <v-col cols="12" md="6">
                      <v-select 
                        v-model="formData.modeleEquipement" 
                        :items="equipmentModels" 
                        item-title="nom"
                        item-value="id" 
                        label="Modèle*"
                        :rules="validation.getFieldRules('modeleEquipement', 2)"
                      />
                    </v-col>
                  </v-row>
                </v-stepper-window-item>

                <!-- Étape 3: Localisation -->
                <v-stepper-window-item :value="3">
                  <LocationTreeView :items="locations" v-model:selected="formData.lieu" />
                </v-stepper-window-item>

                <!-- Étape 4: Statut -->
                <v-stepper-window-item :value="4">
                  <v-select 
                    v-model="formData.statut" 
                    :items="equipmentStatuses" 
                    item-title="label" 
                    item-value="value"
                    label="Statut*"
                    :rules="validation.getFieldRules('statut', 4)"
                  />
                </v-stepper-window-item>

                <!-- Étape 5: Consommables -->
                <v-stepper-window-item :value="5">
                  <v-select 
                    v-model="formData.consommables" 
                    :items="consumables" 
                    item-title="designation"
                    item-value="id" 
                    multiple 
                    chips 
                    label="Consommables"
                  />
                </v-stepper-window-item>

                <!-- Étape 6: Compteurs -->
                <v-stepper-window-item :value="6">
                  <v-row class="my-2" align="center" justify="space-between">
                    <v-col cols="12" md="8">
                      <h3 class="mb-3">Compteurs Associés</h3>
                    </v-col>

                    <v-col cols="12" md="4" class="text-end">
                      <v-btn color="primary" class="my-1" @click="handleCounterAdd">
                        Ajouter un Compteur
                      </v-btn>
                    </v-col>
                  </v-row>

                  <v-data-table :items="formData.compteurs" :headers="counterTableHeaders" class="elevation-1">
                    <template #item.nom="{ item }">
                      {{ item.nom }}
                    </template>
                    <template #item.intervalle="{ item }">
                      {{ item.intervalle }}
                    </template>
                    <template #item.unite="{ item }">
                      {{ item.unite }}
                    </template>
                    <template #item.options="{ item }">
                      <div>
                        {{ item.estGlissant && item.estPrincipal ? 'Glissant et Principal' :
                          item.estGlissant ? 'Glissant' :
                            item.estPrincipal ? 'Principal' :
                              'Aucune' }}
                      </div>
                    </template>
                    <template #item.planMaintenance="{ item }">
                      <div>
                        <v-icon left small>mdi-wrench</v-icon>
                        {{ item.planMaintenance?.nom?.slice(0, 20) || 'Aucun plan associé' }}
                      </div>
                    </template>
                    <template #item.actions="{ item }">
                      <v-btn icon small color="primary" @click="handleCounterEdit(item)">
                        <v-icon>mdi-pencil</v-icon>
                      </v-btn>
                      <v-btn icon small color="red" @click="handleCounterDelete(item)">
                        <v-icon>mdi-delete</v-icon>
                      </v-btn>
                    </template>
                  </v-data-table>
                </v-stepper-window-item>

                <!-- Navigation -->
                <v-row justify="space-between" class="mt-4">
                  <v-btn variant="text" @click="prevStep" :disabled="step === 1">
                    Précédent
                  </v-btn>

                  <v-btn 
                    variant="text" 
                    color="primary" 
                    v-if="step < 6" 
                    @click="nextStep"
                    :disabled="!canGoToNextStep(validation)"
                  >
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
      <CounterForm v-model="currentCounter" :existingPMs="existingPMs" :typesPM="typesPM" :consumables="consumables"
        :typesDocuments="typesDocuments" :isEditMode="isEditMode" @save="saveCurrentCounter"
        @close="closeCounterDialog" />
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
import { BaseForm } from '@/components/common';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL, EQUIPMENT_CREATE_STEPS } from '@/utils/constants';
import LocationTreeView from '@/components/LocationTreeView.vue';
import { EQUIPMENT_STATUS } from '@/utils/constants.js';
import CounterForm from './Counters/CounterForm';
import FabricantForm from '@/components/Forms/FabricantForm.vue';
import FournisseurForm from '@/components/Forms/FournisseurForm.vue';
import ModeleEquipementForm from '@/components/Forms/ModeleEquipementForm.vue';
import FamilleEquipementForm from '@/components/Forms/FamilleEquipementForm.vue';

const router = useRouter();
const api = useApi(API_BASE_URL);

const loading = ref(false);
const loadingData = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const isEditMode = ref(false);
const editingCounterIndex = ref(-1);
const step = ref(1);

// Schéma de validation
const validationSchema = {
  step1: {
    numSerie: ['required', { name: 'minLength', params: [3] }],
    reference: ['required'],
    designation: ['required'],
    dateMiseEnService: ['required', 'date'],
    prixAchat: ['required', 'numeric', 'positive'],
  },
  step2: {
    fournisseur: ['required'],
    fabricant: ['required'],
    famille: ['required'],
    modeleEquipement: ['required'],
  },
  step3: {
    lieu: ['required'],
  },
  step4: {
    statut: ['required'],
  },
  step5: {
    // Consommables optionnels
  },
  step6: {
    // Validation personnalisée pour les compteurs
  }
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
  createurEquipement: 3
});



const locations = ref([]);
const equipmentModels = ref([]);
const fournisseurs = ref([]);
const fabricants = ref([]);
const consumables = ref([]);
const familles = ref([]);
const typesPM = ref([]);
const typesDocuments = ref([]);

// Modales
const showCounterDialog = ref(false);
const showFabricantDialog = ref(false);
const showFournisseurDialog = ref(false);
const showModeleDialog = ref(false);
const showFamilleDialog = ref(false);

const existingPMs = ref([
  { nom: 'Plan de maintenance vidange', consommables: [{ consommable: 1, quantite: 1 }, { consommable: 2, quantite: 2 }], documents: [], type: 2 },
  { nom: 'Plan de maintenance révision', consommables: [], documents: [], type: 3 },
  { nom: 'Plan de maintenance complet', consommables: [], documents: [], type: 2 }
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
    const locationsApi = useApi(API_BASE_URL);
    const modelsApi = useApi(API_BASE_URL);
    const fournisseurApi = useApi(API_BASE_URL);
    const fabricantApi = useApi(API_BASE_URL);
    const consumablesApi = useApi(API_BASE_URL);
    const famillesApi = useApi(API_BASE_URL);
    const typesPMApi = useApi(API_BASE_URL);
    const typesDocumentsApi = useApi(API_BASE_URL);

    await Promise.all([
      locationsApi.get('lieux-hierarchy/'),
      modelsApi.get('modele-equipements/'),
      fabricantApi.get('fabricants/'),
      fournisseurApi.get('fournisseurs/'),
      consumablesApi.get('consommables/'),
      famillesApi.get('famille-equipements/'),
      typesPMApi.get('types-plan-maintenance/'),
      typesDocumentsApi.get('types-documents/')
    ]);

    locations.value = locationsApi.data.value;
    equipmentModels.value = modelsApi.data.value;
    fournisseurs.value = fournisseurApi.data.value;
    fabricants.value = fabricantApi.data.value;
    consumables.value = consumablesApi.data.value;
    familles.value = famillesApi.data.value;
    typesPM.value = typesPMApi.data.value;
    typesDocuments.value = typesDocumentsApi.data.value;

  } catch (error) {
    console.error('Erreur lors du chargement des données:', error);
    errorMessage.value = 'Erreur lors du chargement des données. Veuillez réessayer.';
  } finally {
    loadingData.value = false;
  }
};

const handleSubmit = async () => {
  if (!validateForm()) return;

  loading.value = true;
  errorMessage.value = '';

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
    errorMessage.value = 'Erreur lors de la création de l\'équipement';

    if (e.response?.data) {
      const errors = Object.entries(e.response.data)
        .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
        .join('\n');
      errorMessage.value += `\n${errors}`;
    }
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
  showCounterDialog.value = true;
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

  showCounterDialog.value = true;
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

  // Fermer la dialog après la sauvegarde
  closeCounterDialog();
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
const openFabricantDialog = () => {
  showFabricantDialog.value = true
}

const closeFabricantDialog = () => {
  showFabricantDialog.value = false
}

const handleFabricantCreated = (newFabricant) => {
  fabricants.value.push(newFabricant)
  formData.value.fabricant = newFabricant.id
}

// Fournisseur
const openFournisseurDialog = () => {
  showFournisseurDialog.value = true
}

const closeFournisseurDialog = () => {
  showFournisseurDialog.value = false
}

const handleFournisseurCreated = (newFournisseur) => {
  fournisseurs.value.push(newFournisseur)
  formData.value.fournisseur = newFournisseur.id
}

// Modèle Equipement
const openModeleDialog = () => {
  showModeleDialog.value = true;
};

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
const openFamilleDialog = () => {
  showFamilleDialog.value = true;
};

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
  if (step.value < 6) step.value++;
};

const prevStep = () => {
  if (step.value > 1) step.value--;
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

.rotate-icon {
  transform: rotate(90deg);
  transition: transform 0.2s;
}

.tree-icon-placeholder {
  display: inline-block;
  width: 24px;
}

.location-tree {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 8px;
}
</style>