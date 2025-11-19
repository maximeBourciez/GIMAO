<template>
  <v-container>
    <v-row class="mb-4">
      <!-- Search Bar -->
      <v-col cols="9">
        <v-text-field
          v-model="search_query"
          label="Rechercher un modele d'equipement"
          prepend-icon="mdi-magnify"
          clearable
        ></v-text-field>
      </v-col>
      <v-col cols="3" class="align-center">
        <v-btn 
          color="primary"
          @click="$router.push('/CreateModelEquipment')"
          class="ml-2"
          height="50%"
        >
          Creer un modele d'equipement
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col 
        v-for="model_equipment in filtered_model_equipment" 
        :key="model_equipment.id" 
        cols="12" 
        sm="6" 
        md="4"
      >
        <v-card @click="go_to_model_equipment_details(model_equipment.id)">
          <v-card-title>{{ model_equipment.nomModeleEquipement }}</v-card-title>
          <v-card-text>
            <p>Fabricant : {{ model_equipment.manufacturer_name }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useApi } from '@/composables/useApi';
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { API_BASE_URL } from '@/utils/constants';

export default {
  name: 'ModelEquipmentList',
  setup() {
    const router = useRouter();
    const modelsApi = useApi(API_BASE_URL);
    const manufacturersApi = useApi(API_BASE_URL);
    const model_equipments = computed(() => modelsApi.data.value || []);
    const manufacturers = computed(() => manufacturersApi.data.value || []);
    const search_query = ref('');
    
    const go_to_model_equipment_details = (id) => {
      router.push(`/ModelEquipmentDetail/${id}`);
    };
    
    onMounted(async () => {
      await Promise.all([
        modelsApi.get('modele-equipements/'),
        manufacturersApi.get('fabricants/')
      ]);
    });
    
    return {
      model_equipments,
      manufacturers,
      search_query,
      go_to_model_equipment_details
    };
  },
  computed: {

    model_equipment_with_manufacturers() {
      return this.model_equipments.map(model_equipement => {
        const manufacturer = this.manufacturers.find(f => f.id === model_equipement.fabricant);
        return {
          ...model_equipement,
          manufacturer_name: manufacturer ? manufacturer.nomFabricant : 'Inconnu'
        };
      });
    },
    filtered_model_equipment() {
      if (!this.search_query) {
        return this.model_equipment_with_manufacturers;
      }
      const searchLower = this.search_query.toLowerCase();
      return this.model_equipment_with_manufacturers.filter(model_equipement => 
        model_equipement.nomModeleEquipement.toLowerCase().includes(searchLower)
      );
    },
  }
}
</script>