<template>
  <BaseListView
    ref="tableContainer"
    :title="title"
    :headers="tableHeaders"
    :items="failures"
    :loading="loading"
    :error-message="resolvedErrorMessage"
    :no-data-text="noDataText"
    :no-data-icon="noDataIcon"
    :show-search="showSearch"
    :show-create-button="false"
    :search-value="searchQuery"
    :items-per-page="-1"
    :hide-default-footer="true"
    :internal-search="false"
    @row-click="handleRowClick"
    @clear-error="errorMessage = ''"
    @search="handleSearch"
  >
    <template #item.createur="{ item }">
      {{ item.utilisateur?.prenom ?? '' }} {{ item.utilisateur?.nomFamille ?? '' }}
    </template>

    <template #item.commentaire="{ item }">
      {{ item.commentaire?.length > 50 ? `${item.commentaire.substring(0, 50)}...` : item.commentaire }}
    </template>

    <template #item.statut="{ item }">
      <v-chip :color="item.statut ? FAILURE_STATUS_COLORS[item.statut] : 'grey'" dark>
        {{ FAILURE_STATUS[item.statut] }}
      </v-chip>
    </template>

    <template #item.equipement="{ item }">
      {{ item.equipement?.designation }}
    </template>

    <template #after-table>
      <ServerPaginationControls
        :page="currentPage"
        :page-size="pageSize"
        :page-count="totalPages"
        :total-items="totalItems"
        item-label-singular="demande"
        item-label-plural="demandes"
        :reserve-fab-space="showCreateButton"
        @update:page="currentPage = $event"
        @update:page-size="pageSize = $event"
      />
    </template>
  </BaseListView>

  <FloatingCreateButton
    :visible="showCreateButton"
    :tooltip="createButtonText"
    @click="$emit('create')"
  />
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import BaseListView from '@/components/common/BaseListView.vue';
import FloatingCreateButton from '@/components/common/FloatingCreateButton.vue';
import ServerPaginationControls from '@/components/common/ServerPaginationControls.vue';
import { useApi } from '@/composables/useApi';
import { usePaginatedList } from '@/composables/usePaginatedList';
import { TABLE_HEADERS, API_BASE_URL, FAILURE_STATUS, FAILURE_STATUS_COLORS } from '@/utils/constants';

const props = defineProps({
  createButtonText: {
    type: String,
    default: 'Nouvelle demande d\'intervention',
  },
  noDataText: {
    type: String,
    default: 'Aucune demande d\'intervention enregistrée',
  },
  noDataIcon: {
    type: String,
    default: 'mdi-alert-circle-outline',
  },
  apiEndpoint: {
    type: String,
    default: 'demandes-intervention/',
  },
  templateHeader: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: 'Liste des demandes d\'intervention',
  },
  showSearch: {
    type: Boolean,
    default: true,
  },
  showCreateButton: {
    type: Boolean,
    default: true,
  },
});

const emit = defineEmits(['create', 'row-click']);

const api = useApi(API_BASE_URL);
const errorMessage = ref('');
const containerWidth = ref(0);

const {
  items: failures,
  currentPage,
  pageSize,
  totalItems,
  totalPages,
  searchQuery,
  loading,
  errorMessage: paginationErrorMessage,
  fetchPage,
  handleSearch,
} = usePaginatedList({
  api,
  endpoint: () => props.apiEndpoint,
  initialPageSize: 10,
});

const resolvedErrorMessage = computed(() => errorMessage.value || paginationErrorMessage.value);

const tableHeaders = computed(() => {
  if (containerWidth.value < 860) {
    return TABLE_HEADERS.FAILURES_SUPER_LIGHT;
  }

  if (props.templateHeader || containerWidth.value < 1000) {
    return TABLE_HEADERS.FAILURES_LIGHT;
  }

  return TABLE_HEADERS.FAILURES;
});

const handleRowClick = (item) => {
  emit('row-click', item);
};

const tableContainer = ref(null);
let resizeObserver = null;
let resizeTimeout = null;

const observeTableWidth = () => {
  resizeObserver = new ResizeObserver((entries) => {
    if (resizeTimeout) {
      clearTimeout(resizeTimeout);
    }

    resizeTimeout = setTimeout(() => {
      const entry = entries[0];
      if (entry) {
        containerWidth.value = Math.round(entry.contentRect.width);
      }
    }, 100);
  });

  const element = tableContainer.value?.$el ?? tableContainer.value;
  if (element) {
    resizeObserver.observe(element);
  }
};

onMounted(() => {
  fetchPage().catch(() => {
    errorMessage.value = 'Erreur lors du chargement des défaillances';
  });

  observeTableWidth();
});

onBeforeUnmount(() => {
  if (resizeTimeout) {
    clearTimeout(resizeTimeout);
  }

  if (resizeObserver) {
    resizeObserver.disconnect();
  }
});
</script>
