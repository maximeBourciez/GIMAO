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
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

export default {
  name: 'InterventionList',
  setup() {
    const router = useRouter();
    const interventions = ref([]);
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

    const fetch_interventions = async () => {
      try {
        const response = await api.getInterventions();
        interventions.value = response.data;
      } catch (error) {
        console.error("Error while fetching interventions:", error);
      }
    };

    const open_intervention_detail = (id) => {
      router.push({ name: 'InterventionDetail', params: { id: id } });
    };

    const get_level_color = (niveau) => {
      switch (niveau) {
        case 'Critique':
          return 'red';
        case 'Majeur':
          return 'orange';
        default:
          return 'green';
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return date.toLocaleDateString(undefined, options);
    };

    onMounted(fetch_interventions);

    return {
      interventions,
      table_headers,
      get_level_color,
      open_intervention_detail,
      formatDate,
    };
  },
}
</script>
