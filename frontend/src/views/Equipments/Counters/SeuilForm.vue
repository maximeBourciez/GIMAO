<template>
  <v-card>
    <v-card-title class="text-h5 pa-4">
      {{ formTitle }}
    </v-card-title>
    <v-divider></v-divider>

    <v-card-text class="pa-4">
      <!-- Sélection de PM existant ou création -->
      <v-card class="mb-4" variant="outlined">
        <v-card-text>
          <v-radio-group v-model="pmMode" inline hide-details>
            <v-radio label="Sélectionner un PM existant" value="existing"></v-radio>
            <v-radio label="Créer un nouveau PM" value="new"></v-radio>
          </v-radio-group>
        </v-card-text>
      </v-card>

      <!-- Sélection PM existant -->
      <v-card v-if="pmMode === 'existing'" class="mb-4" variant="outlined">
        <v-card-text>
          <v-select 
            v-model="selectedExistingPMId" 
            :items="existingPMs" 
            item-title="nom" 
            item-value="id"
            label="Sélectionner un plan de maintenance" 
            variant="outlined" 
            density="comfortable"
            clearable
          >
            <template #item="{ props, item }">
              <v-list-item v-bind="props">
                <template #title>{{ item.raw.nom }}</template>
                <template #subtitle>{{ getPMTypeLabel(item.raw.type_id) }}</template>
              </v-list-item>
            </template>
          </v-select>

          <!-- Aperçu du PM sélectionné -->
          <v-card v-if="selectedExistingPM" class="mt-4" elevation="2" color="blue-lighten-5">
            <v-card-title class="text-subtitle-1 font-weight-bold py-3">
              <v-icon left color="primary">mdi-clipboard-check</v-icon>
              Aperçu du plan de maintenance
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <v-row dense class="mb-2">
                <v-col cols="12" md="6">
                  <div class="text-caption text-grey-darken-1 mb-1">Nom du plan</div>
                  <div class="text-body-1 font-weight-medium">{{ selectedExistingPM.nom }}</div>
                </v-col>
                <v-col cols="12" md="6">
                  <div class="text-caption text-grey-darken-1 mb-1">Type de maintenance</div>
                  <v-chip size="small" color="primary">
                    {{ getPMTypeLabel(selectedExistingPM.type_id) }}
                  </v-chip>
                </v-col>
              </v-row>
              <v-row dense v-if="selectedExistingPM.commentaire">
                <v-col cols="12">
                  <div class="text-caption text-grey-darken-1 mb-1">Commentaire</div>
                  <div class="text-body-2">{{ selectedExistingPM.commentaire }}</div>
                </v-col>
              </v-row>
              <v-row dense class="mt-3" v-if="selectedExistingPM.necessiteHabilitationElectrique || selectedExistingPM.necessitePermisFeu">
                <v-col cols="12">
                  <div class="text-caption text-grey-darken-1 mb-2">Habilitations requises</div>
                  <div class="d-flex gap-2">
                    <v-chip v-if="selectedExistingPM.necessiteHabilitationElectrique" size="small" color="orange" variant="flat">
                      <v-icon left size="small">mdi-flash</v-icon>
                      Habilitation électrique
                    </v-chip>
                    <v-chip v-if="selectedExistingPM.necessitePermisFeu" size="small" color="red" variant="flat">
                      <v-icon left size="small">mdi-fire</v-icon>
                      Permis feu
                    </v-chip>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-card-text>
      </v-card>

      <!-- Création d'un nouveau PM avec MaintenancePlanInlineForm -->
      <div v-else>
        <MaintenancePlanInlineForm 
          v-if="currentPlan"
          v-model="currentPlan"
          :counters="countersForSelect"
          :types-p-m="typesPM"
          :consumables="consumables"
          :is-edit-mode="isEditMode && pmMode === 'new'"
          :show-actions="false"
          @save="handlePlanSave"
          @cancel="handleCancel"
        />
      </div>

      <!-- Section Changements détectés -->
      <v-card v-if="hasChanges && isEditMode" variant="outlined" class="mt-4">
        <v-card-title class="d-flex align-center bg-yellow-lighten-5">
          <v-icon left color="yellow-darken-2">mdi-alert-circle</v-icon>
          <span>Changements détectés</span>
        </v-card-title>
        <v-card-text>
          <v-list density="compact">
            <v-list-item v-for="(change, field) in detectedChanges" :key="field">
              <template v-slot:prepend>
                <v-icon color="primary">mdi-pencil</v-icon>
              </template>
              <v-list-item-title class="font-weight-bold">
                {{ getFieldLabel(field) }}
              </v-list-item-title>
              <v-list-item-subtitle>
                <span class="text-red text-decoration-line-through mr-2">
                  {{ formatChangeValue(change.ancienne) }}
                </span>
                →
                <span class="text-green ml-2">
                  {{ formatChangeValue(change.nouvelle) }}
                </span>
              </v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </v-card-text>

    <v-divider></v-divider>

    <v-card-actions class="pa-4">
      <v-spacer></v-spacer>
      <v-btn variant="text" @click="handleCancel">Annuler</v-btn>
      <v-btn 
        color="primary" 
        :loading="loading"
        :disabled="!isFormValid"
        @click="handleSubmit"
      >
        {{ isEditMode ? 'Enregistrer les modifications' : 'Créer le seuil' }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useApi } from "@/composables/useApi";
import { useStore } from "vuex";
import { API_BASE_URL } from "@/utils/constants";
import MaintenancePlanInlineForm from "@/components/Forms/MaintenancePlanInlineForm.vue";

const props = defineProps({
  seuil: {
    type: Object,
    default: () => ({}),
  },
  existingPMs: {
    type: Array,
    default: () => [],
  },
  typesPM: {
    type: Array,
    default: () => [],
  },
  consumables: {
    type: Array,
    default: () => [],
  },
  typesDocuments: {
    type: Array,
    default: () => [],
  },
  isEdit: {
    type: Boolean,
    default: false,
  },
  equipmentId: {
    type: Number,
    default: null,
  },
  compteurId: {
    type: Number,
    default: null,
  },
});

const emit = defineEmits(["submit", "cancel"]);

const loading = ref(false);
const pmMode = ref(props.isEdit && props.seuil.planMaintenanceId ? "existing" : "new");
const selectedExistingPMId = ref(null);

const api = useApi(API_BASE_URL);
const store = useStore();

// Créer un compteur fictif pour le select du MaintenancePlanInlineForm
const countersForSelect = computed(() => {
  if (!props.compteurId) return [];
  
  return [{
    id: props.compteurId,
    nom: 'Compteur actuel',
    unite: props.seuil?.unite || 'heures',
    valeurCourante: props.seuil?.valeurCourante || 0
  }];
});

// Plan de maintenance actuel
const currentPlan = ref(null);

// Initialiser le plan à partir du seuil
const initializePlan = () => {
  if (props.seuil && props.seuil.planMaintenance) {
    const pm = props.seuil.planMaintenance;
    const seuil = props.seuil;
    
    currentPlan.value = {
      id: pm.id || null,
      nom: pm.nom || '',
      type_id: pm.type_id || null,
      description: pm.commentaire || '',
      compteurIndex: 0, // Premier compteur (le seul)
      consommables: pm.consommables?.map(c => c.consommable_id || c.id) || [],
      seuil: {
        derniereIntervention: seuil.derniereIntervention || 0,
        ecartInterventions: seuil.ecartInterventions || 0,
        prochaineMaintenance: seuil.prochaineMaintenance || 0,
        estGlissant: seuil.estGlissant || false
      },
      necessiteHabilitationElectrique: pm.necessiteHabilitationElectrique || false,
      necessitePermisFeu: pm.necessitePermisFeu || false
    };
  } else {
    // Nouveau plan vide
    currentPlan.value = {
      id: null,
      nom: '',
      type_id: null,
      description: '',
      compteurIndex: 0,
      consommables: [],
      seuil: {
        derniereIntervention: 0,
        ecartInterventions: 0,
        prochaineMaintenance: 0,
        estGlissant: false
      },
      necessiteHabilitationElectrique: false,
      necessitePermisFeu: false
    };
  }
};

// Computed properties
const formTitle = computed(() =>
  props.isEdit ? `Modifier le seuil` : `Ajouter un nouveau seuil`
);

const isEditMode = computed(() => props.isEdit);

const selectedExistingPM = computed(() =>
  props.existingPMs.find(pm => pm.id === selectedExistingPMId.value)
);

const isFormValid = computed(() => {
  if (pmMode.value === 'existing') {
    return !!selectedExistingPMId.value;
  } else {
    return currentPlan.value && 
           currentPlan.value.nom && 
           currentPlan.value.type_id &&
           currentPlan.value.seuil.ecartInterventions > 0;
  }
});

const getPMTypeLabel = (typeId) => {
  const type = props.typesPM.find(t => t.id === typeId);
  return type ? type.libelle : "Non spécifié";
};

const getFieldLabel = (field) => {
  const labels = {
    'planMaintenanceId': 'Plan de maintenance',
  };
  return labels[field] || field;
};

const formatChangeValue = (value) => {
  if (value === null || value === undefined) return "—";
  if (typeof value === 'boolean') return value ? "Oui" : "Non";
  return String(value);
};

// Initialize
onMounted(() => {
  initializePlan();
  
  if (props.seuil && props.seuil.planMaintenanceId) {
    selectedExistingPMId.value = props.seuil.planMaintenanceId;
  }
});

// Change detection
const detectedChanges = ref({});
const hasChanges = computed(() => Object.keys(detectedChanges.value).length > 0);

const detectChanges = () => {
  const changes = {};
  
  if (!props.seuil || !isEditMode.value) return changes;

  if (pmMode.value === 'existing') {
    if (selectedExistingPMId.value !== props.seuil.planMaintenanceId) {
      changes['planMaintenanceId'] = {
        ancienne: props.seuil.planMaintenanceId,
        nouvelle: selectedExistingPMId.value,
      };
    }
  }

  detectedChanges.value = changes;
  return changes;
};

// Watch for changes
watch(() => [pmMode.value, selectedExistingPMId.value, currentPlan.value], () => {
  if (isEditMode.value) {
    detectChanges();
  }
}, { deep: true });

const handlePlanSave = () => {
  // Le plan est déjà à jour dans currentPlan via v-model
  // On appelle juste handleSubmit
  handleSubmit();
};

const handleSubmit = async () => {
  try {
    loading.value = true;

    let dataToSubmit;

    if (pmMode.value === 'existing') {
      // Mode PM existant
      dataToSubmit = {
        compteurId: props.compteurId,
        equipmentId: props.equipmentId,
        planMaintenanceId: selectedExistingPMId.value,
        // Seuil avec valeurs par défaut si PM existant
        seuil: {
          derniereIntervention: 0,
          ecartInterventions: 100,
          prochaineMaintenance: 100,
          estGlissant: false
        }
      };
    } else {
      // Mode nouveau PM
      dataToSubmit = {
        compteurId: props.compteurId,
        equipmentId: props.equipmentId,
        planMaintenance: {
          nom: currentPlan.value.nom,
          type_id: currentPlan.value.type_id,
          description: currentPlan.value.description,
          consommables: currentPlan.value.consommables,
          necessiteHabilitationElectrique: currentPlan.value.necessiteHabilitationElectrique,
          necessitePermisFeu: currentPlan.value.necessitePermisFeu
        },
        seuil: currentPlan.value.seuil
      };
    }

    emit("submit", { ...dataToSubmit, pmMode: pmMode.value });
  } catch (error) {
    console.error("Erreur lors de la sauvegarde du seuil:", error);
    throw error;
  } finally {
    loading.value = false;
  }
};

const handleCancel = () => {
  emit("cancel");
};
</script>

<style scoped>
.text-decoration-line-through {
  text-decoration: line-through;
}
</style>