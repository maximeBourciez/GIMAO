<template>
  <v-container>
    <v-data-table
      :headers="table_headers"
      :items="failures"
      :items-per-page="10"
      class="elevation-1"
      @click:row="(event, {item}) => open_failure_details(item.id)"
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
    </v-data-table>
  </v-container>
</template>

<script>
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useApi } from '@/composables/useApi';
import { getFailureLevelColor } from '@/utils/helpers';
import { TABLE_HEADERS, API_BASE_URL } from '@/utils/constants';

export default {
  name: 'FailureList',
  setup() {
    const router = useRouter();
    const api = useApi(API_BASE_URL);
    
    const failures = computed(() => api.data.value || []);
    const loading = computed(() => api.loading.value);

    const open_failure_details = (id) => {
      router.push({ name: 'FailureDetail', params: { id } });
    };

    onMounted(() => {
      api.get('defaillances/');
    });

    return {
      failures,
      loading,
      table_headers: TABLE_HEADERS.FAILURES,
      get_level_color: getFailureLevelColor,
      open_failure_details,
    };
  },
}
</script>