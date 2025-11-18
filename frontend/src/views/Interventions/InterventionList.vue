<template>
  <BaseListView title="Liste des Interventions" :headers="tableHeaders" :items="interventions" :loading="loading"
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
