<template>
  <v-expansion-panels multiple variant="accordion" class="doc-page">

    <!-- LISTE BT -->
    <v-expansion-panel v-if="roleIsAbove('Opérateur')">
      <v-expansion-panel-title>
        Consulter vos bons de travail
      </v-expansion-panel-title>

      <v-expansion-panel-text>
        <BTConsultTab />
      </v-expansion-panel-text>
    </v-expansion-panel>

    <!-- ASSIGNER / MODIFIER BT -->
    <v-expansion-panel v-if="roleIsAbove('Technicien')">
      <v-expansion-panel-title>
        Réaliser et documenter une intervention
      </v-expansion-panel-title>

      <v-expansion-panel-text>
        <BTRealisationTab />
      </v-expansion-panel-text>
    </v-expansion-panel>

  </v-expansion-panels>
</template>

<script setup>
import BTConsultTab from "./BTConsultTab.vue";
import BTRealisationTab from "./BTRealisationTab.vue";

const props = defineProps({
  role: {
    type: String,
    default: "Opérateur"
  }
});

const roles = ["Opérateur", "Technicien", "Responsable GMAO"];

const roleIsAbove = (minRole) => {
  return roles.indexOf(props.role) >= roles.indexOf(minRole);
};
</script>

<style scoped>
.doc-page {
  max-width: 90%;
  margin: auto;
  margin-bottom: 2rem;
}
ul li {
  margin-bottom: 8px;
}
</style>
