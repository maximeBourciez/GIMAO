<template>
  <v-form @submit.prevent="handleSave">
    <!-- Section: Configuration des seuils -->
    <div v-if="!hideSeuilSection">
      <h4 class="mb-3 text-body-1 font-weight-bold">
        <v-icon left color="primary" size="small">mdi-gauge</v-icon>
        Configuration du seuil
      </h4>
      <v-row dense>
        <v-col cols="12" md="6">
          <FormSelect
            v-model="plan.compteurIndex"
            field-name="compteurIndex"
            label="Compteur associé"
            :items="countersForSelect"
            item-title="label"
            item-value="value"
          >
            <template #item="{ props, item }">
              <v-list-item v-bind="props">
                <template #prepend>
                  <v-icon :color="item.raw.isPrincipal ? 'primary' : 'grey'">
                    mdi-{{ item.raw.isPrincipal ? "star" : "counter" }}
                  </v-icon>
                </template>
                <v-list-item-title>
                  {{ item.raw.label }}
                  <span v-if="item.raw.isPrincipal" class="text-caption text-primary ml-1"
                    >(Principal)</span
                  >
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ item.raw.currentValue }} {{ item.raw.unit }}
                </v-list-item-subtitle>
              </v-list-item>
            </template>
          </FormSelect>
        </v-col>

        <v-col cols="12" md="6">
          <FormField
            :model-value="selectedCounterValue"
            field-name="valeurCompteur"
            label="Valeur du compteur"
            :readonly="true"
            :suffix="selectedCounterType === 'Calendaire' ? '': selectedCounterUnit"
          />
        </v-col>

        <v-col cols="12" md="4">
          <FormField
            v-model="plan.seuil.derniereIntervention"
            field-name="derniereIntervention"
            :type="selectedCounterType === 'Calendaire' ? 'date' : 'number'"
            label="Dernière intervention"
            placeholder="0"
            min="0"
            @update:model-value="updateProchaineMaintenance"
          />
        </v-col>

        <v-col cols="12" md="4" v-if="selectedCounterType !== 'Calendaire'">
          <FormField
            v-model="plan.seuil.ecartInterventions"
            field-name="ecartInterventions"
            type="number"
            label="Écart entre interventions"
            placeholder="0"
            min="0"
            @update:model-value="updateProchaineMaintenance"
          />
        </v-col>

        <v-col cols="12" md="4" v-else>
          <v-row dense>
            <v-col cols="4">
              <FormField
                v-model="ecartCalendaire"
                field-name="ecartInterventions"
                type="number"
                label="Écart"
                placeholder="0"
                min="0"
                @update:model-value="updateProchaineMaintenance"
              />
            </v-col>
            <v-col cols="8">
              <FormSelect
                v-model="uniteCalendaire"
                field-name="uniteIntervalle"
                label="Unité"
                :items="[
                  { label: 'Heures', value: 'hours' },
                  { label: 'Jours', value: 'days' },
                  { label: 'Semaines', value: 'weeks' },
                  { label: 'Mois', value: 'months' },
                  { label: 'Années', value: 'years' },
                ]"
                item-title="label"
                item-value="value"
                @update:model-value="updateProchaineMaintenance"
              />
            </v-col>
          </v-row>
        </v-col>

        <v-col cols="12" md="4">
          <FormField
            v-model="plan.seuil.prochaineMaintenance"
            field-name="prochaineMaintenance"
            :type="selectedCounterType === 'Calendaire' ? 'date' : 'number'"
            label="Prochaine maintenance"
            :readonly="true"
          />
        </v-col>

        <v-col cols="12" md="4">
          <FormCheckbox
            v-model="plan.seuil.estGlissant"
            field-name="estGlissant"
            label="Seuil glissant"
          />
        </v-col>
      </v-row>

      <v-divider class="my-4"></v-divider>
    </div>

    <!-- Sélection de PM existant ou création -->
    <div v-if="showPmSelection">
      <h4 class="mb-3 text-body-1 font-weight-bold">
        <v-icon left color="primary" size="small">mdi-clipboard-check</v-icon>
        Plan de maintenance
      </h4>
      <v-radio-group v-model="pmMode" inline hide-details class="mb-4">
        <v-radio label="Sélectionner un PM existant" value="existing"></v-radio>
        <v-radio label="Créer un nouveau PM" value="new"></v-radio>
      </v-radio-group>

      <v-divider class="my-4"></v-divider>
    </div>

    <!-- Sélection PM existant -->
    <div v-if="showPmSelection && pmMode === 'existing'">
      <v-row dense>
        <v-col cols="12">
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
                <template #subtitle>{{
                  getPMTypeLabel(item.raw.type_id ?? item.raw.type)
                }}</template>
              </v-list-item>
            </template>
          </v-select>
        </v-col>
      </v-row>

      <!-- Aperçu du PM sélectionné -->
      <v-alert v-if="selectedExistingPM" type="info" class="mt-4" variant="tonal">
        <div class="text-subtitle-2 font-weight-bold mb-2">
          <v-icon left size="small">mdi-information</v-icon>
          Aperçu du plan sélectionné
        </div>
        <v-row dense class="mb-2">
          <v-col cols="12" md="6">
            <div class="text-caption">Nom du plan</div>
            <div class="font-weight-medium">{{ selectedExistingPM.nom }}</div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="text-caption">Type de maintenance</div>
            <div class="font-weight-medium">
              {{ getPMTypeLabel(selectedExistingPM.type_id) }}
            </div>
          </v-col>
        </v-row>
        <div
          v-if="selectedExistingPM.description || selectedExistingPM.commentaire"
          class="mt-2"
        >
          <div class="text-caption">Commentaire</div>
          <div>
            {{ selectedExistingPM.description || selectedExistingPM.commentaire }}
          </div>
        </div>
        <div
          v-if="
            selectedExistingPM.necessiteHabilitationElectrique ||
            selectedExistingPM.necessitePermisFeu
          "
          class="mt-2"
        >
          <div class="text-caption mb-1">Habilitations requises</div>
          <v-chip
            v-if="selectedExistingPM.necessiteHabilitationElectrique"
            size="small"
            color="orange"
            class="mr-2"
          >
            <v-icon left size="small">mdi-flash</v-icon>
            Habilitation électrique
          </v-chip>
          <v-chip v-if="selectedExistingPM.necessitePermisFeu" size="small" color="red">
            <v-icon left size="small">mdi-fire</v-icon>
            Permis feu
          </v-chip>
        </div>
      </v-alert>
    </div>

    <!-- Section: Plan de maintenance (nouveau) -->
    <div v-if="!showPmSelection || pmMode === 'new'">
      <h4 class="mb-3 text-body-1 font-weight-bold">
        <v-icon left color="primary" size="small">mdi-clipboard-check</v-icon>
        Informations du plan de maintenance
      </h4>
      <v-row dense>
        <v-col cols="12" md="6">
          <FormField
            v-model="plan.nom"
            field-name="nom"
            label="Nom du plan"
            placeholder="Saisir le nom du plan"
            counter="100"
          />
        </v-col>

        <v-col cols="12" md="6">
          <FormSelect
            v-model="plan.type_id"
            field-name="type_id"
            label="Type de maintenance"
            :items="typesPM"
            item-title="libelle"
            item-value="id"
          />
        </v-col>

        <v-col cols="12">
          <FormField
            v-model="plan.description"
            field-name="description"
            label="Description"
            type="textarea"
            rows="2"
            placeholder="Description du plan de maintenance"
          />
        </v-col>
      </v-row>

      <v-divider class="my-4"></v-divider>

      <!-- Section: Consommables -->
      <h4 class="mb-3 text-body-1 font-weight-bold">
        <v-icon left color="primary" size="small">mdi-package-variant</v-icon>
        Consommables nécessaires
      </h4>

      <v-row
        v-for="(conso, index) in plan.consommables"
        :key="index"
        dense
        class="mb-2 align-center"
      >
        <v-col cols="12" md="6">
          <v-select
            v-model="conso.consommable_id"
            :items="consumables"
            item-title="designation"
            item-value="id"
            label="Consommable"
            variant="outlined"
            density="comfortable"
            hide-details
          ></v-select>
        </v-col>
        <v-col cols="12" md="5">
          <v-text-field
            v-model="conso.quantite_necessaire"
            type="number"
            label="Quantité nécessaire"
            variant="outlined"
            density="comfortable"
            hide-details
            min="1"
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="1" class="text-right">
          <v-btn
            icon
            size="small"
            color="error"
            variant="text"
            @click="removeConsommable(index)"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-col>
      </v-row>

      <v-row dense>
        <v-col cols="12">
          <v-btn variant="outlined" color="primary" size="small" @click="addConsommable">
            <v-icon left>mdi-plus</v-icon>
            Ajouter un consommable
          </v-btn>
        </v-col>
      </v-row>

      <v-divider class="my-4"></v-divider>

      <!-- Section: Documents -->
      <h4 class="mb-3 text-body-1 font-weight-bold">
        <v-icon left color="primary" size="small">mdi-file-document</v-icon>
        Documents associés
      </h4>

      <v-row
        v-for="(doc, index) in plan.documents"
        :key="index"
        dense
        class="mb-2 align-center"
      >
        <v-col cols="12" md="5">
          <v-text-field
            v-model="doc.nom"
            label="Nom du document"
            variant="outlined"
            density="comfortable"
            hide-details
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            v-model="doc.type_id"
            :items="typesDocuments"
            item-title="nomTypeDocument"
            item-value="id"
            label="Type de document"
            variant="outlined"
            density="comfortable"
            hide-details
          ></v-select>
        </v-col>
        <v-col cols="12" md="3">
          <v-file-input
            v-model="doc.file"
            label="Fichier"
            variant="outlined"
            density="comfortable"
            hide-details
            prepend-icon=""
            prepend-inner-icon="mdi-paperclip"
            :show-size="true"
          ></v-file-input>
        </v-col>
        <v-col cols="12" md="1" class="text-right">
          <v-btn
            icon
            size="small"
            color="error"
            variant="text"
            @click="removeDocument(index)"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-col>
      </v-row>

      <v-row dense>
        <v-col cols="12">
          <v-btn variant="outlined" color="primary" size="small" @click="addDocument">
            <v-icon left>mdi-plus</v-icon>
            Ajouter un document
          </v-btn>
        </v-col>
      </v-row>

      <v-divider class="my-4"></v-divider>

      <!-- Section: Habilitations -->
      <h4 class="mb-3 text-body-1 font-weight-bold">
        <v-icon left color="primary" size="small">mdi-shield-account</v-icon>
        Habilitations requises
      </h4>
      <v-row dense>
        <v-col cols="12" md="6">
          <FormCheckbox
            v-model="plan.necessiteHabilitationElectrique"
            field-name="necessiteHabilitationElectrique"
            label="Habilitation électrique requise"
            color="orange"
          />
        </v-col>

        <v-col cols="12" md="6">
          <FormCheckbox
            v-model="plan.necessitePermisFeu"
            field-name="necessitePermisFeu"
            label="Permis feu requis"
            color="red"
          />
        </v-col>
      </v-row>
    </div>

    <v-alert v-if="localError" type="error" class="mt-4">{{ localError }}</v-alert>

    <v-card-actions v-if="showActions" class="px-0 pt-4">
      <v-spacer />
      <v-btn variant="text" @click="handleCancel">Annuler</v-btn>
      <v-btn type="submit" color="primary" :disabled="!isValid">
        {{ isEditMode ? "Modifier le plan" : "Ajouter le plan" }}
      </v-btn>
    </v-card-actions>
  </v-form>
</template>

<script setup>
import { computed, ref, watch, onMounted } from "vue";
import { FormField, FormCheckbox, FormSelect } from "@/components/common";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
  isEditMode: {
    type: Boolean,
    default: false,
  },
  showActions: {
    type: Boolean,
    default: true,
  },
  hideSeuilSection: {
    type: Boolean,
    default: false,
  },
  showPmSelection: {
    type: Boolean,
    default: false,
  },
  existingPMs: {
    type: Array,
    default: () => [],
  },
  counters: {
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
});

const emit = defineEmits(["update:modelValue", "save", "cancel"]);

const localError = ref("");
const pmMode = ref("new");
const selectedExistingPMId = ref(null);

// VAriables pour les compteurs calendaires
const ecartCalendaire = ref(0);
const uniteCalendaire = ref("days");

const plan = computed({
  get: () => props.modelValue,
  set: (v) => emit("update:modelValue", v),
});

// Transformer les compteurs pour le select
const countersForSelect = computed(() => {
  return props.counters.map((counter, index) => ({
    value: index,
    label: counter.nom,
    isPrincipal: counter.estPrincipal,
    currentValue: counter.valeurCourante,
    unit: counter.unite,
  }));
});

// Valeur et unité du compteur sélectionné
const selectedCounterValue = computed(() => {
  if (plan.value.compteurIndex === null || plan.value.compteurIndex === undefined)
    return "—";
  const counter = props.counters[plan.value.compteurIndex];
  return counter?.valeurCourante ?? "—";
});

const selectedCounterUnit = computed(() => {
  if (plan.value.compteurIndex === null || plan.value.compteurIndex === undefined)
    return "";
  const counter = props.counters[plan.value.compteurIndex];
  return counter?.unite ?? "";
});

const selectedCounterType = computed(() => {
  if (plan.value.compteurIndex === null || plan.value.compteurIndex === undefined)
    return "";
  const counter = props.counters[plan.value.compteurIndex];
  console.log("Selected counter index:", plan.value.compteurIndex);
  console.log("Counter found:", counter);
  console.log("Selected counter type:", counter?.type);
  return counter?.type ?? "";
});

const selectedExistingPM = computed(() =>
  props.existingPMs.find((pm) => pm.id === selectedExistingPMId.value)
);

const getPMTypeLabel = (typeId) => {
  const type = props.typesPM.find((t) => t.id === typeId);
  return type ? type.libelle : "Non spécifié";
};

const isValid = computed(() => {
  // Vérifier d'abord que le seuil est valide
  const seuilValid = Number(plan.value.seuil?.ecartInterventions) > 0;

  if (!seuilValid) return false;

  if (props.showPmSelection && pmMode.value === "existing") {
    return (
      !!selectedExistingPMId.value &&
      plan.value.compteurIndex !== null &&
      plan.value.compteurIndex !== undefined
    );
  }

  return (
    plan.value.nom &&
    plan.value.nom.trim() !== "" &&
    plan.value.type_id !== null &&
    plan.value.compteurIndex !== null &&
    plan.value.compteurIndex !== undefined
  );
});

const applyExistingPMToPlan = (pm) => {
  if (!pm) return;

  plan.value = {
    ...plan.value,
    nom: pm.nom ?? plan.value.nom,
    type_id: pm.type_id ?? pm.type ?? plan.value.type_id,
    description: pm.description ?? pm.commentaire ?? plan.value.description,
    necessiteHabilitationElectrique: !!pm.necessiteHabilitationElectrique,
    necessitePermisFeu: !!pm.necessitePermisFeu,
    consommables: Array.isArray(pm.consommables)
      ? pm.consommables.map((c) => ({ ...c }))
      : [],
    documents: Array.isArray(pm.documents) ? pm.documents.map((d) => ({ ...d })) : [],
  };
};

watch(pmMode, (mode) => {
  localError.value = "";
  if (mode !== "existing") {
    selectedExistingPMId.value = null;
    return;
  }
  if (selectedExistingPM.value) {
    applyExistingPMToPlan(selectedExistingPM.value);
  }
});

watch(selectedExistingPMId, () => {
  localError.value = "";
  if (!props.showPmSelection) return;
  if (pmMode.value !== "existing") return;
  if (!selectedExistingPM.value) return;
  applyExistingPMToPlan(selectedExistingPM.value);
});

// Calcul automatique de la prochaine maintenance
const updateProchaineMaintenance = () => {
  if (selectedCounterType.value === "Calendaire") {
    const derniere = plan.value.seuil.derniereIntervention;
    const ecart = Number(ecartCalendaire.value || 0);
    const unite = uniteCalendaire.value;

    if (!derniere || !ecart || !unite) {
      plan.value.seuil.prochaineMaintenance = "";
      return;
    }

    const dateDerniere = new Date(derniere);
    let prochaineDate = new Date(dateDerniere);

    switch (unite) {
      case "days":
        prochaineDate.setDate(prochaineDate.getDate() + ecart);
        break;
      case "weeks":
        prochaineDate.setDate(prochaineDate.getDate() + ecart * 7);
        break;
      case "months":
        prochaineDate.setMonth(prochaineDate.getMonth() + ecart);
        break;
      case "years":
        prochaineDate.setFullYear(prochaineDate.getFullYear() + ecart);
        break;
      default:
        plan.value.seuil.prochaineMaintenance = "";
        return;
    }

    plan.value.seuil.prochaineMaintenance = prochaineDate.toISOString().split("T")[0];

    // Stocker le delta en timestamp
    plan.value.seuil.ecartInterventions = prochaineDate.getTime() - dateDerniere.getTime();

  } else {
    // Cas non calendaire
    const derniere = Number(plan.value.seuil.derniereIntervention);
    const ecart = Number(plan.value.seuil.ecartInterventions);
    if (isNaN(derniere) || isNaN(ecart)) {
      plan.value.seuil.prochaineMaintenance = "";
      return;
    }
    plan.value.seuil.prochaineMaintenance = derniere + ecart;
  }
};


// Gestion des consommables
const addConsommable = () => {
  if (!plan.value.consommables) {
    plan.value.consommables = [];
  }
  plan.value.consommables.push({
    consommable_id: null,
    quantite_necessaire: 1,
  });
};

const removeConsommable = (index) => {
  plan.value.consommables.splice(index, 1);
};

// Gestion des documents
const addDocument = () => {
  if (!plan.value.documents) {
    plan.value.documents = [];
  }
  plan.value.documents.push({
    nom: "",
    type_id: null,
    file: null,
  });
};

const removeDocument = (index) => {
  plan.value.documents.splice(index, 1);
};

const handleSave = () => {
  if (!isValid.value) {
    localError.value =
      "Veuillez remplir tous les champs obligatoires (nom, type et compteur)";
    return;
  }
  localError.value = "";
  emit("save", {
    pmMode: pmMode.value,
    selectedExistingPMId: selectedExistingPMId.value,
  });
};

const handleCancel = () => {
  localError.value = "";
  emit("cancel");
};

// Fonction utilitaire
const ordinalToISOString = (ordinal) => {
  if (!ordinal && ordinal !== 0) return null;
  
  const ORDINAL_EPOCH = 719162; // 1970-01-01
  const daysFromEpoch = ordinal - ORDINAL_EPOCH;
  const date = new Date(Date.UTC(1970, 0, 1 + daysFromEpoch));
  
  return date.toISOString().split('T')[0]; // "YYYY-MM-DD"
};

onMounted(() => {
  if (props.isEditMode && plan.value.seuil) {
    if (selectedCounterType.value === "Calendaire") {
      
      // Convertir derniereIntervention (ordinal → ISO string)
      if (plan.value.seuil.derniereIntervention) {
        plan.value.seuil.derniereIntervention = ordinalToISOString(
          plan.value.seuil.derniereIntervention
        );
      }
      
      // Convertir prochaineMaintenance aussi
      if (plan.value.seuil.prochaineMaintenance) {
        plan.value.seuil.prochaineMaintenance = ordinalToISOString(
          plan.value.seuil.prochaineMaintenance
        );
      }
      
      // Calculer ecartCalendaire depuis ecartInterventions (MS)
      const intervalle = Number(plan.value.seuil.ecartInterventions);
      if (!isNaN(intervalle) && intervalle > 0) {
        const days = Math.round(intervalle / (1000 * 60 * 60 * 24));
        
        // Choisir l'unité appropriée
        if (days < 7) {
          ecartCalendaire.value = days;
          uniteCalendaire.value = "days";
        } else if (days < 60) {
          ecartCalendaire.value = Math.round(days / 7);
          uniteCalendaire.value = "weeks";
        } else if (days < 365) {
          ecartCalendaire.value = Math.round(days / 30);
          uniteCalendaire.value = "months";
        } else {
          ecartCalendaire.value = Math.round(days / 365);
          uniteCalendaire.value = "years";
        }
      }
    }
  }
});
</script>
