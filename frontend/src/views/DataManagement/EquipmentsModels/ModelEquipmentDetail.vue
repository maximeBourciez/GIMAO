<template>
  <v-container>
    <!-- En-tête -->
    <v-row class="mb-4">
      <v-col>
        <h1 class="text-h4 text-primary">{{ title }}</h1>
      </v-col>
    </v-row>

    <!-- Message d'erreur -->
    <v-alert v-if="errorMessage" type="error" dismissible class="mb-4">
      {{ errorMessage }}
    </v-alert>

    <!-- Chargement -->
    <v-progress-circular v-if="loading" indeterminate color="primary"></v-progress-circular>

    <!-- Contenu -->
    <v-card v-if="!loading && modelEquipment" elevation="2">
      <v-list>
        <v-list-item>
          <v-list-item-title class="font-weight-bold">ID</v-list-item-title>
          <v-list-item-subtitle>{{ modelEquipment.id }}</v-list-item-subtitle>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item>
          <v-list-item-title class="font-weight-bold">Nom du modèle</v-list-item-title>
          <v-list-item-subtitle>{{ modelEquipment.nom }}</v-list-item-subtitle>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item>
          <v-list-item-title class="font-weight-bold">Fabricant</v-list-item-title>
          <v-list-item-subtitle>{{ modelEquipment.fabricant?.nom || 'Non spécifié' }}</v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </v-card>

    <!-- Bouton retour -->
    <v-row class="mt-4">
      <v-col>
        <v-btn color="secondary" @click="$router.back()">
          <v-icon left>mdi-arrow-left</v-icon>
          Retour
        </v-btn>
      </v-col>
    </v-row>

    <!-- Bouton flottant en bas à droite -->
    <v-btn color="primary" size="large" icon class="floating-add-button" elevation="4"
      @click="$router.push({ name: 'CreateModelEquipment' })">
      <v-icon size="large">mdi-plus</v-icon>
      <v-tooltip activator="parent" location="left">
        Créer un nouveau modèle d'équipement
      </v-tooltip>
    </v-btn>
  </v-container>
</template>

<script setup>
import { useApi } from '@/composables/useApi.js';
import { API_BASE_URL } from '@/utils/constants';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

// Données
const api = useApi(API_BASE_URL);
const route = useRoute();
const modelEquipment = ref(null);
const loading = ref(true);
const errorMessage = ref('');
const title = 'Détail du modèle d\'équipement';
// Récup des données
onMounted(async () => {
  loadModelEquipment();
})

const loadModelEquipment = async () => {
  try {
    const id = route.params.id;
    modelEquipment.value = await api.get(`modele-equipements/${id}/`);
  } catch (error) {
    errorMessage.value = 'Erreur lors du chargement du modèle d\'équipement.';
  } finally {
    loading.value = false;
  }
};

</script>

<style scoped>
.floating-add-button {
  position: fixed;
  bottom: 24px;
  right: 24px;
}
</style>