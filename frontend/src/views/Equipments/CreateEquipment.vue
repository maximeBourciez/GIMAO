<template>
  <v-app>
    <v-main>
      <v-container>
        <BaseForm v-model="formData" title="Créer un Équipement" :loading="loading" :error-message="errorMessage"
          :success-message="successMessage" :loading-message="loadingData ? 'Chargement des données...' : ''"
          :validation-schema="validationSchema" submit-button-text="Créer un Équipement" :handleSubmit="handleSubmit"
          actions-container-class="d-flex justify-end gap-2 mt-3" submit-button-class="mt-3"
          cancel-button-class="mt-3 mr-3" :showActions="step === 6">
          <template #default="{ validation }">
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

              <v-stepper-window v-model="step" :steps="6" class="mb-8">
                <!-- Étape 1: Informations générales -->
                <v-stepper-window-item :value="1">
                  <EquipmentFormFields v-model="formData" :equipment-models="equipmentModels"
                    :fournisseurs="fournisseurs" :fabricants="fabricants" :familles="familles" :locations="locations"
                    :consumables="consumables" :equipment-statuses="equipmentStatuses" :step="1" :show-location="false"
                    :show-status="false" :show-consommables="false" :show-counters="false" :show-general="true"
                    :show-model-info="false" @file-upload="handleFileUpload"
                    @location-created="handleLocationCreated" 
                    @open-modele-dialog="showModeleDialog = true"
                    @open-fournisseur-dialog="showFournisseurDialog = true"
                    @open-fabricant-dialog="showFabricantDialog = true"
                    @open-famille-dialog="showFamilleDialog = true"
                    @open-lieu-dialog="handleOpenLieuDialog" />
                </v-stepper-window-item>

                <!-- Étape 2: Fournisseur et Fabricant -->
                <v-stepper-window-item :value="2">
                  <EquipmentFormFields v-model="formData" :equipment-models="equipmentModels"
                    :fournisseurs="fournisseurs" :fabricants="fabricants" :familles="familles" :locations="locations"
                    :consumables="consumables" :equipment-statuses="equipmentStatuses" :step="2" :show-location="false"
                    :show-status="false" :show-consommables="false" :show-counters="false" :show-general="false"
                    :show-model-info="true" @file-upload="handleFileUpload" @location-created="handleLocationCreated" 
                    @open-modele-dialog="showModeleDialog = true"
                    @open-fournisseur-dialog="showFournisseurDialog = true"
                    @open-fabricant-dialog="showFabricantDialog = true"
                    @open-famille-dialog="showFamilleDialog = true"
                    @open-lieu-dialog="handleOpenLieuDialog" />
                </v-stepper-window-item>

                <!-- Étape 3: Localisation -->
                <v-stepper-window-item :value="3">
                  <EquipmentFormFields v-model="formData" :equipment-models="equipmentModels"
                    :fournisseurs="fournisseurs" :fabricants="fabricants" :familles="familles" :locations="locations"
                    :consumables="consumables" :equipment-statuses="equipmentStatuses" :step="3" :show-status="false"
                    :show-consommables="false" :show-counters="false" :show-general="false" :show-model-info="false"
                    @file-upload="handleFileUpload" @location-created="handleLocationCreated" 
                    @open-modele-dialog="showModeleDialog = true"
                    @open-fournisseur-dialog="showFournisseurDialog = true"
                    @open-fabricant-dialog="showFabricantDialog = true"
                    @open-famille-dialog="showFamilleDialog = true"
                    @open-lieu-dialog="handleOpenLieuDialog" />
                </v-stepper-window-item>

                <!-- Étape 4: Statut -->
                <v-stepper-window-item :value="4">
                  <EquipmentFormFields v-model="formData" :equipment-models="equipmentModels"
                    :fournisseurs="fournisseurs" :fabricants="fabricants" :familles="familles" :locations="locations"
                    :consumables="consumables" :equipment-statuses="equipmentStatuses" :step="4" :show-location="false"
                    :show-consommables="false" :show-counters="false" :show-general="false" :show-model-info="false"
                    @file-upload="handleFileUpload" @location-created="handleLocationCreated" 
                    @open-modele-dialog="showModeleDialog = true"
                    @open-fournisseur-dialog="showFournisseurDialog = true"
                    @open-fabricant-dialog="showFabricantDialog = true"
                    @open-famille-dialog="showFamilleDialog = true"
                    @open-lieu-dialog="handleOpenLieuDialog" />
                </v-stepper-window-item>

                <!-- Étape 5: Consommables -->
                <v-stepper-window-item :value="5">
                  <v-select v-model="formData.consommables" :items="consumables" item-title="designation"
                    item-value="id" multiple chips label="Consommables" />
                </v-stepper-window-item>

                <!-- Étape 6: Compteurs -->
                <v-stepper-window-item :value="6">
                  <!-- Liste des compteurs déjà ajoutés -->
                  <v-sheet v-if="formData.compteurs.length > 0 && !showCounterForm" class="pa-4 mb-4" elevation="0"
                    rounded>
                    <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                      Compteurs ajoutés ({{ formData.compteurs.length }})
                    </v-card-subtitle>

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
                          <v-chip v-if="compteur.estPrincipal" size="x-small" color="primary"
                            class="ml-2">Principal</v-chip>
                          <v-chip v-if="compteur.estGlissant" size="x-small" color="info" class="ml-1">Glissant</v-chip>
                        </v-list-item-subtitle>

                        <template #append>
                          <v-btn icon="mdi-pencil" size="small" variant="text" color="primary"
                            @click="internalHandleCounterEdit(compteur)" />
                          <v-btn icon="mdi-delete" size="small" variant="text" color="error"
                            @click="handleCounterDelete(compteur)" />
                        </template>
                      </v-list-item>
                    </v-list>

                    <v-divider class="my-4" />

                    <!-- Bouton d'ajout -->
                    <div class="d-flex justify-center">
                      <v-btn color="primary" variant="text" prepend-icon="mdi-plus" @click="handleCounterAdd">
                        Ajouter un autre compteur
                      </v-btn>
                    </div>
                  </v-sheet>

                  <!-- Formulaire pour ajouter/éditer un compteur -->
                  <div v-if="showCounterForm" class="mb-6">
                    <CounterInlineForm v-model="currentCounter" :existingPMs="existingPMs" :typesPM="typesPM"
                      :consumables="consumables" :typesDocuments="typesDocuments"
                      :isEditMode="editingCounterIndex >= 0" :isFirstCounter="formData.compteurs.length === 0"
                      @save="internalSaveCurrentCounter" @cancel="cancelCounterForm" />
                  </div>
                </v-stepper-window-item>

                <!-- Navigation -->
                <v-row justify="space-between" class="mt-6 mb-2">
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
          <CounterInlineForm v-model="currentCounter" :existingPMs="existingPMs" :typesPM="typesPM"
            :consumables="consumables" :typesDocuments="typesDocuments" @save="saveCurrentCounter"
            @cancel="closeCounterDialog" />
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showFabricantDialog" max-width="600" scrollable>
      <v-card>
        <v-card-text class="pa-6">
          <FabricantForm @created="handleFabricantCreated" @close="showFabricantDialog = false" />
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showFournisseurDialog" max-width="600" scrollable>
      <v-card>
        <v-card-text class="pa-6">
          <FournisseurForm @created="handleFournisseurCreated" @close="showFournisseurDialog = false" />
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showModeleDialog" max-width="600" scrollable>
      <v-card>
        <v-card-text class="pa-6">
          <ModeleEquipementForm :fabricants="fabricants" @created="handleModeleCreated" @close="showModeleDialog = false"
            @fabricant-created="handleFabricantCreated" />
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showFamilleDialog" max-width="500" scrollable>
      <v-card>
        <v-card-text class="pa-6">
          <FamilleEquipementForm :families="familles" @created="handleFamilleCreated" @close="showFamilleDialog = false" />
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showLieuDialog" max-width="600" scrollable>
      <v-card>
        <v-card-text class="pa-6">
          <LieuForm :parent-id="selectedParentLieuId" :locations="locations" @created="handleLieuCreated" @close="showLieuDialog = false" />
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { BaseForm } from '@/components/common';
import { API_BASE_URL, EQUIPMENT_CREATE_STEPS } from '@/utils/constants';
import { useEquipmentForm } from '@/composables/useEquipmentForm';
import EquipmentFormFields from '@/components/Forms/EquipmentFormFields.vue';
import CounterInlineForm from '@/components/Forms/CounterInlineForm.vue';
import FabricantForm from '@/components/Forms/FabricantForm.vue';
import FournisseurForm from '@/components/Forms/FournisseurForm.vue';
import ModeleEquipementForm from '@/components/Forms/ModeleEquipementForm.vue';
import FamilleEquipementForm from '@/components/Forms/FamilleEquipementForm.vue';
import LieuForm from '@/components/Forms/LieuForm.vue';

const {
  formData,
  loading,
  loadingData,
  errorMessage,
  successMessage,
  locations,
  equipmentModels,
  fournisseurs,
  fabricants,
  consumables,
  familles,
  typesPM,
  typesDocuments,
  equipmentStatuses,
  currentCounter,
  isCounterEditMode,
  existingPMs,
  showCounterDialog,
  showFabricantDialog,
  showFournisseurDialog,
  showModeleDialog,
  showFamilleDialog,
  handleFileUpload,
  fetchData,
  handleCounterEdit,
  handleCounterDelete,
  saveCurrentCounter,
  closeCounterDialog,
  handleFabricantCreated,
  handleFournisseurCreated,
  handleModeleCreated,
  handleFamilleCreated,
  handleLocationCreated,
  getEmptyCounter,
  api,
  router
} = useEquipmentForm();

const step = ref(1);
const visitedSteps = ref([1]);
const showCounterForm = ref(true);
const editingCounterIndex = ref(-1);
const showLieuDialog = ref(false);
const selectedParentLieuId = ref(null);

//Règles de validation par étape
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
    errorMessage.value = 'L\'équipement n\'a pas pu être créé. Veuillez vérifier les informations saisies.';
  } finally {
    loading.value = false;
  }
};

const handleCounterAdd = () => {
  editingCounterIndex.value = -1;
  currentCounter.value = getEmptyCounter();
  showCounterForm.value = true;
};

const internalHandleCounterEdit = (counter) => {
  handleCounterEdit(counter);
  editingCounterIndex.value = formData.value.compteurs.indexOf(counter);
  showCounterForm.value = true;
};

const internalSaveCurrentCounter = () => {
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
    formData.value.compteurs[editingCounterIndex.value] = counterToSave;
  } else {
    formData.value.compteurs.push(counterToSave);
  }

  if (counterToSave.planMaintenance.nom &&
    !existingPMs.value.some(pm => pm.nom === counterToSave.planMaintenance.nom)) {
    existingPMs.value.push({
      nom: counterToSave.planMaintenance.nom,
      type: counterToSave.planMaintenance.type,
      consommables: [...counterToSave.planMaintenance.consommables],
      documents: [...counterToSave.planMaintenance.documents]
    });
  }

  showCounterForm.value = false;
  editingCounterIndex.value = -1;
  currentCounter.value = getEmptyCounter();
};

const cancelCounterForm = () => {
  if (formData.value.compteurs.length > 0) {
    showCounterForm.value = false;
    editingCounterIndex.value = -1;
    currentCounter.value = getEmptyCounter();
  }
};

const nextStep = () => {
  if (step.value < 6) {
    step.value++;
    if (!visitedSteps.value.includes(step.value)) {
      visitedSteps.value.push(step.value);
    }
  }
};

const prevStep = () => {
  if (step.value > 1) step.value--;
};

const goToStep = (targetStep) => {
  if (isStepEditable(targetStep)) {
    step.value = targetStep;
  }
};

const isStepComplete = (stepNumber) => {
  return visitedSteps.value.includes(stepNumber) && step.value > stepNumber;
};

const isStepEditable = (stepNumber) => {
  return visitedSteps.value.includes(stepNumber);
};

const canGoToNextStep = (validation) => {
  if (!validation) return true;
  return validation.isStepValid(step.value, formData.value);
};

const handleOpenLieuDialog = (parentId) => {
  selectedParentLieuId.value = parentId;
  showLieuDialog.value = true;
};

const handleLieuCreated = async (newLieu) => {
  console.log('Nouveau lieu créé:', newLieu);
  // Rafraîchir la liste des lieux
  await fetchData();
  // Fermer la dialog
  showLieuDialog.value = false;
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