<template>
  <v-app>
    <v-main>
      <v-container>
        <BaseForm v-model="formData" title="Créer un Équipement" :loading="loading" :error-message="errorMessage"
          :success-message="successMessage" :loading-message="loadingData ? 'Chargement des données...' : ''"
          :validation-schema="validationSchema" submit-button-text="Créer un Équipement" :handleSubmit="handleSubmit"
          actions-container-class="d-flex justify-end gap-2 mt-3" submit-button-class="mt-3"
          cancel-button-class="mt-3 mr-3" :showActions="showFormActions">
          <template #default="{ validation }">
            <v-stepper v-model="step" :steps="EQUIPMENT_CREATE_STEPS.length" justify="center" alt-labels>
              <v-stepper-header class="justify-center">
                <v-stepper-item v-for="(label, index) in EQUIPMENT_CREATE_STEPS" :key="index" :value="index + 1"
                  :complete="isStepComplete(index + 1)" :editable="isStepEditable(index + 1)"
                  :color="isStepEditable(index + 1) ? 'primary' : undefined" @click="goToStep(index + 1)">
                  <template #title>
                    <span class="step-label">{{ label }}</span>
                  </template>
                </v-stepper-item>
              </v-stepper-header>

              <v-stepper-window v-model="step" :steps="EQUIPMENT_CREATE_STEPS.length" class="mb-8">
                <!-- Étape 1: Informations générales  & Statut -->
                <v-stepper-window-item :value="1">
                  <EquipmentFormFields v-model="formData" :equipment-models="equipmentModels"
                    :fournisseurs="fournisseurs" :fabricants="fabricants" :familles="familles" :locations="locations"
                    :consumables="consumables" :equipment-statuses="equipmentStatuses" :step="1" :show-location="false"
                    :show-status="true" :show-consommables="false" :show-counters="false" :show-general="true"
                    :show-model-info="false" @file-upload="handleFileUpload" @location-created="handleLocationCreated"
                    @open-modele-dialog="showModeleDialog = true"
                    @open-fournisseur-dialog="showFournisseurDialog = true"
                    @open-fabricant-dialog="showFabricantDialog = true" @open-famille-dialog="showFamilleDialog = true"
                    @open-lieu-dialog="handleOpenLieuDialog" @open-consommable-dialog="showConsommableDialog = true" />
                </v-stepper-window-item>

                <!-- Étape 2: Fournisseur et Fabricant -->
                <v-stepper-window-item :value="2">
                  <EquipmentFormFields v-model="formData" :equipment-models="equipmentModels"
                    :fournisseurs="fournisseurs" :fabricants="fabricants" :familles="familles" :locations="locations"
                    :consumables="consumables" :equipment-statuses="equipmentStatuses" :step="2" :show-location="false"
                    :show-status="false" :show-consommables="true" :show-counters="false" :show-general="false"
                    :show-model-info="true" @file-upload="handleFileUpload" @location-created="handleLocationCreated"
                    @open-modele-dialog="showModeleDialog = true"
                    @open-fournisseur-dialog="showFournisseurDialog = true"
                    @open-fabricant-dialog="showFabricantDialog = true" @open-famille-dialog="showFamilleDialog = true"
                    @open-lieu-dialog="handleOpenLieuDialog" @open-consommable-dialog="showConsommableDialog = true" />
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
                    @open-fabricant-dialog="showFabricantDialog = true" @open-famille-dialog="showFamilleDialog = true"
                    @open-lieu-dialog="handleOpenLieuDialog" />
                </v-stepper-window-item>

                <!-- Étape 4: Compteurs -->
                <v-stepper-window-item :value="4">
                  <v-card variant="outlined" class="pa-4">
                    <v-card-title class="text-h6 font-weight-bold px-0 pb-4 d-flex align-center justify-space-between">
                      <span>Compteurs de l'équipement</span>
                      <v-btn color="primary" size="small" @click="handleCounterAdd" prepend-icon="mdi-plus">
                        Ajouter un compteur
                      </v-btn>
                    </v-card-title>

                    <v-card-text>
                      <!-- Liste des compteurs -->
                      <div v-if="visibleCounters.length > 0">
                        <v-row>
                          <v-col v-for="(compteur, index) in visibleCounters" :key="index" cols="12">
                            <v-card variant="outlined" class="pa-4">
                              <div class="d-flex align-center justify-space-between mb-2">
                                <div class="d-flex align-center gap-2">
                                  <v-icon color="primary">mdi-counter</v-icon>
                                  <h3 class="text-h6 mr-2">{{ compteur.nom || 'Compteur sans nom' }}</h3>
                                  <v-chip v-if="compteur.estPrincipal" color="primary" size="small" label>
                                    Principal
                                  </v-chip>
                                </div>
                                <div class="d-flex gap-2">
                                  <v-btn icon="mdi-pencil" size="small" color="primary" variant="text"
                                    @click="handleCounterEdit(compteur)" />
                                  <v-btn icon="mdi-delete" size="small" color="error" variant="text"
                                    @click="handleCounterDelete(compteur)" />
                                </div>
                              </div>
                              
                              <v-divider class="my-3" />
                              
                              <v-row dense>
                                <v-col cols="6" md="3">
                                  <div class="text-caption text-grey">Valeur courante</div>
                                  <div class="text-body-1">{{ compteur.type === 'Calendaire' ? ordinalToDate(compteur.valeurCourante) : compteur.valeurCourante }} {{ compteur.type !== 'Calendaire' ? compteur.unite : '' }}</div>
                                </v-col>
                                <v-col cols="6" md="3">
                                  <div class="text-caption text-grey">Unité</div>
                                  <div class="text-body-1">{{ compteur.unite }}</div>
                                </v-col>
                              </v-row>
                            </v-card>
                          </v-col>
                        </v-row>

                        <v-alert type="info" variant="tonal" class="mt-4">
                          <v-icon>mdi-information</v-icon>
                          Les compteurs permettent de suivre l'utilisation de l'équipement. Au moins un compteur doit être marqué comme "Principal".
                        </v-alert>
                      </div>

                      <div v-else class="text-center py-8 text-grey">
                        <v-icon size="large" class="mb-2">mdi-counter</v-icon>
                        <div class="text-h6 mb-2">Aucun compteur défini</div>
                        <div class="text-body-1 mb-4">Ajoutez au moins un compteur pour suivre l'utilisation de l'équipement</div>
                        <v-btn color="primary" @click="handleCounterAdd" prepend-icon="mdi-plus">
                          Ajouter un compteur
                        </v-btn>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-stepper-window-item>

                <!-- Etape 5: Définition des périodicités -->
                <v-stepper-window-item :value="5">
                  <v-card variant="outlined" class="pa-4">
                    <v-card-title class="text-h6 font-weight-bold px-0 pb-4 d-flex align-center justify-space-between">
                      <span>Définition des périodicités</span>
                      <v-btn color="primary" size="small" @click="openPeriodicMaintenanceDialog" prepend-icon="mdi-plus"
                        :disabled="!hasCalendarCounter">
                        Ajouter une périodicité
                      </v-btn>
                    </v-card-title>

                    <v-card-text>
                      <!-- Message si pas de compteurs -->
                      <v-alert v-if="!hasCalendarCounter" type="warning"
                        variant="tonal" class="mb-4">
                        <v-alert-title class="text-body-1">Compteur calendaire requis</v-alert-title>
                        Un compteur calendaire est requis pour pouvoir définir des
                        périodicités.
                      </v-alert>

                      <!-- Liste des périodicités -->
                      <div v-if="periodicMaintenancePlans.length > 0">
                        <v-row>
                          <v-col v-for="(plan, index) in periodicMaintenancePlans" :key="index" cols="12">
                            <v-card variant="outlined" class="pa-4">
                              <div class="d-flex align-center justify-space-between mb-2">
                                <div class="d-flex align-center gap-2">
                                  <v-icon color="primary">mdi-clipboard-check</v-icon>
                                  <h3 class="text-h6">{{ plan.nom || 'Plan sans nom' }}</h3>
                                  <v-chip v-if="plan.type_id" :color="getPlanTypeColor(plan)" size="small" label>
                                    {{ getPlanTypeName(plan) }}
                                  </v-chip>
                                </div>
                                <div class="d-flex gap-2">
                                  <v-btn icon="mdi-pencil" size="small" color="primary" variant="text"
                                    @click="handlePeriodicPlanEdit(plan)" />
                                  <v-btn icon="mdi-delete" size="small" color="error" variant="text"
                                    @click="handlePlanDelete(plan)" />
                                </div>
                              </div>
                              
                              <v-divider class="my-3" />
                              
                              <v-row dense>
                                <v-col cols="12" md="6">
                                  <div class="text-caption text-grey">Compteur associé</div>
                                  <div class="text-body-1">{{ getCounterName(plan.compteurIndex) }}</div>
                                </v-col>
                                <v-col cols="12" md="3">
                                  <div class="text-caption text-grey">Intervalle</div>
                                  <div class="text-body-1">{{ 
                                    getCounterType(plan.compteurIndex) === 'Calendaire' 
                                      ? getSeuilInterval(plan.seuil.ecartInterventions) 
                                      : `${plan.seuil.ecartInterventions} ${getCounterUnit(plan.compteurIndex)}`
                                   }}</div>
                                </v-col>
                                <v-col cols="12" md="3">
                                  <div class="text-caption text-grey">Prochaine maintenance</div>
                                  <div class="text-body-1">{{ 
                                    getCounterType(plan.compteurIndex) === 'Calendaire' 
                                      ? getSeuilNextMaintenance(plan.seuil.prochaineMaintenance) 
                                      : `${plan.seuil.prochaineMaintenance} ${getCounterUnit(plan.compteurIndex)}`
                                  }}</div>
                                </v-col>
                              </v-row>

                              <v-row dense class="mt-2" v-if="plan.necessiteHabilitationElectrique || plan.necessitePermisFeu">
                                <v-col cols="12">
                                  <div class="text-caption text-grey mb-1">Habilitations requises</div>
                                  <v-chip v-if="plan.necessiteHabilitationElectrique" size="x-small" color="orange" class="mr-1">
                                    <v-icon start size="x-small">mdi-flash</v-icon>
                                    Hab. élec.
                                  </v-chip>
                                  <v-chip v-if="plan.necessitePermisFeu" size="x-small" color="error">
                                    <v-icon start size="x-small">mdi-fire</v-icon>
                                    Permis feu
                                  </v-chip>
                                </v-col>
                              </v-row>
                            </v-card>
                          </v-col>
                        </v-row>

                        <v-alert type="info" variant="tonal" class="mt-4">
                          <v-icon>mdi-information</v-icon>
                          Les périodicités permettent de définir le rythme des interventions préventives.
                        </v-alert>
                      </div>

                      <div v-else-if="hasCalendarCounter"
                        class="text-center py-8 text-grey">
                        <v-icon size="large" class="mb-2">mdi-calendar-clock</v-icon>
                        <div class="text-h6 mb-2">Aucune périodicité définie</div>
                        <div class="text-body-1 mb-4">Ajoutez des périodicités pour programmer les interventions
                          préventives
                        </div>
                        <v-btn color="primary" @click="openPeriodicMaintenanceDialog" prepend-icon="mdi-plus">
                          Ajouter une périodicité
                        </v-btn>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-stepper-window-item>

                <!-- Etape 6: Définition des seuils -->
                <v-stepper-window-item :value="6">
                  <v-card variant="outlined" class="pa-4">
                    <v-card-title class="text-h6 font-weight-bold px-0 pb-4 d-flex align-center justify-space-between">
                      <span>Définition des seuils</span>
                      <v-btn color="primary" size="small" @click="openPreventiveMaintenanceDialog" prepend-icon="mdi-plus"
                        :disabled="!hasUserCounters">
                        Ajouter un seuil
                      </v-btn>
                    </v-card-title>

                    <v-card-text>
                      <v-alert type="info" variant="tonal" class="mb-4">
                        <v-icon>mdi-information</v-icon>
                        Créez ici les maintenances préventives non périodiques basées sur des seuils numériques.
                      </v-alert>

                      <div v-if="preventiveMaintenancePlans.length > 0">
                        <v-row>
                          <v-col v-for="(plan, index) in preventiveMaintenancePlans" :key="`review-${index}`" cols="12">
                            <v-card variant="outlined" class="pa-4">
                              <div class="d-flex align-center justify-space-between mb-2">
                                <div class="d-flex align-center gap-2">
                                  <v-icon color="primary">mdi-clipboard-check</v-icon>
                                  <h3 class="text-h6">{{ plan.nom || 'Plan sans nom' }}</h3>
                                  <v-chip v-if="plan.type_id" :color="getPlanTypeColor(plan)" size="small" label>
                                    {{ getPlanTypeName(plan) }}
                                  </v-chip>
                                </div>
                              </div>

                              <v-divider class="my-3" />

                              <v-row dense>
                                <v-col cols="12" md="6">
                                  <div class="text-caption text-grey">Compteur associé</div>
                                  <div class="text-body-1">{{ getCounterName(plan.compteurIndex) }}</div>
                                </v-col>
                                <v-col cols="12" md="3">
                                  <div class="text-caption text-grey">Intervalle</div>
                                  <div class="text-body-1">{{ 
                                    getCounterType(plan.compteurIndex) === 'Calendaire' 
                                      ? getSeuilInterval(plan.seuil.ecartInterventions) 
                                      : `${plan.seuil.ecartInterventions} ${getCounterUnit(plan.compteurIndex)}`
                                   }}</div>
                                </v-col>
                                <v-col cols="12" md="3">
                                  <div class="text-caption text-grey">Prochaine maintenance</div>
                                  <div class="text-body-1">{{ 
                                    getCounterType(plan.compteurIndex) === 'Calendaire' 
                                      ? getSeuilNextMaintenance(plan.seuil.prochaineMaintenance) 
                                      : `${plan.seuil.prochaineMaintenance} ${getCounterUnit(plan.compteurIndex)}`
                                  }}</div>
                                </v-col>
                              </v-row>
                            </v-card>
                          </v-col>
                        </v-row>
                      </div>

                      <div v-else class="text-center py-8 text-grey">
                        <v-icon size="large" class="mb-2">mdi-clipboard-check-outline</v-icon>
                        <div class="text-h6 mb-2">Aucun seuil à afficher</div>
                        <div class="text-body-1 mb-4">Les opérations liées au calendrier ne sont pas affichées ici.</div>
                        <v-btn color="primary" @click="openPreventiveMaintenanceDialog" prepend-icon="mdi-plus"
                          :disabled="!hasUserCounters">
                          Ajouter un seuil
                        </v-btn>
                      </div>

                    </v-card-text>
                  </v-card>
                </v-stepper-window-item>

                <!-- Navigation -->
                <v-row justify="space-between" class="mt-6 mb-2">
                  <v-btn type="button" variant="text" @click="prevStep" :disabled="step === 1">
                    Précédent
                  </v-btn>

                  <v-btn
                    type="button"
                    variant="text"
                    color="primary"
                    v-if="step < EQUIPMENT_CREATE_STEPS.length && !(step === 4 && !hasUserCounters)"
                    @click="nextStep" :disabled="!canGoToNextStep(validation)">
                    Suivant
                  </v-btn>
                </v-row>
              </v-stepper-window>
            </v-stepper>
          </template>
        </BaseForm>
      </v-container>
    </v-main>

    <v-dialog v-model="showCounterDialog" max-width="1000px" @click:outside="closeCounterDialog" persistent>
      <v-card>
        <v-card-title>
          {{ isCounterEditMode ? 'Modifier un compteur' : 'Ajouter un compteur' }}
        </v-card-title>
        <v-card-text>
          <CounterInlineForm v-model="currentCounter" :isEditMode="isCounterEditMode"
            @save="saveCurrentCounter" @cancel="closeCounterDialog" />
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showPlanDialog" max-width="1000px" @click:outside="closePlanDialog" persistent>
      <v-card>
        <v-card-title>
          {{ isPlanEditMode ? 'Modifier un plan de maintenance' : 'Ajouter un plan de maintenance' }}
        </v-card-title>
        <v-card-text>
          <MaintenancePlanInlineForm v-model="currentPlan" :isEditMode="isPlanEditMode"
            :counters="formData.compteurs" :typesPM="typesPM" :consumables="consumables"
            :typesDocuments="typesDocuments" :show-pm-selection="true" :existing-p-ms="existingPMs"
            :counter-filter="maintenanceCounterFilter"
            @save="savePlan" @cancel="closePlanDialog" />
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
          <ModeleEquipementForm :fabricants="fabricants" @created="handleModeleCreated"
            @close="showModeleDialog = false" @fabricant-created="handleFabricantCreated" />
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showFamilleDialog" max-width="500" scrollable>
      <v-card>
        <v-card-text class="pa-6">
          <FamilleEquipementForm :families="familles" @created="handleFamilleCreated"
            @close="showFamilleDialog = false" />
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showLieuDialog" max-width="600" scrollable>
      <v-card>
        <v-card-text class="pa-6">
          <LieuForm :parent-id="selectedParentLieuId" :locations="locations" @created="handleLieuCreated"
            @close="showLieuDialog = false" />
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showConsommableDialog" max-width="600" scrollable>
      <v-card>
        <v-card-text class="pa-6">
          <ConsommableForm :magasins="magasins" @created="handleConsommableCreated"
            @close="showConsommableDialog = false" @magasin-created="handleMagasinCreated" />
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import { BaseForm } from '@/components/common';
import { API_BASE_URL, EQUIPMENT_CREATE_STEPS, COUNTER_UNITS } from '@/utils/constants';
import { useEquipmentForm } from '@/composables/useEquipmentForm';
import EquipmentFormFields from '@/components/Forms/EquipmentFormFields.vue';
import CounterInlineForm from '@/components/Forms/CounterInlineForm.vue';
import MaintenancePlanInlineForm from '@/components/Forms/MaintenancePlanInlineForm.vue';
import FabricantForm from '@/components/Forms/FabricantForm.vue';
import FournisseurForm from '@/components/Forms/FournisseurForm.vue';
import ModeleEquipementForm from '@/components/Forms/ModeleEquipementForm.vue';
import FamilleEquipementForm from '@/components/Forms/FamilleEquipementForm.vue';
import LieuForm from '@/components/Forms/LieuForm.vue';
import ConsommableForm from '@/components/Forms/ConsommableForm.vue';

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
  currentPlan,
  isPlanEditMode,
  existingPMs,
  showCounterDialog,
  showPlanDialog,
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
  handlePlanAdd,
  handlePlanEdit,
  handlePlanDelete,
  savePlan,
  closePlanDialog,
  handleFabricantCreated,
  handleFournisseurCreated,
  handleModeleCreated,
  handleFamilleCreated,
  handleLocationCreated,
  getEmptyCounter,
  api,
  router,
  ordinalToDate,
} = useEquipmentForm();

const step = ref(1);
const visitedSteps = ref([1]);
const showCounterForm = ref(true);
const editingCounterIndex = ref(-1);
const showLieuDialog = ref(false);
const selectedParentLieuId = ref(null);
const showConsommableDialog = ref(false);
const magasins = ref([]);
const openedMaintenancePanels = ref([0]);

const visibleCounters = computed(() =>
  (formData.value?.compteurs || []).filter(counter => !counter?.isDefaultCalendar && counter?.type !== 'Calendaire')
);

const hasUserCounters = computed(() => visibleCounters.value.length > 0);
const hasCalendarCounter = computed(() =>
  (formData.value?.compteurs || []).some(counter => counter?.isDefaultCalendar || counter?.type === 'Calendaire')
);

const maintenanceCounterFilter = ref('calendar');

const periodicMaintenancePlans = computed(() =>
  (formData.value?.plansMaintenance || []).filter(plan => {
    if (plan?.compteurIndex === null || plan?.compteurIndex === undefined) {
      return false;
    }

    const counter = formData.value?.compteurs?.[plan.compteurIndex];
    return !!(counter?.isDefaultCalendar || counter?.type === 'Calendaire');
  })
);

const preventiveMaintenancePlans = computed(() =>
  (formData.value?.plansMaintenance || []).filter(plan => {
    if (plan?.compteurIndex === null || plan?.compteurIndex === undefined) {
      return false;
    }

    const counter = formData.value?.compteurs?.[plan.compteurIndex];
    return !(counter?.isDefaultCalendar || counter?.type === 'Calendaire');
  })
);

const openPeriodicMaintenanceDialog = async () => {
  maintenanceCounterFilter.value = 'calendar';
  await nextTick();
  handlePlanAdd();
};

const openPreventiveMaintenanceDialog = async () => {
  maintenanceCounterFilter.value = 'numeric';
  await nextTick();
  handlePlanAdd();
  const firstNumericCounterIndex = (formData.value?.compteurs || []).findIndex(
    counter => !counter?.isDefaultCalendar && counter?.type !== 'Calendaire'
  );
  if (firstNumericCounterIndex >= 0) {
    currentPlan.value.compteurIndex = firstNumericCounterIndex;
  } else {
    currentPlan.value.compteurIndex = null;
  }
};

const handlePeriodicPlanEdit = (plan) => {
  maintenanceCounterFilter.value = 'calendar';
  handlePlanEdit(plan);
};

// Affiche les actions (dont "Créer") à l'étape 4 si aucun compteur utilisateur, sinon seulement à la dernière étape.
const showFormActions = computed(() =>
  step.value === EQUIPMENT_CREATE_STEPS.length || (step.value === 4 && !hasUserCounters.value)
);

// Helpers de navigation entre étapes
const getSeuilInterval = (intervalle) => {
  if (intervalle === null || intervalle === undefined) return "—";

    const days = Math.round(intervalle / 1000 / 60 / 60 / 24);
    if (days === 0) return "0 jour";

    const years = Math.floor(days / 365);
    const remainingAfterYears = days % 365;

    const months = Math.floor(remainingAfterYears / 30);
    const remDays = remainingAfterYears % 30;

    const parts = [];
    if (years) parts.push(`${years} ${years > 1 ? "ans" : "an"}`);
    if (months) parts.push(`${months} mois`);
    if (remDays) parts.push(`${remDays} ${remDays > 1 ? "jours" : "jour"}`);

    return parts.join(" ");
};

const getSeuilNextMaintenance = (nextMaintenance) => {
  if (nextMaintenance === null || nextMaintenance === undefined) return "—";

  // Cas : nombre de jours (calendaire backend)
  if (typeof nextMaintenance === "number") {
    const baseDate = new Date(1, 0, 1);
    baseDate.setDate(baseDate.getDate() + nextMaintenance);
    return baseDate.toLocaleDateString("fr-FR");
  }

  // Cas : string YYYY-MM-DD
  if (typeof nextMaintenance === "string") {
    const date = new Date(nextMaintenance);
    if (isNaN(date.getTime())) return "—";
    return date.toLocaleDateString("fr-FR");
  }

  return "—";
};


//Règles de validation par étape
const validationSchema = {
  step1: {
    numSerie: [{ name: 'minLength', params: [1] }, { name: 'maxLength', params: [100] }],
    designation: ['required', { name: 'maxLength', params: [100] }],
    reference: ['required', { name: 'maxLength', params: [100] }],
    dateMiseEnService: ['required'],
    prixAchat: ['numeric', 'positive'],
    statut: ['required'],
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
    // compteurs: ['required', { name: 'minItems', params: [1] }],
  },
  step5: {
  },
  step6: {
  },
};

const handleSubmit = async () => {
  // Validation basique : au moins un compteur requis
  // if (formData.value.compteurs.length === 0) {
  //   errorMessage.value = 'Au moins un compteur est requis';
  //   step.value = 6;  // Rediriger vers l'étape des compteurs
  //   return;
  // }

  // Validation des compteurs
  const invalidCounters = (formData.value.compteurs || []).filter(c =>
    !c?.isDefaultCalendar && (!c.nom || !c.unite)
  );

  if (invalidCounters.length > 0) {
    errorMessage.value = 'Tous les compteurs doivent avoir un nom et une unité';
    step.value = 4;
    return;
  }

  // Validation que le statut est défini
  if (!formData.value.statut) {
    errorMessage.value = 'Le statut de l\'équipement est requis';
    step.value = 1;
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
        // Envoyer uniquement les données de base du compteur
        const compteursData = formData.value.compteurs.map(c => ({
          id: c.id,
          nom: c.nom,
          valeurCourante: c.valeurCourante ?? 0,
          unite: c.unite,
          estPrincipal: c.estPrincipal,
          type: c.type
        }));
        fd.append(key, JSON.stringify(compteursData));
      } else if (key === 'plansMaintenance') {
        // Envoyer les plans de maintenance séparément
        const plansData = formData.value.plansMaintenance.map((p, planIndex) => {
          const docsAvecFichier = (p.documents || []).filter((d) => d?.file instanceof File);

          docsAvecFichier.forEach((doc, docIndex) => {
            fd.append(`pm_${planIndex}_document_${docIndex}`, doc.file);
          });

          return {
          id: p.id,
          nom: p.nom,
          type_id: p.type_id,
          description: p.description,
          compteurIndex: p.compteurIndex,
          consommables: p.consommables,
          necessiteHabilitationElectrique: p.necessiteHabilitationElectrique,
          necessitePermisFeu: p.necessitePermisFeu,
          documents: docsAvecFichier.map((doc) => ({
            titre: doc.nom || doc.nomDocument || doc.titre || '',
            type: doc.type_id ?? doc.typeDocument_id ?? doc.type ?? null
          })),
          seuil: {
            estGlissant: p.seuil.estGlissant,
            derniereIntervention: p.seuil.derniereIntervention ?? 0,
            ecartInterventions: p.seuil.ecartInterventions ?? 0,
            prochaineMaintenance: p.seuil.prochaineMaintenance ?? 0
          }
          };
        });
        fd.append(key, JSON.stringify(plansData));
      } else if (key === 'lienImageEquipement') {
        if (formData.value[key] instanceof File) {
          fd.append('lienImageEquipement', formData.value[key]);
        }
      } else if (formData.value[key] !== null && formData.value[key] !== undefined) {
        fd.append(key, formData.value[key]);
      }
    }

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
  isCounterEditMode.value = false;
  currentCounter.value = getEmptyCounter();
  currentCounter.value.estPrincipal = visibleCounters.value.length === 0;
  showCounterDialog.value = true;
};

const updateCounter = (index) => {
  formData.value.compteurs[index] = { ...formData.value.compteurs[index] };
};

// Fonctions helper pour l'affichage des plans
const getCounterName = (compteurIndex) => {
  if (compteurIndex === null || compteurIndex === undefined) return 'Non défini';
  const counter = formData.value.compteurs[compteurIndex];
  return counter ? counter.nom : 'Non défini';
};

const getCounterType = (compteurIndex) => {
  if (compteurIndex === null || compteurIndex === undefined) return '';
  const counter = formData.value.compteurs[compteurIndex];
  return counter ? counter.type : '';
};

const getCounterUnit = (compteurIndex) => {
  if (compteurIndex === null || compteurIndex === undefined) return '';
  const counter = formData.value.compteurs[compteurIndex];
  return counter ? counter.unite : '';
};

const getPlanTypeName = (plan) => {
  const type = typesPM.value.find(t => t.id === plan.type_id);
  return type ? type.libelle : 'Non défini';
};

const getPlanTypeColor = (plan) => {
  return 'primary';
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
  if (step.value < EQUIPMENT_CREATE_STEPS.length) {
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
  // Si aucun compteur, on ne va pas au step 5 (on crée directement au step 4).
  if (step.value === 4 && !hasUserCounters.value) return false;

  // Si on a des compteurs, on empêche la navigation si un compteur est incomplet.
  if (step.value === 4 && hasUserCounters.value) {
    const hasInvalidCounter = (formData.value.compteurs || []).some(c => !c?.isDefaultCalendar && (!c.nom || !c.unite));
    if (hasInvalidCounter) return false;
  }
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

const handleConsommableCreated = async (newConsommable) => {
  console.log('Nouveau consommable créé:', newConsommable);
  // Rafraîchir la liste des consommables
  await fetchData();
  // Ajouter le consommable à la sélection
  if (!formData.value.consommables.includes(newConsommable.id)) {
    formData.value.consommables.push(newConsommable.id);
  }
  // Fermer la dialog
  showConsommableDialog.value = false;
};

const handleMagasinCreated = async (newMagasin) => {
  console.log('Nouveau magasin créé:', newMagasin);
  // Rafraîchir la liste des magasins
  await fetchMagasins();
};

const fetchMagasins = async () => {
  try {
    const data = await api.get('magasins/');
    magasins.value = data;
  } catch (error) {
    console.error('Erreur lors du chargement des magasins:', error);
  }
};

onMounted(async () => {
  await fetchData();
  await fetchMagasins();
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