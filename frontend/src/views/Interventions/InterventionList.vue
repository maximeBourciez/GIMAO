<template>
  <v-container>
    <v-data-table
      :headers="table_headers"
      :items="interventions"
      :items-per-page="10"
      class="elevation-1"
      @click:row="(event, {item}) => open_intervention_detail(item.id)"
    >
      <template v-slot:item.traite="{ item }">
        <v-chip :color="item.dateTraitementDefaillance ? 'green' : 'red'" dark>
          {{ item.dateTraitementDefaillance ? 'Oui' : 'Non' }}
        </v-chip>
      </template>
      <template v-slot:item.niveau="{ item }">
        <v-chip :color="get_level_color(item.niveau)" dark>
          {{ item.niveau }}
        </v-chip>
      </template>
      <template v-slot:item.dateAssignation="{ item }">
        {{ formatDate(item.dateAssignation) }}
      </template>
      <template v-slot:item.dateCloture="{ item }">
        {{ formatDate(item.dateCloture) }}
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useApi } from '@/composables/useApi';
import { getFailureLevelColor, formatDateTime } from '@/utils/helpers';
import { TABLE_HEADERS, API_BASE_URL } from '@/utils/constants';

export default {
  name: 'InterventionList',
  setup() {
    const router = useRouter();
    const api = useApi(API_BASE_URL);
    
    const interventions = computed(() => api.data.value || []);
    const loading = computed(() => api.loading.value);

    const table_headers = [
      {
        title: 'Nom de l\' intervention',
        align: 'start',
        sortable: true,
        value: 'nomIntervention'
      },
      {
        title: 'Date d\'assignation',
        align: 'center',
        sortable: true,
        value: 'dateAssignation'
      },
      {
        title: 'Date de clôture',
        align: 'center',
        sortable: true,
        value: 'dateCloture'
      },
      {
        title: 'Temps estimé',
        align: 'center',
        sortable: true,
        value: 'tempsEstime'
      },
    ];

    const open_intervention_detail = (id) => {
      router.push({ name: 'InterventionDetail', params: { id } });
    };

    onMounted(() => {
      api.get('interventions/');
    });

    return {
      interventions,
      loading,
      table_headers,
      get_level_color: getFailureLevelColor,
      open_intervention_detail,
      formatDate: formatDateTime,
    };
  },
}
</script>
