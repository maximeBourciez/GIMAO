<template>
  <BaseListView :title="title" :headers="TABLE_HEADERS.SUPPLIERS" :items="suppliers" :loading="loading"
    :error-message="errorMessage" :show-search="true" :show-create-button="false"
    no-data-icon="mdi-package-variant-closed" @row-click="goToSupplierDetail($event.id)"
    @clear-error="errorMessage = ''" :internal-search="true">

    <template #item.serviceApresVente="{ item }">
      <v-chip :color="item.serviceApresVente ? 'success' : 'error'" variant="outlined" size="small">
        {{ item.serviceApresVente ? 'Oui' : 'Non' }}
      </v-chip>
    </template>

    <template #item.actions="{ item }">
      <v-btn icon size="small" @click.stop="goToSupplierDetail(item.id)">
        <v-icon>mdi-eye</v-icon>
      </v-btn>
    </template>
  </BaseListView>

  <!-- Bouton flottant en bas à droite -->
  <v-btn color="primary" size="large" icon class="floating-add-button" elevation="4" @click="goToSupplierCreation">
    <v-icon size="large">mdi-plus</v-icon>
    <v-tooltip activator="parent" location="left">
      {{ createButtonText }}
    </v-tooltip>
  </v-btn>
</template>


<script setup>
import BaseListView from '@/components/common/BaseListView.vue';
import { ref, onMounted } from 'vue';
import { useApi } from '@/composables/useApi.js';
import { API_BASE_URL, TABLE_HEADERS } from '@/utils/constants';
import { useRouter } from 'vue-router';

// Données 
const title = 'Liste des fournisseurs';
const api = useApi(API_BASE_URL);
const suppliers = ref([]);
const loading = ref(true);
const errorMessage = ref('');
const router = useRouter();
const createButtonText = 'Créer un nouveau fournisseur';



// Récup des données
onMounted(async () => {
  loadSuppliers();
})


const loadSuppliers = async () => {
  try {
    suppliers.value = await api.get('fournisseurs/');
    loading.value = false;
  } catch (error) {
    errorMessage.value = 'Erreur lors du chargement des fournisseurs.';
  } finally {
    loading.value = false;
  }
};


// Navigation
const goToSupplierDetail = (id) => {
  router.push({
    name: 'SupplierDetail',
    params: { id: id },
  })
};

const goToSupplierCreation = () => {
  router.push({ name: 'CreateSupplier' });
};

</script>

<style scoped>
.floating-add-button {
  position: fixed !important;
  bottom: 24px;
  right: 24px;
  z-index: 100;
}

.floating-add-button:hover {
  transform: scale(1.1);
  transition: transform 0.2s ease;
}
</style>