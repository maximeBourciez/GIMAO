<template>
  <v-container fluid>
    <v-row>
      <!-- Sidebar gauche avec filtres -->
      <v-col cols="12" md="3">
        <!-- Filtres par Magasin -->
        <MagasinFilter 
          :magasins="magasins"
          :consommables="consommables"
          v-model:selectedMagasin="selectedMagasin"
          class="mb-4"
        />

        <!-- Statistiques -->
        <StockStatistics :consommables="filteredConsommables" />
      </v-col>

      <!-- Colonne principale avec BaseListView -->
      <v-col cols="12" md="9">
        <BaseListView 
          :title="title" 
          :subtitle="currentSubtitle"
          :headers="tableHeaders" 
          :items="filteredConsommables" 
          :loading="loading"
          :error-message="errorMessage" 
          :show-search="true"
          search-label="Rechercher un consommable"
          search-placeholder="Recherchez par désignation..."
          :show-create-button="false"
          :no-data-text="noDataText" 
          no-data-icon="mdi-package-variant"
          @row-click="$emit('row-click', $event)" 
          @clear-error="errorMessage = ''"
          :internal-search="true"
        >
          <!-- Colonne Fournisseur -->
          <template #item.fournisseur_nom="{ item }">
            <span v-if="item.fournisseur_nom">{{ item.fournisseur_nom }}</span>
            <span v-else class="text-grey">-</span>
          </template>

          <!-- Colonne Quantité avec couleur -->
          <template #item.quantite="{ item }">
            <v-chip 
              size="small"
              :color="getQuantiteColor(item.quantite, item.seuilStockFaible)"
              variant="tonal"
            >
              {{ item.quantite }}
            </v-chip>
          </template>
        </BaseListView>

        <!-- Bouton flottant en bas à droite -->
        <v-btn 
          v-if="showCreateButton" 
          color="primary" 
          size="large" 
          icon 
          class="floating-add-button" 
          elevation="4"
          @click="$emit('create')"
        >
          <v-icon size="large">mdi-plus</v-icon>
          <v-tooltip activator="parent" location="left">
            {{ createButtonText }}
          </v-tooltip>
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import BaseListView from '@/components/common/BaseListView.vue';
import MagasinFilter from '@/components/Stock/MagasinFilter.vue';
import StockStatistics from '@/components/Stock/StockStatistics.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const props = defineProps({
  title: {
    type: String,
    default: 'Gestion des Consommables'
  },
  showCreateButton: {
    type: Boolean,
    default: true
  },
  createButtonText: {
    type: String,
    default: 'Ajouter un consommable'
  },
  noDataText: {
    type: String,
    default: 'Aucun consommable trouvé'
  }
});

const emit = defineEmits(['create', 'row-click', 'consommables-loaded']);

const consommablesApi = useApi(API_BASE_URL);
const magasinsApi = useApi(API_BASE_URL);

const errorMessage = ref('');
const selectedMagasin = ref(null);

const consommables = computed(() => consommablesApi.data.value || []);
const magasins = computed(() => magasinsApi.data.value || []);
const loading = computed(() => consommablesApi.loading.value || magasinsApi.loading.value);

// Headers du tableau
const tableHeaders = [
  { title: 'Nom', key: 'designation', sortable: true },
  { title: 'Fournisseur', key: 'fournisseur_nom', sortable: true },
  { title: 'Quantité', key: 'quantite', sortable: true, align: 'center' }
];

// Sous-titre dynamique
const currentSubtitle = computed(() => {
  if (selectedMagasin.value === null) {
    return `${filteredConsommables.value.length} consommable(s) au total`;
  }
  const magasin = magasins.value.find(m => m.id === selectedMagasin.value);
  return magasin ? `Magasin: ${magasin.nom} - ${filteredConsommables.value.length} consommable(s)` : '';
});

// Filtrage par magasin
const filteredConsommables = computed(() => {
  if (selectedMagasin.value === null) {
    return consommables.value;
  }
  return consommables.value.filter(c => c.magasin === selectedMagasin.value);
});

// Couleur de la quantité
const getQuantiteColor = (quantite, seuil) => {
  if (quantite === 0) return 'error';
  if (seuil !== null && quantite <= seuil) return 'warning';
  return 'success';
};

// Chargement des données
const fetchData = async () => {
  try {
    await Promise.all([
      consommablesApi.get('consommables/'),
      magasinsApi.get('magasins/')
    ]);
    emit('consommables-loaded', consommables.value);
  } catch (error) {
    console.error('Erreur lors du chargement des données:', error);
    errorMessage.value = 'Erreur lors du chargement des données';
  }
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.selected-item {
  border-left: 3px solid rgb(var(--v-theme-primary));
}

.floating-add-button {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 100;
}
</style>
