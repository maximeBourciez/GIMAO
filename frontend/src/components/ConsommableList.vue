<template>
  <v-container fluid>
    <v-row>
      <!-- Colonne principale pleine largeur -->
      <v-col cols="12">
        <!-- Statistiques en haut -->
        <StockStatistics 
          :consommables="consommables" 
          :selectedFilter="selectedStockFilter"
          @filter-change="selectedStockFilter = $event"
          class="mb-4" 
        />
        
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

          <!-- Colonne Fabricant -->
          <template #item.fabricant_nom="{ item }">
            <span v-if="item.fabricant_nom">{{ item.fabricant_nom }}</span>
            <span v-else class="text-grey">-</span>
          </template>

          <!-- Colonne Quantité avec couleur -->
          <template #item.quantite="{ item }">
            <v-chip 
              size="small"
              :color="getQuantiteColor(item.quantite_totale, item.seuilStockFaible)"
              variant="tonal"
            >
              {{ item.quantite }}
            </v-chip>
          </template>

          <!-- Colonne Prix -->
          <template #item.prix_unitaire="{ item }">
            <span v-if="item.prix_unitaire !== null">{{ item.prix_unitaire.toFixed(2) }} €</span>
            <span v-else class="text-grey">-</span>
          </template>
        </BaseListView>
      </v-col>
    </v-row>

    <!-- Bouton flottant en bas à droite -->
    <v-btn
      v-if="showCreateButton" 
      color="primary" 
      size="large" 
      icon 
      class="floating-add-button" 
      elevation="8"
      @click="$emit('create')"
    >
      <v-icon size="large">mdi-plus</v-icon>
      <v-tooltip activator="parent" location="left">
        {{ createButtonText }}
      </v-tooltip>
    </v-btn>

    <!-- Filtres par Magasin sticky en bas -->
    <div class="magasin-filter-sticky" v-if="store.getters.hasPermission('mag:viewList')">
      <v-container fluid>
        <MagasinFilter 
          :magasins="magasins"
          :consommables="consommables"
          v-model:selectedMagasin="selectedMagasin"
        />
      </v-container>
    </div>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import BaseListView from '@/components/common/BaseListView.vue';
import MagasinFilter from '@/components/Stock/MagasinFilter.vue';
import StockStatistics from '@/components/Stock/StockStatistics.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const props = defineProps({
  title: {
    type: String,
    default: 'Liste des Consommables'
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
const store = useStore();

const errorMessage = ref('');
const selectedMagasin = ref(null);
const selectedStockFilter = ref(null);

const consommables = computed(() => consommablesApi.data.value || []);
const magasins = computed(() => magasinsApi.data.value || []);
const loading = computed(() => consommablesApi.loading.value || magasinsApi.loading.value);

const showCreateButton = computed(() => store.getters.hasPermission('cons:create'));

// Headers du tableau
const tableHeaders = [
  { title: 'Nom', key: 'designation', sortable: true },
  { title: 'Magasin', key: 'magasin_nom' },
  { title: 'Quantité', key: 'quantite', sortable: true, align: 'center' }
];

// Fonction utilitaire pour vérifier le statut du stock d'un consommable
const getStockStatus = (consommable) => {
  const quantite = consommable.quantite_totale ?? 0;
  if (quantite === 0) return 'hors-stock';
  if (consommable.seuilStockFaible !== null && quantite <= consommable.seuilStockFaible) return 'sous-seuil';
  return 'stock-suffisant';
};

// Filtrage par magasin et stock sur les consommables originaux
const consommablesFiltered = computed(() => {
  let filtered = consommables.value;

  // Filtre par magasin
  if (selectedMagasin.value !== null) {
    filtered = filtered.filter(c => c.magasins.includes(selectedMagasin.value));
  }

  // Filtre par type de stock (utilise quantite_totale)
  if (selectedStockFilter.value) {
    filtered = filtered.filter(c => getStockStatus(c) === selectedStockFilter.value);
  }

  return filtered;
});

// Expansion des consommables filtrés (Logique Stock)
const filteredConsommables = computed(() => {
  return consommablesFiltered.value.map(consommable => {
    let quantityToDisplay = 0;

    if (selectedMagasin.value !== null) {
      // Cas filtré par magasin : Quantité dans ce magasin
      const stock = consommable.stocks?.find(s => s.magasin === selectedMagasin.value);
      quantityToDisplay = stock ? stock.quantite : 0;
    } else {
      // Cas global : Quantité totale
      quantityToDisplay = consommable.quantite_totale || 0;
    }
    const magasins_noms = [...new Set(consommable.stocks?.map(s => s.magasin_nom).filter(Boolean))].join(', ');

    return {
      ...consommable,
      quantite: quantityToDisplay,
      magasin_nom: magasins_noms || '-',
    };
  });
});

// Sous-titre dynamique
const currentSubtitle = computed(() => {
  if (selectedMagasin.value === null) {
    return `${filteredConsommables.value.length} consommable(s) au total`;
  }
  const magasin = magasins.value.find(m => m.id === selectedMagasin.value);
  return magasin ? `Magasin: ${magasin.nom} - ${filteredConsommables.value.length} consommable(s)` : '';
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
.magasin-filter-sticky {
  position: sticky;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid rgba(0, 0, 0, 0.12);
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  padding: 8px 0;
  margin-top: 24px;
}

.floating-add-button {
  position: fixed !important;
  bottom: 24px;
  right: 24px;
  z-index: 1001;
}
</style>
