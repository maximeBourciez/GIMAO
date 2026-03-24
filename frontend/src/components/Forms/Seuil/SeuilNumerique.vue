<template>
  <v-row dense>
    <v-col cols="12" md="4">
      <FormField
        v-model="localSeuil.derniereIntervention"
        field-name="derniereIntervention"
        type="number"
        label="Dernière intervention"
        placeholder="0"
        min="0"
        @update:model-value="updateProchaineMaintenance"
      />
    </v-col>

    <v-col cols="12" md="4">
      <FormField
        v-model="localSeuil.ecartInterventions"
        field-name="ecartInterventions"
        type="number"
        label="Écart entre interventions"
        placeholder="0"
        min="0"
        @update:model-value="updateProchaineMaintenance"
      />
    </v-col>

    <v-col cols="12" md="4">
      <FormField
        :model-value="localSeuil.prochaineMaintenance"
        field-name="prochaineMaintenance"
        type="number"
        label="Prochaine maintenance"
        :readonly="true"
      />
    </v-col>
  </v-row>
</template>

<script setup>
import { reactive, watch } from "vue";
import { FormField } from "@/components/common";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
    // { derniereIntervention: number, ecartInterventions: number, prochaineMaintenance: number }
  },
});

const emit = defineEmits(["update:modelValue"]);

// Copie locale pour éviter la mutation directe de la prop
const localSeuil = reactive({
  derniereIntervention: props.modelValue.derniereIntervention ?? 0,
  ecartInterventions:   props.modelValue.ecartInterventions   ?? 0,
  prochaineMaintenance: props.modelValue.prochaineMaintenance ?? 0,
});

// Sync depuis le parent (ex : mode édition)
watch(
  () => props.modelValue,
  (val) => {
    localSeuil.derniereIntervention = val.derniereIntervention ?? 0;
    localSeuil.ecartInterventions   = val.ecartInterventions   ?? 0;
    localSeuil.prochaineMaintenance = val.prochaineMaintenance ?? 0;
  },
  { deep: true }
);

const updateProchaineMaintenance = () => {
  const derniere = Number(localSeuil.derniereIntervention);
  const ecart    = Number(localSeuil.ecartInterventions);

  if (isNaN(derniere) || isNaN(ecart)) {
    localSeuil.prochaineMaintenance = "";
  } else {
    localSeuil.prochaineMaintenance = derniere + ecart;
  }

  emit("update:modelValue", { ...localSeuil });
};
</script>