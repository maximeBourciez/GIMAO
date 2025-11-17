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
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

export default {
  name: 'FailureList',
  setup() {
    const router = useRouter();
    const failures = ref([]);
    const table_headers = [
      { 
        title: 'Commentaire', 
        align: 'start',  
        sortable: true, 
        value: 'commentaireDefaillance' 
      },
      { 
        title: 'Traitée', 
        align: 'center', 
        sortable: true, 
        value: 'traite' 
      },
      { 
        title: 'Niveau', 
        align: 'center', 
        sortable: true, 
        value: 'niveau' 
      },
      { 
        title: 'Équipement', 
        align: 'center', 
        sortable: false, 
        value: 'equipement' 
      },
    ];

    const fetch_failures = async () => {
      try {
        const response = await api.getDefaillances();
        failures.value = response.data;
      } catch (error) {
        console.error("Error while fetching failures:", error);
      }
    };

    const open_failure_details = (id) => {
      router.push({ name: 'FailureDetail', params: { id: id } });
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

    onMounted(fetch_failures);

    return {
      failures,
      table_headers,
      get_level_color,
      open_failure_details,
    };
  },
}
</script>