<template>
  <BaseListView 
    :title="title" 
    :headers="tableHeaders" 
    :items="failures" 
    :loading="loading"
    :error-message="errorMessage" 
    :create-button-text="createButtonText"
    :no-data-text="noDataText" 
    :no-data-icon="noDataIcon" 
    @create="handleCreate"
    @row-click="handleRowClick" 
    @clear-error="errorMessage = ''">
    <!-- Colonne Createur -->
    <template #item.createur="{ item }">
      <v-chip dark>
        {{ item.utilisateur.nomUtilisateur }}
      </v-chip>
    </template>

    <!-- Colonne Statut -->
    <template #item.statut="{ item }">
      <v-chip :color="item.dateTraitementDefaillance ? 'green' : 'red'" dark>
        {{ item.dateTraitementDefaillance ? 'Oui' : 'Non' }}
      </v-chip>
    </template>

    <!-- Colonne Equipement -->
    <template #item.equipement="{ item }">
      <v-chip dark>
        {{ item.equipement.reference }}
      </v-chip>
    </template>

    
  </BaseListView>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import BaseListView from '@/components/common/BaseListView.vue';
import { useApi } from '@/composables/useApi';
import { getFailureLevelColor } from '@/utils/helpers';
import { TABLE_HEADERS, API_BASE_URL } from '@/utils/constants';

const props = defineProps({
  title: {
    type: String,
    default: 'Liste des Défaillances'
  },
  createButtonText: {
    type: String,
    default: 'Nouvelle Défaillance'
  },
  noDataText: {
    type: String,
    default: 'Aucune défaillance enregistrée'
  },
  noDataIcon: {
    type: String,
    default: 'mdi-alert-circle-outline'
  },
  apiEndpoint: {
    type: String,
    default: 'demandes-intervention/'
  }
});

const emit = defineEmits(['create', 'row-click']);

const api = useApi(API_BASE_URL);
const errorMessage = ref('');

const failures = computed(() => api.data.value || []);
const loading = computed(() => api.loading.value);
const tableHeaders = TABLE_HEADERS.FAILURES;

const handleCreate = () => {
  emit('create');
};

const handleRowClick = (item) => {
  emit('row-click', item);
};

onMounted(async () => {
  try {
    await api.get(props.apiEndpoint);
  } catch (error) {
    errorMessage.value = 'Erreur lors du chargement des défaillances';
  }
});
</script>
