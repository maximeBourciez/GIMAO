<template>
  <v-container>    
    <v-row class="mb-4">
      <!-- Barre de recherche -->
      <v-col cols="9">
        <v-text-field
          v-model="search_query"
          label="Rechercher un consommable"
          prepend-icon="mdi-magnify"
          clearable
        ></v-text-field>
      </v-col>
      <v-col cols="3" class="align-center">
        <v-btn 
          color="primary" 
          @click="$router.push('/CreateConsumable')"
          class="ml-2"
          height="50%"
        >
          Créer un consommable
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col v-for="consumable in filtered_consumables" :key="consumable.id" cols="12" sm="6" md="4">
        <v-card @click="go_to_consumable_details(consumable.id)">
          <v-img
            :src="consumable.lienImageConsommable"
            height="200px"
            cover
          ></v-img>
          <v-card-title>{{ consumable.designation }}</v-card-title>
          <v-card-text>
            Fabricant: {{ consumable.manufacturer_name }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'ConsumableList',
  data() {
    return {
      consommables: [],
      fabricants: [],
      search_query: ''
    };
  },
  computed: {
    consumables_with_manufacturers() {
      return this.consommables.map(consumable => {
        const manufacturer = this.fabricants.find(f => f.id === consumable.fabricant);
        return {
          ...consumable,
          manufacturer_name: manufacturer ? manufacturer.nomFabricant : 'Inconnu'
        };
      });
    },
    filtered_consumables() {
      if (!this.search_query) {
        return this.consumables_with_manufacturers;
      }
      const searchLower = this.search_query.toLowerCase();
      return this.consumables_with_manufacturers.filter(consumable => 
        consumable.designation.toLowerCase().includes(searchLower)
      );
    }
  },
  methods: {
    async fetch_consumables() {
      try {
        const response = await api.getConsommables();
        this.consommables = response.data;
      } catch (error) {
        console.error('Erreur lors de la récupération des consommables:', error);
      }
    },
    async fetch_manufacturers() {
      try {
        const response = await api.getFabricants();
        this.fabricants = response.data;
      } catch (error) {
        console.error('Erreur lors de la récupération des fabricants:', error);
      }
    },
    go_to_consumable_details(id) {
      this.$router.push(`/ConsumableDetail/${id}`);
    }
  },
  async created() {
    await Promise.all([this.fetch_consumables(), this.fetch_manufacturers()]);
  }
}
</script>