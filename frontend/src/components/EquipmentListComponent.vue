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
    :items-per-page="serverPagination ? -1 : 10"
    :hide-default-footer="serverPagination"
    no-data-icon="mdi-package-variant-closed"
    :internal-search="true"
    @row-click="$emit('row-click', $event)"
    @clear-error="errorMessage = ''"
    @search="handleSearch"
  >
    <template #item.statut.statut="{ item }">
      <v-chip
        v-if="item.statut && item.statut.statut"
        :color="getStatusColor(item.statut.statut)"
        variant="tonal"
        size="small"
      >
        {{ getStatusLabel(item.statut.statut) }}
      </v-chip>

      <v-chip v-else color="grey" variant="outlined" size="small">
        Non renseigné
      </v-chip>
    </template>

    <template v-if="serverPagination" #after-table>
      <div class="pagination-bar">
        <div class="pagination-bar__count">
          {{ totalItems }} équipement<span v-if="totalItems > 1">s</span>
        </div>

        <div class="pagination-bar__controls">
          <v-select
            v-model="pageSize"
            :items="pageSizeOptions"
            label="Par page"
            density="compact"
            variant="outlined"
            hide-details
            class="pagination-bar__page-size"
          />

          <v-pagination
            v-model="currentPage"
            :length="totalPages"
            density="comfortable"
            rounded="circle"
          />
        </div>
      </div>
    </template>
  </BaseListView>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import BaseListView from "@/components/common/BaseListView.vue";
import { useApi } from "@/composables/useApi";
import { getStatusColor, getStatusLabel } from "@/utils/helpers";
import { API_BASE_URL } from "@/utils/constants";

const props = defineProps({
  title: {
    type: String,
    default: "Liste des Équipements",
  },
  showSearch: {
    type: Boolean,
    default: true,
  },
  noDataText: {
    type: String,
    default: "Aucun équipement trouvé",
  },
  additionalHeaders: {
    type: Array,
    default: () => [],
  },
  tableHeaders: {
    type: Array,
    default: () => [
      { title: "Référence", key: "reference", sortable: true, align: "center" },
      { title: "Désignation", key: "designation", sortable: true, align: "center" },
      { title: "Lieu", key: "lieu.nomLieu", sortable: false, align: "center" },
      { title: "Modèle", key: "modele", sortable: false, align: "center" },
      {
        title: "Statut",
        key: "statut.statut",
        sortable: true,
        align: "center",
        sort: (a, b) => {
          const order = ["EN_FONCTIONNEMENT", "DEGRADE", "A_LARRET", "HORS_SERVICE"];
          return order.indexOf(a) - order.indexOf(b);
        },
      },
    ],
  },
  filteredItems: {
    type: Array,
    default: () => [],
  },
  getItemsBySelf: {
    type: Boolean,
    default: false,
  },
  serverPagination: {
    type: Boolean,
    default: false,
  },
  selectedLocationIds: {
    type: Array,
    default: () => [],
  },
  selectedModelIds: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["row-click", "equipments-loaded", "locations-loaded", "models-loaded"]);

const equipmentsApi = useApi(API_BASE_URL);
const locationsApi = useApi(API_BASE_URL);
const modelsApi = useApi(API_BASE_URL);

const errorMessage = ref("");
const currentItems = ref([]);
const currentPage = ref(1);
const pageSize = ref(25);
const totalItems = ref(0);
const serverSearch = ref("");
const pageSizeOptions = [10, 25, 50, 100];

let searchDebounceId = null;

const toItems = (payload) => {
  if (Array.isArray(payload)) {
    return payload;
  }
  if (payload && Array.isArray(payload.results)) {
    return payload.results;
  }
  return [];
};

const locations = computed(() => toItems(locationsApi.data.value));
const equipmentModels = computed(() => toItems(modelsApi.data.value));
const loading = computed(
  () =>
    equipmentsApi.loading.value || locationsApi.loading.value || modelsApi.loading.value,
);
const totalPages = computed(() => Math.max(1, Math.ceil(totalItems.value / pageSize.value)));

const displayedItems = computed(() => {
  if (props.serverPagination || props.getItemsBySelf) {
    return currentItems.value;
  }
  return props.filteredItems;
});

const buildEquipementParams = () => {
  if (!props.serverPagination) {
    return {};
  }

  const params = {
    page: currentPage.value,
    page_size: pageSize.value,
  };

  const searchValue = serverSearch.value.trim();
  if (searchValue) {
    params.search = searchValue;
  }

  if (props.selectedLocationIds.length > 0) {
    params.lieu_ids = props.selectedLocationIds.join(",");
  }

  if (props.selectedModelIds.length > 0) {
    params.modele_ids = props.selectedModelIds.join(",");
  }

  return params;
};

const fetchEquipments = async () => {
  const response = await equipmentsApi.get("equipements/", buildEquipementParams());
  const items = toItems(response);

  currentItems.value = items;
  totalItems.value = props.serverPagination ? Number(response?.count || 0) : items.length;
  emit("equipments-loaded", items);
};

const fetchSupportData = async () => {
  const [locationsResponse, modelsResponse] = await Promise.all([
    locationsApi.get("lieux/hierarchy/"),
    modelsApi.get("modele-equipements/"),
  ]);

  emit("locations-loaded", toItems(locationsResponse));
  emit("models-loaded", toItems(modelsResponse));
};

const fetchData = async () => {
  try {
    await Promise.all([fetchSupportData(), fetchEquipments()]);
  } catch (error) {
    console.error("Erreur lors du chargement des données:", error);
    errorMessage.value = "Erreur lors du chargement des données";
  }
};

const resetToFirstPageAndFetch = () => {
  if (currentPage.value !== 1) {
    currentPage.value = 1;
    return;
  }
  fetchEquipments().catch((error) => {
    console.error("Erreur lors du chargement des équipements:", error);
    errorMessage.value = "Erreur lors du chargement des équipements";
  });
};

const handleSearch = (value) => {
  if (!props.serverPagination) {
    return;
  }

  serverSearch.value = typeof value === "string" ? value : value?.target?.value || "";

  if (searchDebounceId) {
    clearTimeout(searchDebounceId);
  }

  searchDebounceId = setTimeout(() => {
    resetToFirstPageAndFetch();
  }, 300);
};

watch(currentPage, () => {
  if (!props.serverPagination) {
    return;
  }
  fetchEquipments().catch((error) => {
    console.error("Erreur lors du chargement des équipements:", error);
    errorMessage.value = "Erreur lors du chargement des équipements";
  });
});

watch(pageSize, () => {
  if (!props.serverPagination) {
    return;
  }
  resetToFirstPageAndFetch();
});

watch(
  () => [props.selectedLocationIds.join(","), props.selectedModelIds.join(",")],
  () => {
    if (!props.serverPagination) {
      return;
    }
    resetToFirstPageAndFetch();
  },
);

defineExpose({
  fetchData,
  fetchEquipments,
  locations,
  equipmentModels,
});

onMounted(() => {
  fetchData();
});

onBeforeUnmount(() => {
  if (searchDebounceId) {
    clearTimeout(searchDebounceId);
  }
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

.pagination-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 16px 8px 0;
  flex-wrap: wrap;
}

.pagination-bar__count {
  color: #5f6368;
  font-size: 0.95rem;
}

.pagination-bar__controls {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.pagination-bar__page-size {
  width: 120px;
}
</style>
