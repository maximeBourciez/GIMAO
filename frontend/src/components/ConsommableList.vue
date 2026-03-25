<template>
  <v-container fluid>
    <!-- Statistiques en haut sur toute la largeur -->
    <StockStatistics :consommables="consommables" :selectedFilter="selectedStockFilter" :bt-count="btPendingCount"
      @filter-change="selectedStockFilter = $event" class="mb-4" />

    <v-row class="mb-4">
      <!-- Colonne Consommables (50%) -->
      <v-col cols="12" lg="6">
        <v-card class="rounded-lg pa-4" elevation="1">
          <!-- Header custom -->
          <div class="mb-4">
            <h1 class="text-h4 text-primary">{{ title }}</h1>
            <p class="text-subtitle-1 text-grey">{{ currentSubtitle }}</p>
          </div>

          <!-- Filtres + Recherche -->
          <div class="d-flex align-center ga-3 mb-4">
            <v-btn v-if="store.getters.hasPermission('mag:viewList')" prepend-icon="mdi-filter-variant" variant="flat"
              class="filter-btn" rounded="lg" @click="showMagasinFilterDialog = true">
              Filtrer
            </v-btn>

            <v-text-field v-model="searchQuery" placeholder="Rechercher un consommable..."
              prepend-inner-icon="mdi-magnify" variant="outlined" density="compact" hide-details clearable
              class="flex-grow-1" />
          </div>

          <!-- Tableau -->
          <v-data-table :headers="tableHeaders" :items="searchedConsommables" :loading="loading" :items-per-page="10"
            class="elevation-0" @click:row="(event, { item }) => $emit('row-click', item)">
            <!-- Colonne Quantité avec couleur -->
            <template #item.quantite="{ item }">
              <v-chip size="small" :color="getQuantiteColor(item.quantite_totale, item.seuilStockFaible)"
                variant="tonal">
                {{ item.quantite }}
              </v-chip>
            </template>

            <!-- No data -->
            <template #no-data>
              <div class="text-center pa-4">
                <v-icon size="64" color="grey">mdi-package-variant</v-icon>
                <p class="text-h6 mt-2">{{ noDataText }}</p>
              </div>
            </template>
          </v-data-table>
        </v-card>
      </v-col>

      <!-- Colonne BT en attente (50%) -->
      <v-col v-if="store.getters.hasPermission('stock:viewReservations')" cols="12" lg="6">
        <BTStockValidation
          ref="btStockValidationRef"
          :consommables="consommables"
          @count-updated="btPendingCount = $event"
          @counts-updated="handleBtCountsUpdated"
          @stock-updated="handleStockUpdated"
        />
      </v-col>
    </v-row>

    <!-- Bouton flottant en bas à droite -->
    <v-btn v-if="showCreateButton" color="primary" size="large" icon class="floating-add-button" elevation="8"
      @click="$emit('create')">
      <v-icon size="large">mdi-plus</v-icon>
      <v-tooltip activator="parent" location="left">
        {{ createButtonText }}
      </v-tooltip>
    </v-btn>

    <!-- Dialog Filtre par Magasin -->
    <v-dialog v-model="showMagasinFilterDialog" max-width="900px">
      <v-card class="rounded-lg">
        <v-card-title class="d-flex align-center justify-space-between pa-4 pb-2">
          <span class="text-h6 text-primary font-weight-bold">Filtrer par magasin</span>
          <v-btn icon size="small" variant="text" @click="showMagasinFilterDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-divider />

        <v-card-text class="pa-4">
          <MagasinFilter :magasins="magasins" :consommables="consommables" v-model:selectedMagasin="selectedMagasin"
            @edit:magasin="handleOpenEditMagasin" @archive:magasin="handleOpenArchiveMagasin" />
        </v-card-text>

        <v-divider />

        <v-card-actions class="pa-4">
          <v-btn prepend-icon="mdi-plus" variant="text" color="primary" @click="handleCreateMagasin">
            Ajouter un magasin
          </v-btn>
          <v-spacer />
          <v-btn variant="outlined" @click="handleCancelFilter">
            Réinitialiser
          </v-btn>
          <v-btn color="primary" variant="flat" @click="handleApplyFilter">
            Fermer
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog Formulaire Magasin -->
    <v-dialog v-model="showMagasinFormDialog" max-width="500px">
      <v-card class="rounded-lg">
        <MagasinForm :magasin="magasinToEdit" @created="handleMagasinCreated" @updated="handleMagasinUpdated"
          @close="showMagasinFormDialog = false" />
      </v-card>
    </v-dialog>

    <ConfirmationModal
      v-model="showArchiveDialog"
      type="warning"
      title="Confirmer l'archivage"
      message="Êtes-vous sûr de vouloir archiver le magasin ?\nIl ne sera plus visible dans la liste des magasins."
      confirm-text="Archiver"
      :loading="archiving"
      @confirm="archiveMagasin"
      @cancel="handleCancelArchive"
    />
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import MagasinFilter from '@/components/Stock/MagasinFilter.vue';
import MagasinForm from '@/components/Forms/MagasinForm.vue';
import StockStatistics from '@/components/Stock/StockStatistics.vue';
import BTStockValidation from '@/components/Stock/BTStockValidation.vue';
import ConfirmationModal from '@/components/common/ConfirmationModal.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const props = defineProps({
  title: {
    type: String,
    default: 'Liste des consommables'
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
const archiveApi = useApi(API_BASE_URL);
const store = useStore();

const errorMessage = ref('');
const selectedMagasin = ref(null);
const selectedStockFilter = ref(null);
const showMagasinFilterDialog = ref(false);
const showMagasinFormDialog = ref(false);
const showArchiveDialog = ref(false);
const magasinToEdit = ref(null);
const magasinToArchive = ref(null);
const btPendingCount = ref(0);
const btCompletedCount = ref(0);
const btStockValidationRef = ref(null);
const archiving = ref(false);

const consommables = computed(() => consommablesApi.data.value || []);
const magasins = computed(() => magasinsApi.data.value || []);
const loading = computed(() => consommablesApi.loading.value || magasinsApi.loading.value);
const searchQuery = ref('');
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

  if (selectedMagasin.value !== null) {
    filtered = filtered.filter(c => c.magasins.includes(selectedMagasin.value));
  }

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
      const stock = consommable.stocks?.find(s => s.magasin === selectedMagasin.value);
      quantityToDisplay = stock ? stock.quantite : 0;
    } else {
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
  return magasin ? `Magasin : ${magasin.nom} - ${filteredConsommables.value.length} consommable(s)` : '';
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

// Filtrage avec recherche
const searchedConsommables = computed(() => {
  if (!searchQuery.value) return filteredConsommables.value;
  
  const search = searchQuery.value.toLowerCase();
  return filteredConsommables.value.filter(c => 
    c.designation?.toLowerCase().includes(search) ||
    c.magasin_nom?.toLowerCase().includes(search)
  );
});

const handleApplyFilter = () => {
  showMagasinFilterDialog.value = false;
};

const handleCreateMagasin = () => {
  magasinToEdit.value = null;
  showMagasinFormDialog.value = true;
};

const handleOpenEditMagasin = (magasin) => {
  magasinToEdit.value = magasin;
  showMagasinFormDialog.value = true;
};

const handleOpenArchiveMagasin = (magasin) => {
  magasinToArchive.value = magasin;
  showArchiveDialog.value = true;
};

const handleMagasinCreated = async () => {
  await fetchData();
  showMagasinFormDialog.value = false;
};

const handleMagasinUpdated = async () => {
  await fetchData();
  showMagasinFormDialog.value = false;
};

const handleCancelArchive = () => {
  showArchiveDialog.value = false;
  magasinToArchive.value = null;
};

const archiveMagasin = async () => {
  if (!magasinToArchive.value?.id) {
    showArchiveDialog.value = false;
    return;
  }

  archiving.value = true;

  try {
    await archiveApi.patch(`magasins/${magasinToArchive.value.id}/set-archive/`, { archive: true });
    await fetchData();
    if (selectedMagasin.value === magasinToArchive.value.id) {
      selectedMagasin.value = null;
    }
    showArchiveDialog.value = false;
  } catch (error) {
    console.error('Erreur archivage magasin', error);
  } finally {
    archiving.value = false;
    magasinToArchive.value = null;
  }
};

const handleCancelFilter = () => {
  selectedMagasin.value = null;
  showMagasinFilterDialog.value = false;
};

const handleBtCountsUpdated = ({ pending, completed, reserved }) => {
  btPendingCount.value = pending ?? 0;
  btCompletedCount.value = (reserved ?? completed) ?? 0;
};

const handleStockUpdated = async () => {
  await fetchData();
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.floating-add-button {
  position: fixed !important;
  bottom: 24px;
  right: 24px;
  z-index: 1001;
}

.filter-btn {
  background-color: #F1F5FF !important;
  color: #05004E !important;
  text-transform: none !important;
  font-weight: 500;
  letter-spacing: normal !important;
}

.filter-btn:hover {
  background-color: #E4EBFF !important;
}
</style>
