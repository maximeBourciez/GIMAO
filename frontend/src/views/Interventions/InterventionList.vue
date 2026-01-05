<template>
  <BaseListView title="Liste des Interventions" :headers="tableHeaders" :items="tempInterventions" :loading="loading"
    :error-message="errorMessage" :show-create-button="false"
    no-data-text="Aucune intervention enregistrée" no-data-icon="mdi-wrench-outline"
    @row-click="handleRowClick" @clear-error="errorMessage = ''">
    <!-- Colonne Date d'assignation -->
    <template #item.dateAssignation="{ item }">
      {{ formatDateTime(item.dateAssignation) }}
    </template>

    <!-- Colonne Date de clôture -->
    <template #item.dateCloture="{ item }">
      {{ item.dateCloture ? formatDateTime(item.dateCloture) : '-' }}
    </template>
  </BaseListView>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import BaseListView from '@/components/common/BaseListView.vue';
import { useApi } from '@/composables/useApi';
import { formatDateTime } from '@/utils/helpers';
import { API_BASE_URL } from '@/utils/constants';

const router = useRouter();
const api = useApi(API_BASE_URL);

const interventions = computed(() => api.data.value || []);
const loading = computed(() => api.loading.value);
const errorMessage = ref('');

const tempInterventions = [
  {
    id: 1,
    nomIntervention: "Remplacement du filtre à air",
    dateAssignation: "2024-06-10T09:30:00Z",
    dateCloture: "2024-06-12T15:45:00Z",
    tempsEstime: "4 heures"
  },
  {
    id: 2,
    nomIntervention: "Réparation de la pompe hydraulique",
    dateAssignation: "2024-06-11T11:00:00Z",
    dateCloture: null,
    tempsEstime: "6 heures"
  },
  {
    id: 3,
    nomIntervention: "Inspection générale de la machine CNC",
    dateAssignation: "2024-06-09T08:15:00Z",
    dateCloture: "2024-06-10T12:30:00Z",
    tempsEstime: "3 heures"
  }
];

const tableHeaders = [
  {
    title: "Nom de l'intervention",
    align: 'start',
    sortable: true,
    key: 'nomIntervention'
  },
  {
    title: "Date d'assignation",
    align: 'center',
    sortable: true,
    key: 'dateAssignation'
  },
  {
    title: 'Date de clôture',
    align: 'center',
    sortable: true,
    key: 'dateCloture'
  },
  {
    title: 'Temps estimé',
    align: 'center',
    sortable: true,
    key: 'tempsEstime'
  }
];

const handleRowClick = (item) => {
  router.push({ name: 'InterventionDetail', params: { id: item.id } });
};

onMounted(async () => {
  try {
    await api.get('interventions/');
  } catch (error) {
    errorMessage.value = 'Erreur lors du chargement des interventions';
  }
});
</script>
