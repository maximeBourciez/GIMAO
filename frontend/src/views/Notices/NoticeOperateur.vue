<template>
  <div class="py-2">
    <!-- Intro -->
    <div class="text-body-2 mb-4">
      En tant qu'opérateur, votre rôle principal est de signaler les pannes constatées sur les équipements et d'en suivre le traitement. Vous n'avez pas accès aux stocks ni à la gestion des comptes.
    </div>

    <!-- Onglets -->
    <v-tabs v-model="tab" class="mb-4">
      <v-tab value="dashboard">Tableau de bord</v-tab>
      <v-tab value="creation">Créer une DI</v-tab>
      <v-tab value="suivi">Suivi des DI</v-tab>
      <v-tab value="modification">Modifier une DI</v-tab>
      <v-tab value="equipements">Équipements</v-tab>
      <v-tab value="bt">Bons de travail</v-tab>
    </v-tabs>

    <v-window v-model="tab">
      <v-window-item value="dashboard">
        <DashboardTab />
      </v-window-item>

      <v-window-item value="creation">
        <CreationDITab />
      </v-window-item>

      <!-- <v-window-item value="suivi">
        <SuiviDITab />
      </v-window-item>

      <v-window-item value="modification">
        <ModificationDITab />
      </v-window-item>

      <v-window-item value="equipements">
        <EquipementsTab />
      </v-window-item>

      <v-window-item value="bt">
        <BTTab />
      </v-window-item> -->
    </v-window>
  </div>
</template>

<script setup>
import { ref } from "vue";

import DashboardTab from "./Dashboard/DashboardTab.vue";
import CreationDITab from "./DI/CreationDITab.vue";
// import SuiviDITab from "./tabs/SuiviDITab.vue";
// import ModificationDITab from "./tabs/ModificationDITab.vue";
// import EquipementsTab from "./tabs/EquipementsTab.vue";
// import BTTab from "./tabs/BTTab.vue";

const tab = ref("dashboard");
</script>