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
const headerMode = ref(props.templateHeader ? 'light' : 'full');

const FAILURE_SUPER_LIGHT_BREAKPOINT = 860;
const FAILURE_LIGHT_BREAKPOINT = 1000;
const FAILURE_HEADER_HYSTERESIS = 48;

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

const computeFailureHeaderMode = (width) => {
  if (width < FAILURE_SUPER_LIGHT_BREAKPOINT) {
    return 'super-light';
  }

  if (props.templateHeader || width < FAILURE_LIGHT_BREAKPOINT) {
    return 'light';
  }

  return 'full';
};

const resolveFailureHeaderMode = (width, currentMode) => {
  if (currentMode === 'super-light') {
    if (width >= FAILURE_SUPER_LIGHT_BREAKPOINT + FAILURE_HEADER_HYSTERESIS) {
      return props.templateHeader || width < FAILURE_LIGHT_BREAKPOINT ? 'light' : 'full';
    }

    return currentMode;
  }

  if (currentMode === 'light') {
    if (width < FAILURE_SUPER_LIGHT_BREAKPOINT - FAILURE_HEADER_HYSTERESIS) {
      return 'super-light';
    }

    if (!props.templateHeader && width >= FAILURE_LIGHT_BREAKPOINT + FAILURE_HEADER_HYSTERESIS) {
      return 'full';
    }

    return currentMode;
  }

  if (width < FAILURE_LIGHT_BREAKPOINT - FAILURE_HEADER_HYSTERESIS) {
    return props.templateHeader || width >= FAILURE_SUPER_LIGHT_BREAKPOINT
      ? 'light'
      : 'super-light';
  }

  return currentMode;
};

const updateResponsiveState = (width) => {
  const normalizedWidth = Math.round(Number(width) || 0);

  if (normalizedWidth <= 0) {
    return;
  }

  const nextMode = containerWidth.value === 0
    ? computeFailureHeaderMode(normalizedWidth)
    : resolveFailureHeaderMode(normalizedWidth, headerMode.value);

  containerWidth.value = normalizedWidth;

  if (nextMode !== headerMode.value) {
    headerMode.value = nextMode;
  }
};

const tableHeaders = computed(() => {
  if (headerMode.value === 'super-light') {
    return TABLE_HEADERS.FAILURES_SUPER_LIGHT;
  }

  if (headerMode.value === 'light') {
    return TABLE_HEADERS.FAILURES_LIGHT;
  }

  return TABLE_HEADERS.FAILURES;
});

const handleRowClick = (item) => {
  emit('row-click', item);
};

const tableContainer = ref(null);
let resizeObserver = null;
let rafId = null;

const observeTableWidth = () => {
  resizeObserver = new ResizeObserver((entries) => {
    const entry = entries[0];
    if (!entry) {
      return;
    }

    if (rafId) {
      cancelAnimationFrame(rafId);
    }

    rafId = requestAnimationFrame(() => {
      updateResponsiveState(entry.contentRect.width);
    });
  });

  const element = tableContainer.value?.$el ?? tableContainer.value;
  if (element) {
    updateResponsiveState(element.getBoundingClientRect().width);
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
  if (rafId) {
    cancelAnimationFrame(rafId);
  }

  if (resizeObserver) {
    resizeObserver.disconnect();
  }
});
</script>
