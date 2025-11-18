<template>
  <BaseListView
    title="Liste des Défaillances"
    :headers="tableHeaders"
    :items="failures"
    :loading="loading"
    :error-message="errorMessage"
    create-button-text="Nouvelle Défaillance"
    no-data-text="Aucune défaillance enregistrée"
    no-data-icon="mdi-alert-circle-outline"
    @create="handleCreate"
    @row-click="handleRowClick"
    @clear-error="errorMessage = ''"
  >
    <!-- Colonne Traité -->
    <template #item.traite="{ item }">
      <v-chip :color="item.dateTraitementDefaillance ? 'green' : 'red'" dark>
        {{ item.dateTraitementDefaillance ? 'Oui' : 'Non' }}
      </v-chip>
    </template>

    <!-- Colonne Niveau -->
    <template #item.niveau="{ item }">
      <v-chip :color="getFailureLevelColor(item.niveau)" dark>
        {{ item.niveau }}
      </v-chip>
    </template>
  </BaseListView>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import BaseListView from '@/components/common/BaseListView.vue';
import { useApi } from '@/composables/useApi';
import { getFailureLevelColor } from '@/utils/helpers';
import { TABLE_HEADERS, API_BASE_URL } from '@/utils/constants';

const router = useRouter();
const api = useApi(API_BASE_URL);

const failures = computed(() => api.data.value || []);
const loading = computed(() => api.loading.value);
const errorMessage = ref('');

const tableHeaders = TABLE_HEADERS.FAILURES;

const handleCreate = () => {
  router.push({ name: 'CreateFailure' });
};

const handleRowClick = (item) => {
  router.push({ name: 'FailureDetail', params: { id: item.id } });
};

onMounted(async () => {
  try {
    await api.get('defaillances/');
  } catch (error) {
    errorMessage.value = 'Erreur lors du chargement des défaillances';
  }
});
</script>