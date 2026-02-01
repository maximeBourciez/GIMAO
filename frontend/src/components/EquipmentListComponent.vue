<template>
  <BaseListView 
    :title="title" 
    :headers="tableHeaders" 
    :items="displayedItems" 
    :loading="loading"
    :error-message="errorMessage" 
    :show-search="showSearch"
    :show-create-button="false" 
    :no-data-text="noDataText" 
    no-data-icon="mdi-package-variant-closed"
    @row-click="$emit('row-click', $event)" 
    @clear-error="errorMessage = ''" 
    :internal-search="true">
    
    <!-- Colonne Statut avec chip coloré -->
    <template #item.statut.statut="{ item }">
      <v-chip 
        v-if="item.statut && item.statut.statut" 
        :color="getStatusColor(item.statut.statut)" 
        variant="tonal"
        size="small">
        {{ getStatusLabel(item.statut.statut) }}
      </v-chip>

      <v-chip v-else color="grey" variant="outlined" size="small">
        Non renseigné
      </v-chip>
    </template>

  </BaseListView>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import BaseListView from '@/components/common/BaseListView.vue';
import { useApi } from '@/composables/useApi';
import { getStatusColor, getStatusLabel } from '@/utils/helpers';
import { API_BASE_URL } from '@/utils/constants';

const props = defineProps({
  title: {
    type: String,
    default: 'Liste des Équipements'
  },
  showSearch: {
    type: Boolean,
    default: true
  },
  noDataText: {
    type: String,
    default: 'Aucun équipement trouvé'
  },
  additionalHeaders: {
    type: Array,
    default: () => []
  },
  tableHeaders: {
    type: Array,
    default: () => [
      { title: 'Référence', key: 'reference', sortable: true, align: 'center' },
      { title: 'Désignation', key: 'designation', sortable: true, align: 'center' },
      { title: 'Lieu', key: 'lieu.nomLieu', sortable: false, align: 'center' },
      { title: 'Modèle', key: 'modele', sortable: false, align: 'center' },
      {
        title: 'Statut',
        key: 'statut.statut',
        sortable: true,
        align: 'center',
        sort: (a, b) => {
          const order = ['EN_FONCTIONNEMENT', 'DEGRADE', 'A_LARRET', 'HORS_SERVICE'];
          return order.indexOf(a) - order.indexOf(b);
        }
      }
    ]
  },
  filteredItems: {
    type: Array,
    default: () => []
  },
  getItemsBySelf: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['row-click', 'equipments-loaded', 'locations-loaded', 'models-loaded']);

const equipmentsApi = useApi(API_BASE_URL);
const locationsApi = useApi(API_BASE_URL);
const modelsApi = useApi(API_BASE_URL);

const errorMessage = ref('');

const equipments = computed(() => equipmentsApi.data.value || []);
const locations = computed(() => locationsApi.data.value || []);
const equipmentModels = computed(() => modelsApi.data.value || []);
const loading = computed(() =>
  equipmentsApi.loading.value || locationsApi.loading.value || modelsApi.loading.value
);

// Use filteredItems from parent if explicitly provided, otherwise use all equipments
const displayedItems = computed(() => {
  if (!props.getItemsBySelf) {
    return props.filteredItems;
  }
  // Otherwise, use all equipments (no filtering) - this is the standalone case
  return equipments.value;
});

const fetchData = async () => {
  try {
    await Promise.all([
      equipmentsApi.get('equipements/'),
      locationsApi.get('lieux/hierarchy/'),
      modelsApi.get('modele-equipements/')
    ]);
    emit('equipments-loaded', equipments.value);
    emit('locations-loaded', locations.value);
    emit('models-loaded', equipmentModels.value);
  } catch (error) {
    console.error('Erreur lors du chargement des données:', error);
    errorMessage.value = 'Erreur lors du chargement des données';
  }
};

// Exposer des méthodes publiques
defineExpose({
  fetchData,
  equipments,
  locations,
  equipmentModels
});

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.v-data-table tr:hover {
  background-color: #e6f2ff;
  transition: background-color 0.3s ease;
}

.v-data-table tr:hover td {
  color: #0056b3;
}

.v-data-table th {
  color: black !important;
}
</style>