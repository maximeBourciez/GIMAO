<template>
  <v-container fluid :style="containerStyle">
    <v-row class="align-stretch">
      <!-- Sidebar gauche avec filtres -->
      <v-col cols="12" md="4" lg="3" class="filters-column">
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
            <div v-else>
              <v-text-field v-model="searchLocation" placeholder="Rechercher un lieu..."
                prepend-inner-icon="mdi-magnify" variant="outlined" density="compact" clearable class="mb-n4">
              </v-text-field>

              <VTreeview v-model:selected="selectedTreeNodes" v-model:opened="openedNodes" :items="filteredLocations"
                item-title="nomLieu" item-children="children" item-value="id" select-strategy="independent" selectable
                dense @update:selected="onSelectLocation">
                <template v-slot:prepend="{ item, open }">
                  <v-icon v-if="item.children && item.children.length > 0 && item.nomLieu !== 'Tous'"
                    @click.stop="toggleNode(item)" :class="{ 'rotate-icon': open }">
                    {{ open ? 'mdi-triangle-down' : 'mdi-triangle-right' }}
                  </v-icon>
                  <span v-else class="tree-icon-placeholder"></span>
                </template>
                <template v-slot:label="{ item }">
                  <span class="text-caption ml-2 tree-label" :title="item.nomLieu">{{ item.nomLieu }}</span>
                </template>
              </VTreeview>
            </div>
          </div>
        </v-card>

        <!-- Card: Types d'équipements -->
        <v-card elevation="1" class="rounded-lg pa-2">
          <v-card-title class="font-weight-bold text-uppercase text-primary text-body-2">
            Types des équipements
          </v-card-title>
          <v-divider></v-divider>
          <v-list density="compact" bg-color="transparent">
            <!-- Option Tous -->
            <v-list-item link @click="handleEquipmentTypeSelected(null)" :active="selectedTypeEquipments.length === 0"
              :class="{ 'selected-item': selectedTypeEquipments.length === 0 }" density="compact">
              <template v-slot:prepend>
                <v-icon size="small" color="grey-darken-1">mdi-all-inclusive</v-icon>
              </template>
              <v-list-item-title class="text-body-2">Tous</v-list-item-title>
            </v-list-item>

            <!-- Types filtrés -->
            <v-list-item v-for="model in filteredEquipmentModels" :key="model.id" link
              @click="handleEquipmentTypeSelected(model)" :active="isEquipmentTypeSelected(model)"
              :class="{ 'selected-item': isEquipmentTypeSelected(model) }" density="compact">
              <template v-slot:prepend>
                <v-icon size="small" color="grey-darken-1">mdi-wrench</v-icon>
              </template>
              <v-list-item-title class="text-body-2">{{ model.nom }}</v-list-item-title>
            </v-list-item>

            <!-- Message si aucun résultat -->
            <v-list-item v-if="filteredEquipmentModels.length === 0 && searchEquipmentType">
              <v-list-item-title class="text-caption text-grey text-center">
                Aucun type trouvé pour "{{ searchEquipmentType }}"
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <!-- Colonne principale avec EquipmentListComponent -->
      <v-col cols="12" md="8" lg="9" ref="tableContainer">
        <EquipmentListComponent :title="title" :show-search="showSearch" :no-data-text="noDataText"
          :table-headers="computedTableHeaders" :filtered-items="filteredEquipments" @row-click="handleRowClick"
          @equipments-loaded="handleEquipmentsLoaded" @locations-loaded="handleLocationsLoaded"
          @models-loaded="handleModelsLoaded" ref="equipmentListComponentRef" />

        <!-- Bouton flottant en bas à droite -->
        <v-btn v-if="showCreateButton" color="primary" size="large" icon class="floating-add-button" elevation="4"
          @click="handleCreate">
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
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { VTreeview } from 'vuetify/labs/components'
import EquipmentListComponent from '@/components/EquipmentListComponent.vue';

const props = defineProps({
  title: {
    type: String,
    default: 'Liste des Équipements'
  },
  showSearch: {
    type: Boolean,
    default: true
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
  height: {
    type: String,
    default: null
  },
  maxHeight: {
    type: String,
    default: null
  }
});

const router = useRouter();

// Refs pour les données
const equipmentListComponentRef = ref(null);
const equipments = ref([]);
const locations = ref([]);
const equipmentModels = ref([]);

// Refs pour les filtres
const selectedLocation = ref([]);
const selectedTypeEquipments = ref([]);
const selectedTreeNodes = ref([]);
const openNodes = ref(new Set());

const searchEquipmentType = ref('');
const filteredEquipmentModels = computed(() => {
  if (!searchEquipmentType.value) {
    handleEquipmentTypeSelected(null);
    return equipmentModels.value;
  }
  return equipmentModels.value.filter(model =>
    model?.nom?.toLowerCase().includes(searchEquipmentType.value.toLowerCase())
  );
});

const searchLocation = ref('');

const openedNodes = ref([]);

const filteredLocations = computed(() => {
  if (!searchLocation.value) {
    openedNodes.value = [];
    return locations.value;
  }

  const search = searchLocation.value.toLowerCase();
  const parentsToOpen = [];

  const filterTree = (nodes) => {
    return nodes.reduce((acc, node) => {
      const matchSelf = node.nomLieu?.toLowerCase().includes(search);
      const filteredChildren = node.children ? filterTree(node.children) : [];

      if (matchSelf || filteredChildren.length > 0) {
        if (filteredChildren.length > 0) {
          parentsToOpen.push(node.id); // ← ouvre ce parent
        }
        acc.push({ ...node, children: filteredChildren });
      }
      return acc;
    }, []);
  };

  const result = filterTree(locations.value);
  openedNodes.value = parentsToOpen;
  return result;
});

// Refs pour le container
const tableContainer = ref(null);
const containerWidth = ref(0);

let resizeObserver;

// Handlers pour les événements du composant enfant
const handleEquipmentsLoaded = (data) => {
  equipments.value = data;
};

const handleLocationsLoaded = (data) => {
  locations.value = data;
};

const handleModelsLoaded = (data) => {
  equipmentModels.value = data;
};

// Navigation handlers
const handleCreate = () => {
  router.push('/CreateEquipment');
};

const handleRowClick = (item) => {
  router.push({ name: 'EquipmentDetail', params: { id: item.id } });
};

// Fonctions utilitaires pour la hiérarchie des lieux
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

const getAllDescendantIds = (item) => {
  let ids = [item.id];
  if (item.children && item.children.length > 0) {
    item.children.forEach(child => {
      ids = ids.concat(getAllDescendantIds(child));
    });
  }
  return ids;
};

const getAllDescendantNames = (item) => {
  let names = [item.nomLieu];
  if (item.children && item.children.length > 0) {
    item.children.forEach(child => {
      names = names.concat(getAllDescendantNames(child));
    });
  }
  return names;
};

// Gestion de la sélection des lieux
const onSelectLocation = (items) => {
  if (items.length > 0) {
    const allLocationNames = [];

    items.forEach(id => {
      const selectedItem = findItem(locations.value, id);
      if (selectedItem) {
        allLocationNames.push(...getAllDescendantNames(selectedItem));
      }
    });

    selectedLocation.value = [...new Set(allLocationNames)];
    console.log('Selected Locations (with descendants):', selectedLocation.value);
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

// Gestion de la sélection des types d'équipements
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
    console.log('Selected Equipment Types:', selectedTypeEquipments.value);
  }
};

const isEquipmentTypeSelected = (model) => {
  return selectedTypeEquipments.value.some(
    m => m.nom === model.nom
  );
};

// Filtrage des équipements
const filteredEquipments = computed(() => {
  if (!equipments.value) return [];

  return equipments.value.filter(e => {
    const locationMatch = selectedLocation.value.length === 0 ||
      selectedLocation.value.includes('All') ||
      selectedLocation.value.includes(e.lieu.nomLieu);

    const typeMatch = selectedTypeEquipments.value.length === 0 ||
      selectedTypeEquipments.value.some(m => m.nom === e.modele);

    return locationMatch && typeMatch;
  });
});

// Headers responsifs
const computedTableHeaders = computed(() => {
  if (containerWidth.value < 700) {
    return compactHeaders;
  }
  return fullHeaders;
});

const fullHeaders = [
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
];

const compactHeaders = [
  { title: 'Réf.', key: 'reference', align: 'center' },
  { title: 'Désignation', key: 'designation', align: 'center' },
  { title: 'Statut', key: 'statut.statut', align: 'center' }
];

// Style du container
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

// Observer pour le responsive
onMounted(() => {
  resizeObserver = new ResizeObserver(entries => {
    const entry = entries[0];
    containerWidth.value = Math.round(entry.contentRect.width);
  });

  if (tableContainer.value) {
    resizeObserver.observe(tableContainer.value.$el ?? tableContainer.value);
  }
});

onBeforeUnmount(() => {
  resizeObserver?.disconnect();
});
</script>

<style scoped>
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

.v-list-item__prepend i,
.v-list-item__prepend i {
  margin-right: 8px;
}

.filters-column {
  max-height: 100%;
  overflow-y: auto;
}

.tree-label {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: inline-block;
}

.filters-column {
  max-height: calc(100% - 120px);
  overflow-y: hidden;
}
</style>