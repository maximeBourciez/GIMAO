<template>
  <BaseForm :title="formTitle" :loading="loading" @submit="handleSubmit" @cancel="handleCancel" :max-width="1200">
    <v-container fluid class="px-0">
      <!-- Section Seuil -->
      <v-card class="mb-6" variant="outlined">
        <v-card-title class="d-flex align-center mb-2">
          <v-icon left>mdi-calendar-clock</v-icon>
          <span>Paramètres du seuil</span>
        </v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col cols="12" md="4">
              <v-text-field v-model.number="form.derniereIntervention" label="Dernière intervention" variant="outlined"
                density="compact" type="number" :rules="[rules.required, rules.positive]" />
            </v-col>



            <v-col cols="12" md="4">
              <v-text-field v-model.number="form.ecartInterventions" label="Intervalle entre interventions"
                variant="outlined" density="compact" type="number" :rules="[rules.required, rules.positive]" />
            </v-col>

            <v-col cols="12" md="4">
              <v-text-field v-model.number="form.prochaineMaintenance" label="Prochaine maintenance" variant="outlined"
                density="compact" type="number" :rules="[rules.required, rules.positive]" />
            </v-col>
          </v-row>

          <v-row dense>
            <v-col cols="12" md="6">
              <v-switch v-model="form.estGlissant" label="Seuil glissant" color="primary" hide-details>
                <template v-slot:label>
                  <div class="d-flex align-center">
                    <v-icon :color="form.estGlissant ? 'green' : 'grey'" class="mr-2">
                      {{ form.estGlissant ? 'mdi-check-circle' : 'mdi-close-circle' }}
                    </v-icon>
                    <span>Seuil glissant</span>
                  </div>
                </template>
              </v-switch>
            </v-col>

            <v-col cols="12" md="6" class="d-flex align-center">
              <div class="text-body-2 text-grey">
                Un seuil glissant se recalcule après chaque intervention
              </div>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Section Plan de Maintenance -->
      <v-card class="mb-6" variant="outlined">
        <v-card-title class="d-flex align-center mb-2">
          <v-icon left>mdi-clipboard-check</v-icon>
          <span>Plan de maintenance</span>
        </v-card-title>
        <v-card-text>
          <!-- Sélection de PM existant ou création -->
          <v-row dense class="mb-4">
            <v-col cols="12">
              <v-radio-group v-model="pmMode" inline hide-details>
                <v-radio label="Sélectionner un PM existant" value="existing"></v-radio>
                <v-radio label="Créer un nouveau PM" value="new"></v-radio>
              </v-radio-group>
            </v-col>
          </v-row>

          <!-- Sélection PM existant -->
          <div v-if="pmMode === 'existing'">
            <v-select v-model="form.planMaintenanceId" :items="existingPMs" item-title="nom" item-value="id"
              label="Sélectionner un plan de maintenance" variant="outlined" density="compact" :rules="[rules.required]"
              clearable />

            <!-- Aperçu du PM sélectionné -->
            <v-card v-if="selectedExistingPM" class="mt-4" variant="tonal">
              <v-card-text>
                <v-row dense>
                  <v-col cols="12" md="6">
                    <strong>Nom :</strong> {{ selectedExistingPM.nom }}
                  </v-col>
                  <v-col cols="12" md="6">
                    <strong>Type :</strong> {{ getPMTypeLabel(selectedExistingPM.type_id) }}
                  </v-col>
                </v-row>
                <v-row dense v-if="selectedExistingPM.commentaire">
                  <v-col cols="12">
                    <strong>Commentaire :</strong> {{ selectedExistingPM.commentaire }}
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </div>

          <!-- Création d'un nouveau PM -->
          <div v-else>
            <v-row dense>
              <v-col cols="12" md="6">
                <v-text-field v-model="form.planMaintenance.nom" label="Nom du plan de maintenance" variant="outlined"
                  density="compact" :rules="[rules.required]" />
              </v-col>

              <v-col cols="12" md="6">
                <v-select v-model="form.planMaintenance.type_id" :items="typesPM" item-title="libelle" item-value="id"
                  label="Type de maintenance" variant="outlined" density="compact" :rules="[rules.required]" />
              </v-col>
            </v-row>

            <v-row dense>
              <v-col cols="12">
                <v-textarea v-model="form.planMaintenance.commentaire" label="Commentaire" variant="outlined"
                  density="compact" rows="2" />
              </v-col>
            </v-row>

            <v-row dense>
              <v-col cols="12" md="6">
                <v-switch v-model="form.planMaintenance.necessiteHabilitationElectrique"
                  label="Habilitation électrique requise" color="orange" hide-details />
              </v-col>

              <v-col cols="12" md="6">
                <v-switch v-model="form.planMaintenance.necessitePermisFeu" label="Permis feu requis" color="red"
                  hide-details />
              </v-col>
            </v-row>

            <!-- Consommables -->
            <v-card class="mt-4" variant="outlined">
              <v-card-title class="d-flex align-center">
                <v-icon left>mdi-package-variant</v-icon>
                <span>Consommables nécessaires</span>
              </v-card-title>
              <v-card-text>
                <div v-if="!form.planMaintenance.consommables?.length" class="text-grey text-center py-4">
                  Aucun consommable ajouté
                </div>

                <v-row v-for="(consommable, index) in form.planMaintenance.consommables" :key="index" dense
                  align="center" class="mb-2">
                  <v-col cols="7">
                    <v-select v-model="consommable.consommable_id" :items="consumables" item-title="designation"
                      item-value="id" label="Consommable" variant="outlined" density="compact"
                      :rules="[rules.required]" />
                  </v-col>

                  <v-col cols="3">
                    <v-text-field v-model.number="consommable.quantite" label="Quantité" variant="outlined"
                      density="compact" type="number" :rules="[rules.required, rules.positive]" />
                  </v-col>

                  <v-col cols="2" class="text-right">
                    <v-btn icon color="red" size="small" @click="removeConsommable(index)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>

                <v-btn color="primary" variant="outlined" size="small" @click="addConsommable" class="mt-2">
                  <v-icon left>mdi-plus</v-icon>
                  Ajouter un consommable
                </v-btn>
              </v-card-text>
            </v-card>

            <!-- Documents -->
            <v-card class="mt-4" variant="outlined">
              <v-card-title class="d-flex align-center">
                <v-icon left>mdi-file-document</v-icon>
                <span>Documents associés</span>
              </v-card-title>
              <v-card-text>
                <div v-if="!form.planMaintenance.documents?.length" class="text-grey text-center py-4">
                  Aucun document ajouté
                </div>

                <v-row v-for="(document, index) in form.planMaintenance.documents" :key="index" dense align="center"
                  class="mb-4">
                  <v-col cols="12" md="4">
                    <v-text-field v-model="document.nomDocument" label="Nom du document" variant="outlined"
                      density="compact" :rules="[rules.required]" />
                  </v-col>

                  <v-col cols="12" md="4">
                    <v-select v-model="document.typeDocument_id" :items="typesDocuments" item-title="nomTypeDocument"
                      item-value="id" label="Type de document" variant="outlined" density="compact"
                      :rules="[rules.required]" />
                  </v-col>

                  <v-col cols="12" md="3">
                    <v-file-input v-model="document.file" label="Fichier" variant="outlined" density="compact"
                      :show-size="true" :rules="[rules.requiredIfNew(document.id)]"
                      accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png" />

                    <!-- Aperçu du fichier existant -->
                    <div v-if="document.cheminAcces && !document.file" class="text-body-2 text-grey mt-1">
                      Fichier actuel : {{ getFileName(document.cheminAcces) }}
                    </div>
                  </v-col>

                  <v-col cols="12" md="1" class="text-right">
                    <v-btn icon color="red" size="small" @click="removeDocument(index)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>

                <v-btn color="primary" variant="outlined" size="small" @click="addDocument" class="mt-2">
                  <v-icon left>mdi-plus</v-icon>
                  Ajouter un document
                </v-btn>
              </v-card-text>
            </v-card>
          </div>
        </v-card-text>
      </v-card>

      <!-- Section Changements détectés -->
      <v-card v-if="hasChanges && isEditMode" variant="outlined" class="mb-6">
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
    </v-container>
  </BaseForm>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useApi } from "@/composables/useApi";
import { useStore } from "vuex";
import { API_BASE_URL } from "@/utils/constants";
import BaseForm from "@/components/common/BaseForm.vue";

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

const api = useApi(API_BASE_URL);
const store = useStore();

// Form data structure
const form = ref({
  id: null,
  derniereIntervention: 0,
  prochaineMaintenance: 0,
  ecartInterventions: 0,
  estGlissant: false,
  planMaintenanceId: null,
  planMaintenance: {
    id: null,
    nom: "",
    commentaire: "",
    type_id: null,
    necessiteHabilitationElectrique: false,
    necessitePermisFeu: false,
    consommables: [],
    documents: [],
  },
});

// Rules
const rules = {
  required: (v) => !!v || "Ce champ est requis",
  requiredIfNew: (hasId) => (v) => !hasId ? !!v || "Un fichier est requis pour un nouveau document" : true,
  positive: (v) => v >= 0 || "La valeur doit être positive",
};

// Computed properties
const formTitle = computed(() =>
  props.isEdit ? `Modifier le seuil` : `Ajouter un nouveau seuil`
);

const isEditMode = computed(() => props.isEdit);

const selectedExistingPM = computed(() =>
  props.existingPMs.find(pm => pm.id === form.value.planMaintenanceId)
);

const getPMTypeLabel = (typeId) => {
  const type = props.typesPM.find(t => t.id === typeId);
  return type ? type.libelle : "Non spécifié";
};

const getFileName = (path) => path?.split('/').pop() || "Fichier";

const getFieldLabel = (field) => {
  const labels = {
    'derniereIntervention': 'Dernière intervention',
    'prochaineMaintenance': 'Prochaine maintenance',
    'ecartInterventions': 'Intervalle',
    'estGlissant': 'Seuil glissant',
    'planMaintenanceId': 'Plan de maintenance',
    'planMaintenance.nom': 'Nom du PM',
    'planMaintenance.type_id': 'Type de PM',
    'planMaintenance.commentaire': 'Commentaire PM',
    'planMaintenance.necessiteHabilitationElectrique': 'Habilitation électrique',
    'planMaintenance.necessitePermisFeu': 'Permis feu',
  };
  return labels[field] || field;
};

const formatChangeValue = (value) => {
  if (value === null || value === undefined) return "—";
  if (typeof value === 'boolean') return value ? "Oui" : "Non";
  return String(value);
};

// Initialize form
onMounted(() => {
  if (props.seuil) {
    form.value = {
      id: props.seuil.id || null,
      derniereIntervention: props.seuil.derniereIntervention || 0,
      prochaineMaintenance: props.seuil.prochaineMaintenance || 0,
      ecartInterventions: props.seuil.ecartInterventions || 0,
      estGlissant: props.seuil.estGlissant || false,
      planMaintenanceId: props.seuil.planMaintenanceId || null,
      planMaintenance: props.seuil.planMaintenance ? {
        id: props.seuil.planMaintenance.id,
        nom: props.seuil.planMaintenance.nom || "",
        commentaire: props.seuil.planMaintenance.commentaire || "",
        type_id: props.seuil.planMaintenance.type_id || null,
        necessiteHabilitationElectrique: props.seuil.planMaintenance.necessiteHabilitationElectrique || false,
        necessitePermisFeu: props.seuil.planMaintenance.necessitePermisFeu || false,
        consommables: props.seuil.planMaintenance.consommables?.map(c => ({
          consommable_id: c.id,
          quantite: c.quantite || 1,
          designation: c.designation,
        })) || [],
        documents: props.seuil.planMaintenance.documents?.map(d => ({
          id: d.id,
          nomDocument: d.nom || d.titre || "",
          typeDocument_id: d.type || d.typeDocument_id,
          cheminAcces: d.chemin || d.path || "",
          file: null,
        })) || [],
      } : {
        id: null,
        nom: "",
        commentaire: "",
        type_id: null,
        necessiteHabilitationElectrique: false,
        necessitePermisFeu: false,
        consommables: [],
        documents: [],
      },
    };
  }

  console.log("Datas : ", {
    existingPMs: props.existingPMs,
    typesPM: props.typesPM,
    consumables: props.consumables,
    typesDocuments: props.typesDocuments,
  });
});

// Methods for managing consumables and documents
const addConsommable = () => {
  form.value.planMaintenance.consommables.push({
    consommable_id: null,
    quantite: 1,
    designation: "",
  });
};

const removeConsommable = (index) => {
  form.value.planMaintenance.consommables.splice(index, 1);
};

const addDocument = () => {
  form.value.planMaintenance.documents.push({
    id: null,
    nomDocument: "",
    typeDocument_id: null,
    cheminAcces: "",
    file: null,
  });
};

const removeDocument = (index) => {
  form.value.planMaintenance.documents.splice(index, 1);
};

// Change detection
const detectedChanges = ref({});
const hasChanges = computed(() => Object.keys(detectedChanges.value).length > 0);

const detectChanges = () => {
  const changes = {};
  const original = props.seuil;

  if (!original) return changes;

  // Check basic seuil fields
  const basicFields = ['derniereIntervention', 'prochaineMaintenance', 'ecartInterventions', 'estGlissant', 'planMaintenanceId'];
  basicFields.forEach(field => {
    if (form.value[field] !== original[field]) {
      changes[field] = {
        ancienne: original[field],
        nouvelle: form.value[field],
      };
    }
  });

  // Check if using new PM vs existing PM
  if (pmMode.value === 'existing') {
    if (form.value.planMaintenanceId !== original.planMaintenanceId) {
      changes['planMaintenanceId'] = {
        ancienne: original.planMaintenanceId,
        nouvelle: form.value.planMaintenanceId,
      };
    }
  } else {
    // Check PM fields if creating/updating a new PM
    const originalPM = original.planMaintenance || {};
    const newPM = form.value.planMaintenance;

    const pmFields = ['nom', 'type_id', 'commentaire', 'necessiteHabilitationElectrique', 'necessitePermisFeu'];
    pmFields.forEach(field => {
      if (newPM[field] !== originalPM[field]) {
        changes[`planMaintenance.${field}`] = {
          ancienne: originalPM[field],
          nouvelle: newPM[field],
        };
      }
    });

    // Check consumables
    const originalConsommables = JSON.stringify(originalPM.consommables || []);
    const newConsommables = JSON.stringify(newPM.consommables || []);
    if (originalConsommables !== newConsommables) {
      changes['planMaintenance.consommables'] = {
        ancienne: originalPM.consommables || [],
        nouvelle: newPM.consommables || [],
      };
    }

    // Check documents
    const originalDocs = originalPM.documents || [];
    const newDocs = newPM.documents || [];

    if (JSON.stringify(originalDocs.map(d => ({ ...d, file: null }))) !==
      JSON.stringify(newDocs.map(d => ({ nomDocument: d.nomDocument, typeDocument_id: d.typeDocument_id })))) {

      changes['planMaintenance.documents'] = {
        ancienne: originalDocs,
        nouvelle: newDocs.map(d => ({
          nomDocument: d.nomDocument,
          typeDocument_id: d.typeDocument_id,
          fileChanged: !!d.file,
        })),
      };
    }
  }

  detectedChanges.value = changes;
  return changes;
};

// Watch for changes
watch(() => form.value, () => {
  if (isEditMode.value) {
    detectChanges();
  }
}, { deep: true });

const handleSubmit = async () => {
  try {
    loading.value = true;

    const data = {
      ...form.value,
      user: store.getters.currentUser?.id,
      compteurId: props.compteurId, // Ajout ici
      equipmentId: props.equipmentId, // Ajout ici aussi pour cohérence
    };

    // Remove the nested PM if using existing PM
    if (pmMode.value === 'existing') {
      delete data.planMaintenance;
    } else {
      // For new PM, keep only the PM ID if editing existing PM
      if (data.planMaintenance?.id) {
        data.planMaintenanceId = data.planMaintenance.id;
      }
    }

    // Prepare FormData for file uploads
    const formData = new FormData();
    formData.append('seuil', JSON.stringify(data));

    // Add files to FormData
    if (pmMode.value === 'new' && data.planMaintenance?.documents) {
      data.planMaintenance.documents.forEach((doc, index) => {
        if (doc.file) {
          formData.append(`document_${index}`, doc.file);
        }
      });
    }

    // Add changes if in edit mode
    if (isEditMode.value) {
      const changes = detectChanges();
      formData.append('changes', JSON.stringify(changes));
    }

    if (isEditMode.value && data.id) {
      await api.put(`plans-maintenance/${data.id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
    } else {
      await api.post('plans-maintenance/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
    }

    emit("submit", { ...data, pmMode: pmMode.value });
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


watch(() => [form.value.derniereIntervention, form.value.ecartInterventions, form.value.estGlissant], () => {
  if (form.value.derniereIntervention >= 0 && form.value.ecartInterventions > 0) {
    form.value.prochaineMaintenance = form.value.derniereIntervention + form.value.ecartInterventions;
  }
}, { deep: true });

</script>

<style scoped>
.text-decoration-line-through {
  text-decoration: line-through;
}
</style>