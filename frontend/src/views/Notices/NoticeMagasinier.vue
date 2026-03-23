<template>
  <div class="py-2">
    <!-- Intro -->
    <div class="text-body-2 mb-4">
      En tant que magasinier, vous gérez les stocks de pièces détachées et consommables de l'entreprise. Vous validez également les demandes de pièces associées aux bons de travail.
    </div>

    <!-- Onglets -->
    <v-tabs v-model="tab" class="mb-4">
      <v-tab value="connexion">Connexion</v-tab>
      <v-tab value="dashboard">Tableau de bord</v-tab>
      <v-tab value="stock">Stocks</v-tab>
      <v-tab value="bt">Bons de travail</v-tab>
      <v-tab value="magasins">Magasins</v-tab>
    </v-tabs>

    <v-window v-model="tab">
      <v-window-item value="connexion">
        <ConnexionTab :hasMenu="false" />
      </v-window-item>

      <v-window-item value="dashboard">
        <v-container class="doc-page">
          <h4>Tableau de bord</h4>
          <div class="text-body-2 mt-2">
            <em>En conception...</em>
          </div>
        </v-container>
      </v-window-item>

      <v-window-item value="stock">
        <StockGeneralTab role="Magasinier" />
      </v-window-item>

      <v-window-item value="bt">
        <v-container class="doc-page">
          <h4>Gestion des bons de travail (Magasinier)</h4>
          <div class="text-body-2 mt-2">
            <em>En conception...</em>
          </div>
        </v-container>
      </v-window-item>

      <v-window-item value="magasins">
        <v-container class="doc-page">
          <h4>Gestion des Magasins</h4>
          <div class="text-body-2 mt-2">
            <em>En conception...</em>
          </div>
        </v-container>
      </v-window-item>

    </v-window>
  </div>
</template>

<script setup>
import { ref } from "vue";

import ConnexionTab from "./Auth/ConnexionTab.vue";
import StockGeneralTab from "./Stock/StockGeneralTab.vue";

const tab = ref("dashboard");
</script>
