<template>
  <v-container fluid>
    <v-row>
      <!-- Sidebar gauche avec filtres -->
      <v-col cols="12" md="3">
        <!-- Card: Filtres par Magasin -->
        <v-card elevation="1" class="rounded-lg pa-2 mb-4">
          <v-card-title class="font-weight-bold text-uppercase text-primary text-body-2">
            Magasins
          </v-card-title>
          <v-divider></v-divider>
          <v-list dense>
            <v-list-item 
              link 
              @click="selectedMagasin = null"
              :class="{ 'selected-item bg-primary-lighten-5': selectedMagasin === null }"
            >
              <v-list-item-title>Tous les magasins</v-list-item-title>
              <template v-slot:append>
                <v-chip size="small" color="primary">{{ consommables.length }}</v-chip>
              </template>
            </v-list-item>
            <v-list-item 
              v-for="magasin in magasins" 
              :key="magasin.id" 
              link
              @click="selectedMagasin = magasin.id"
              :class="{ 'selected-item bg-primary-lighten-5': selectedMagasin === magasin.id }"
            >
              <v-list-item-title>
                <v-icon v-if="magasin.estMobile" size="small" class="mr-1">mdi-truck</v-icon>
                <v-icon v-else size="small" class="mr-1">mdi-warehouse</v-icon>
                {{ magasin.nom }}
              </v-list-item-title>
              <template v-slot:append>
                <v-chip size="small" color="primary">
                  {{ getConsommableCountByMagasin(magasin.id) }}
                </v-chip>
              </template>
            </v-list-item>
          </v-list>
        </v-card>

        <!-- Card: Statistiques -->
        <v-card elevation="1" class="rounded-lg pa-3">
          <v-card-title class="font-weight-bold text-uppercase text-primary text-body-2 mb-2">
            Statistiques
          </v-card-title>
          <v-divider class="mb-3"></v-divider>
          <v-row dense>
            <v-col cols="12">
              <div class="d-flex justify-space-between align-center mb-2">
                <span class="text-caption text-grey-darken-1">Hors stock</span>
                <v-chip size="small" color="error" variant="tonal">
                  {{ horsStockCount }}
                </v-chip>
              </div>
            </v-col>
            <v-col cols="12">
              <div class="d-flex justify-space-between align-center mb-2">
                <span class="text-caption text-grey-darken-1">Sous le seuil</span>
                <v-chip size="small" color="warning" variant="tonal">
                  {{ sousSeuilCount }}
                </v-chip>
              </div>
            </v-col>
            <v-col cols="12">
              <div class="d-flex justify-space-between align-center">
                <span class="text-caption text-grey-darken-1">Stock suffisant</span>
                <v-chip size="small" color="success" variant="tonal">
                  {{ stockSuffisantCount }}
                </v-chip>
              </div>
            </v-col>
          </v-row>
        </v-card>
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

// Compteur de consommables par magasin
const getConsommableCountByMagasin = (magasinId) => {
  return consommables.value.filter(c => c.magasin === magasinId).length;
};

// Statistiques de stock
const horsStockCount = computed(() => {
  return filteredConsommables.value.filter(c => c.quantite === 0).length;
});

const sousSeuilCount = computed(() => {
  return filteredConsommables.value.filter(c => 
    c.quantite > 0 && c.seuilStockFaible !== null && c.quantite <= c.seuilStockFaible
  ).length;
});

const stockSuffisantCount = computed(() => {
  return filteredConsommables.value.filter(c => 
    c.seuilStockFaible === null || c.quantite > c.seuilStockFaible
  ).length;
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
