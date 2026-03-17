<template>
  <v-expansion-panels multiple variant="accordion">

    <!-- 🔹 CRÉER DI -->
    <v-expansion-panel v-if="roleIsAbove('Opérateur')">
      <v-expansion-panel-title>
        Créer une demande d’intervention
      </v-expansion-panel-title>

      <v-expansion-panel-text>
        <CreationDITab />
      </v-expansion-panel-text>
    </v-expansion-panel>

    <!-- 🔹 CONSULTER DI -->
    <v-expansion-panel v-if="roleIsAbove('Opérateur')">
      <v-expansion-panel-title>
        Consulter vos demandes d’intervention
      </v-expansion-panel-title>

      <v-expansion-panel-text>
        <SuiviDITab />
      </v-expansion-panel-text>
    </v-expansion-panel>

    <!-- 🔹 MODIFIER DI -->
    <v-expansion-panel v-if="roleIsAbove('Opérateur')">
      <v-expansion-panel-title>
        Modifier une demande d’intervention
      </v-expansion-panel-title>

      <v-expansion-panel-text>
        <ModificationDITab />
      </v-expansion-panel-text>
    </v-expansion-panel>

  </v-expansion-panels>
</template>

<script setup>
import CreationDITab from "./CreationDITab.vue";
import SuiviDITab from "./SuiviDITab.vue";
import ModificationDITab from "./ModificationDITab.vue";
import ZoomImage from "../common/ZoomImage.vue";

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
  max-width: 900px;
  margin: auto;
}

p {
  margin-bottom: 16px;
}
</style>