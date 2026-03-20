<template>
  <div class="py-2">
    <!-- Intro -->
    <div class="text-body-2 mb-4">
      En tant que technicien, vous réalisez les interventions sur les équipements. Vous pouvez signaler des pannes, gérer vos bons de travail et consulter les équipements et les stocks.
    </div>

    <!-- Onglets -->
    <v-tabs v-model="tab" class="mb-4">
      <v-tab value="connexion">Connexion</v-tab>
      <v-tab value="dashboard">Tableau de bord</v-tab>
      <v-tab value="di">Demandes d'intervention</v-tab>
      <v-tab value="bt">Bons de travail</v-tab>
      <v-tab value="equipements">Équipements</v-tab>
      <v-tab value="stock">Stocks</v-tab>
    </v-tabs>

    <v-window v-model="tab">
      <v-window-item value="connexion">
        <ConnexionTab :hasMenu="true"/>
      </v-window-item>

      <v-window-item value="dashboard">
        <DashboardTab role="Technicien" />
      </v-window-item>

      <v-window-item value="di">
        <DIGeneralTab role="Technicien"/>
      </v-window-item>

      <v-window-item value="bt">
        <BTGeneralTab role="Technicien"/>
      </v-window-item>

      <v-window-item value="equipements">
        <EquipementsTab role="Technicien"/>
      </v-window-item>

      <v-window-item value="stock">
        <StockGeneralTab role="Technicien"/>
      </v-window-item>
    </v-window>
  </div>
</template>

<script setup>
import { ref } from "vue";

import DashboardTab from "./Dashboard/DashboardTab.vue";
import DIGeneralTab from "./DI/DIGeneralTab.vue";
import EquipementsTab from "./Equipments/EquipementsTab.vue";
import ConnexionTab from "./Auth/ConnexionTab.vue";
import BTGeneralTab from "./BT/BTGeneralTab.vue";
import StockGeneralTab from "./Stock/StockGeneralTab.vue";

const tab = ref("dashboard");
</script>
