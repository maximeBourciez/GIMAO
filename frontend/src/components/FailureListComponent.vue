<template>
  <BaseListView ref="tableContainer" :title="title" :headers="tableHeaders" :items="failures" :loading="loading"
    :error-message="errorMessage" :no-data-text="noDataText" :no-data-icon="noDataIcon" :show-search="showSearch"
    :internalSearch="true" :show-create-button="false" @row-click="handleRowClick" @clear-error="errorMessage = ''">

    <!-- Colonne Createur -->
    <template #item.createur="{ item }">
      {{ item.utilisateur.prenom ?? '' }} {{ item.utilisateur.nomFamille ?? '' }}
    </template>
    <template #item.commentaire="{ item }">
      {{ item.commentaire.length > 50 ? item.commentaire.substring(0, 50) + '...' : item.commentaire }}
    </template>

    <!-- Colonne Statut -->
    <template #item.statut="{ item }">
      <v-chip :color="item.statut ? FAILURE_STATUS_COLORS[item.statut] : 'grey'" dark>
        {{ FAILURE_STATUS[item.statut] }}
      </v-chip>
    </template>


    <!-- Colonne Equipement -->
    <template #item.equipement="{ item }">
      {{ item.equipement.designation }}
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
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import BaseListView from '@/components/common/BaseListView.vue';
import { useApi } from '@/composables/useApi';
import { TABLE_HEADERS, API_BASE_URL, FAILURE_STATUS, FAILURE_STATUS_COLORS } from '@/utils/constants';
import { useStore } from 'vuex';


const props = defineProps({
  createButtonText: {
    type: String,
    default: 'Nouvelle demande d\'intervention'
  },
  noDataText: {
    type: String,
    default: 'Aucune demande d\'intervention enregistrée'
  },
  noDataIcon: {
    type: String,
    default: 'mdi-alert-circle-outline'
  },
  apiEndpoint: {
    type: String,
    default: 'demandes-intervention/'
  },
  templateHeader: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Liste des demandes d\'intervention'
  },
  showSearch: {
    type: Boolean,
    default: true
  },
  showCreateButton: {
    type: Boolean,
    default: true
  }
});
const emit = defineEmits(['create', 'row-click']);
const api = useApi(API_BASE_URL);
const errorMessage = ref('');
const failures = computed(() => api.data.value || []);
const loading = computed(() => api.loading.value);
const containerWidth = ref(0);
const store = useStore();



const tableHeaders = computed(() => {
  if (containerWidth.value < 860) {
    return TABLE_HEADERS.FAILURES_SUPER_LIGHT;
  } else if (props.templateHeader) {
    return TABLE_HEADERS.FAILURES_LIGHT;
  }
  return TABLE_HEADERS.FAILURES;
});
const handleCreate = () => {
  emit('create');
};
const handleRowClick = (item) => {
  emit('row-click', item);
};
const tableContainer = ref(null);
let resizeObserver = null;
let resizeTimeout = null;

onMounted(async () => {
  try {
    await api.get(props.apiEndpoint);
  } catch (error) {
    errorMessage.value = 'Erreur lors du chargement des défaillances';
  }

  resizeObserver = new ResizeObserver(entries => {
    if (resizeTimeout) {
      clearTimeout(resizeTimeout);
    }

    resizeTimeout = setTimeout(() => {
      window.requestAnimationFrame(() => {
        const entry = entries[0];
        if (entry) {
          containerWidth.value = Math.round(entry.contentRect.width);
        }
      });
    }, 100);
  });

  if (tableContainer.value) {
    const element = tableContainer.value.$el ?? tableContainer.value;
    if (element) {
      resizeObserver.observe(element);
    }
  }
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
<style scoped>
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