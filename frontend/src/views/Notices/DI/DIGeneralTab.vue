<template>

    <v-expansion-panels multiple variant="accordion">

      <!-- 🔹 CRÉER DI -->
      <v-expansion-panel>
        <v-expansion-panel-title>
          Créer une demande d’intervention
        </v-expansion-panel-title>

        <v-expansion-panel-text>
            <CreationDITab />
        </v-expansion-panel-text>
      </v-expansion-panel>

      <!-- 🔹 CONSULTER DI -->
      <v-expansion-panel>
        <v-expansion-panel-title>
          Consulter vos demandes d’intervention
        </v-expansion-panel-title>

        <v-expansion-panel-text>
          <SuiviDITab />

          <ZoomImage src="/images/list-di.png" alt="Liste des DI" />
        </v-expansion-panel-text>
      </v-expansion-panel>

      <!-- 🔹 MODIFIER DI -->
      <v-expansion-panel>
        <v-expansion-panel-title>
          Modifier une demande d’intervention
        </v-expansion-panel-title>

        <v-expansion-panel-text>
            <ModificationDITab />
          <ZoomImage src="/images/edit-di.png" alt="Modification DI" />
        </v-expansion-panel-text>
      </v-expansion-panel>

    </v-expansion-panels>

</template>

<script setup>
import CreationDITab from "./CreationDITab.vue";
import SuiviDITab from "./SuiviDITab.vue";
import ModificationDITab from "./ModificationDITab.vue";

import ZoomImage from "../common/ZoomImage.vue";
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