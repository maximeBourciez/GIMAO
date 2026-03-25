<template>
  <v-row dense>
    <v-col cols="12" md="4">
      <FormField
        v-model="localSeuil.derniereIntervention"
        field-name="derniereIntervention"
        type="date"
        label="Dernière intervention"
        @update:model-value="updateProchaineMaintenance"
      />
    </v-col>

    <v-col cols="12" md="4">
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
            :items="UNITES"
            item-title="label"
            item-value="value"
            @update:model-value="updateProchaineMaintenance"
          />
        </v-col>
      </v-row>
    </v-col>

    <v-col cols="12" md="4">
      <FormField
        :model-value="localSeuil.prochaineMaintenance"
        field-name="prochaineMaintenance"
        type="date"
        label="Prochaine maintenance"
        :readonly="true"
      />
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from "vue";
import { FormField, FormSelect } from "@/components/common";

const UNITES = [
  { label: "Heures",   value: "hours"  },
  { label: "Jours",    value: "days"   },
  { label: "Semaines", value: "weeks"  },
  { label: "Mois",     value: "months" },
  { label: "Années",   value: "years"  },
];

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
    // {
    //   derniereIntervention : string ISO "YYYY-MM-DD" | number (ordinal)
    //   ecartInterventions   : number (delta ms, stocké pour le backend)
    //   prochaineMaintenance : string ISO "YYYY-MM-DD" | number (ordinal)
    // }
  },
});

const emit = defineEmits(["update:modelValue"]);

// --- Utilitaires date ---

const ordinalToISO = (ordinal) => {
  if (ordinal === null || ordinal === undefined) return null;
  const ORDINAL_EPOCH = 719162; // 1970-01-01
  const date = new Date(Date.UTC(1970, 0, 1 + (ordinal - ORDINAL_EPOCH)));
  return date.toISOString().split("T")[0];
};

const toISODate = (val) => {
  if (!val && val !== 0) return null;
  if (typeof val === "number") return ordinalToISO(val);
  return val; // déjà ISO string
};

// --- État local ---

const ecartCalendaire = ref(0);
const uniteCalendaire = ref("days");

const localSeuil = reactive({
  derniereIntervention: null,
  ecartInterventions:   0,
  prochaineMaintenance: null,
});

// --- Calcul ---

const updateProchaineMaintenance = () => {
  const derniere = localSeuil.derniereIntervention;
  const ecart    = Number(ecartCalendaire.value || 0);
  const unite    = uniteCalendaire.value;

  if (!derniere || !ecart || !unite) {
    localSeuil.prochaineMaintenance = "";
    localSeuil.ecartInterventions   = 0;
    emit("update:modelValue", { ...localSeuil });
    return;
  }

  const dateDerniere  = new Date(derniere);
  const prochaineDate = new Date(dateDerniere);

  switch (unite) {
    case "hours":   prochaineDate.setHours  (prochaineDate.getHours()   + ecart);       break;
    case "days":    prochaineDate.setDate   (prochaineDate.getDate()    + ecart);       break;
    case "weeks":   prochaineDate.setDate   (prochaineDate.getDate()    + ecart * 7);   break;
    case "months":  prochaineDate.setMonth  (prochaineDate.getMonth()   + ecart);       break;
    case "years":   prochaineDate.setFullYear(prochaineDate.getFullYear() + ecart);     break;
    default:
      localSeuil.prochaineMaintenance = "";
      emit("update:modelValue", { ...localSeuil });
      return;
  }

  localSeuil.prochaineMaintenance = prochaineDate.toISOString().split("T")[0];
  // Delta en ms pour le backend
  localSeuil.ecartInterventions   = prochaineDate.getTime() - dateDerniere.getTime();

  emit("update:modelValue", { ...localSeuil });
};

// --- Init depuis prop (conversion ordinal si besoin) ---

const initFromProp = (val) => {
  localSeuil.derniereIntervention = toISODate(val.derniereIntervention);
  localSeuil.prochaineMaintenance = toISODate(val.prochaineMaintenance);
  localSeuil.ecartInterventions   = val.ecartInterventions ?? 0;

  // Reconstituer ecartCalendaire + uniteCalendaire depuis le delta ms
  const intervalle = Number(val.ecartInterventions);
  if (!isNaN(intervalle) && intervalle > 0) {
    const days = Math.round(intervalle / (1000 * 60 * 60 * 24));
    if (days < 1) {
      ecartCalendaire.value = Math.round(intervalle / (1000 * 60 * 60));
      uniteCalendaire.value = "hours";
    } else if (days < 7) {
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
};

onMounted(() => initFromProp(props.modelValue));

// Sync si le parent pousse une mise à jour (rare mais possible en mode édition)
watch(() => props.modelValue, (val) => initFromProp(val), { deep: true });
</script>