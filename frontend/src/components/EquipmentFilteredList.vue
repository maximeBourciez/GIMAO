<template>
  <v-container fluid :style="containerStyle">
    <v-row>
      <!-- Sidebar gauche avec filtres -->
      <v-col cols="12" md="4" lg="3">
        <!-- Card: Structure des Lieux -->
        <v-card elevation="1" class="rounded-lg pa-2 mb-4">
          <v-card-title class="font-weight-bold text-uppercase text-primary text-body-2">
            Structure des Lieux
          </v-card-title>
          <v-divider></v-divider>
          <div class="pa-2">
            <p v-if="!locations || locations.length === 0" class="text-caption">
              Pas de données disponibles.
            </p>
            <VTreeview v-else v-model:selected="selectedTreeNodes" :items="locations" item-title="nomLieu"
              item-children="children" item-value="id" select-strategy="independent" selectable dense
              @update:selected="onSelectLocation">
              <template v-slot:prepend="{ item, open }">
                <v-icon v-if="item.children && item.children.length > 0 && item.nomLieu !== 'Tous'"
                  @click.stop="toggleNode(item)" :class="{ 'rotate-icon': open }">
                  {{ open ? 'mdi-triangle-down' : 'mdi-triangle-right' }}
                </v-icon>
                <span v-else class="tree-icon-placeholder"></span>
              </template>
              <template v-slot:label="{ item }">
                <span class="text-caption ml-2">{{ item.nomLieu }}</span>
              </template>
            </VTreeview>
          </div>
        </v-card>

        <!-- Card: Types d'équipements -->
        <v-card elevation="1" class="rounded-lg pa-2">
          <v-card-title class="font-weight-bold text-uppercase text-primary text-body-2">
            Types des équipements
          </v-card-title>
          <v-divider></v-divider>
          <v-list dense>
            <v-list-item link @click="handleEquipmentTypeSelected(null)"
              :class="{ 'selected-item': selectedTypeEquipments.length === 0 }">
              <v-list-item-title>Tous</v-list-item-title>
            </v-list-item>
            <v-list-item v-for="(model, index) in equipmentModels" :key="index" link
              @click="handleEquipmentTypeSelected(model)" :class="{ 'selected-item': isEquipmentTypeSelected(model) }">
              <v-list-item-title>{{ model.nom }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <!-- Colonne principale avec BaseListView -->
      <v-col cols="12" md="8" lg="9">
        <BaseListView :title="title" :headers="tableHeaders" :items="filteredEquipments" :loading="loading"
          :error-message="errorMessage" :show-search="showSearch" :show-create-button="false" :no-data-text="noDataText"
          no-data-icon="mdi-package-variant-closed" @row-click="$emit('row-click', $event)"
          @clear-error="errorMessage = ''">
          <!-- Colonne Statut avec chip coloré -->
          <template #item.statut.statut="{ item }">
            <v-chip :color="getStatusColor(item.statut.statut)" text-color="white" size="small">
              {{ item.statut.statut }}
            </v-chip>
          </template>
        </BaseListView>

        <!-- Bouton flottant en bas à droite -->
        <v-btn v-if="showCreateButton" color="primary" size="large" icon class="floating-add-button" elevation="4"
          @click="$emit('create')">
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
import { VTreeview } from 'vuetify/labs/VTreeview';
import BaseListView from '@/components/common/BaseListView.vue';
import { useApi } from '@/composables/useApi';
import { getStatusColor } from '@/utils/helpers';
import { API_BASE_URL } from '@/utils/constants';

const props = defineProps({
  title: {
    type: String,
    default: 'Liste des Équipements'
  },
  showSearch: {
    type: Boolean,
    default: false
  },
  showCreateButton: {
    type: Boolean,
    default: true
  },
  createButtonText: {
    type: String,
    default: 'Ajouter un équipement'
  },
  noDataText: {
    type: String,
    default: 'Aucun équipement trouvé avec ces filtres'
  },
  additionalHeaders: {
    type: Array,
    default: () => []
  },
  height: {
    type: String,
    default: null
  },
  maxHeight: {
    type: String,
    default: null
  }
});

const emit = defineEmits(['create', 'row-click', 'equipments-loaded']);

const equipmentsApi = useApi(API_BASE_URL);
const locationsApi = useApi(API_BASE_URL);
const modelsApi = useApi(API_BASE_URL);

const errorMessage = ref('');
const selectedLocation = ref([]);
const selectedTypeEquipments = ref([]);
const selectedTreeNodes = ref([]);
const openNodes = ref(new Set());

const equipments = computed(() => equipmentsApi.data.value || []);
const locations = computed(() => locationsApi.data.value || []);
const equipmentModels = computed(() => modelsApi.data.value || []);
const loading = computed(() =>
  equipmentsApi.loading.value || locationsApi.loading.value || modelsApi.loading.value
);

const defaultHeaders = [
  { title: 'Désignation', key: 'designation', sortable: true, align: 'center' },
  { title: 'Lieu', key: 'lieu.nomLieu', sortable: true, align: 'center' },
  {
    title: 'Statut',
    key: 'statut.statut',
    sortable: true,
    align: 'center',
    sort: (a, b) => {
      const order = ['Rebuté', 'En fonctionnement', 'Dégradé', 'À l\'arrêt'];
      return order.indexOf(a) - order.indexOf(b);
    }
  }
];

const tableHeaders = computed(() => [...defaultHeaders, ...props.additionalHeaders]);

const fetchData = async () => {
  try {
    await Promise.all([
      equipmentsApi.get('equipements/'),
      locationsApi.get('lieux-hierarchy/'),
      modelsApi.get('modele-equipements/')
    ]);
    emit('equipments-loaded', equipments.value);
  } catch (error) {
    console.error('Erreur lors du chargement des données:', error);
    errorMessage.value = 'Erreur lors du chargement des données';
  }
};

const findItem = (items, id) => {
  for (const item of items) {
    if (item.id === id) return item;
    if (item.children) {
      const found = findItem(item.children, id);
      if (found) return found;
    }
  }
  return null;
};

const onSelectLocation = (items) => {
  if (items.length > 0) {
    selectedLocation.value = items.map(id => {
      const selectedItem = findItem(locations.value, id);
      return selectedItem?.nomLieu;
    }).filter(Boolean);
    console.log('Selected Locations:', selectedLocation.value);
  } else {
    console.log('No Locations Selected');
    selectedLocation.value = [];
  }
};

const toggleNode = (item) => {
  if (openNodes.value.has(item.id)) {
    openNodes.value.delete(item.id);
  } else {
    openNodes.value.add(item.id);
  }
};

const handleEquipmentTypeSelected = (model) => {
  if (model === null) {
    selectedTypeEquipments.value = [];
  } else {
    const index = selectedTypeEquipments.value.findIndex(
      m => m.nom === model.nom
    );
    if (index > -1) {
      selectedTypeEquipments.value.splice(index, 1);
    } else {
      selectedTypeEquipments.value.push(model);
    }
  }
};

const isEquipmentTypeSelected = (model) => {
  return selectedTypeEquipments.value.some(
    m => m.nom === model.nom
  );
};

const filteredEquipments = computed(() => {
  return equipments.value.filter(e => {
    const locationMatch = selectedLocation.value.length === 0 ||
      selectedLocation.value.includes('All') ||
      selectedLocation.value.includes(e.lieu.nomLieu);
    const typeMatch = selectedTypeEquipments.value.length === 0 ||
      selectedTypeEquipments.value.some(m =>
        m.nom === e.modele.nom
      );
    return locationMatch && typeMatch;
  });
});

const containerStyle = computed(() => {
  const styles = {};
  if (props.height) {
    styles.height = props.height;
    styles.overflow = 'auto';
  }
  if (props.maxHeight) {
    styles.maxHeight = props.maxHeight;
    styles.overflow = 'auto';
  }
  return styles;
});

// Exposer des méthodes publiques si nécessaire
defineExpose({
  fetchData,
  filteredEquipments
});

onMounted(() => {
  fetchData();
});

components: {
  VTreeview
}
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

.v-treeview-node--active {
  background-color: #7577e9 !important;
  color: white !important;
}

.v-treeview-node--active:hover {
  background-color: #5658c7 !important;
}

.selected-item {
  background-color: #7577e9 !important;
  color: white !important;
}

.selected-item:hover {
  background-color: #5658c7 !important;
}

.text-caption {
  color: #666;
  font-size: 0.75rem;
}

.tree-icon-placeholder {
  display: inline-block;
  width: 24px;
  height: 24px;
  margin-right: 4px;
}

.rotate-icon {
  transform: rotate(180deg);
}

.v-icon {
  transition: transform 0.3s ease;
}

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
