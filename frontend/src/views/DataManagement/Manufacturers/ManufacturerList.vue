<template>
  <v-container>
    <v-row class="mb-4">
      <!-- Search bar -->
      <v-col cols="9">
        <v-text-field
          v-model="search_query"
          label="Rechercher un fabricant"
          prepend-icon="mdi-magnify"
          clearable
        ></v-text-field>
      </v-col>
      <v-col cols="3" class="align-center">
        <v-btn 
          color="primary"
          @click="$router.push('/CreateManufacturer')"
          class="ml-2"
          height="50%"
        >
          Créer un fabricant
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col v-for="manufacturer in filtered_manufacturers" :key="manufacturer.id" cols="12" sm="6" md="4">
        <v-card @click="go_to_manufacturer_detail(manufacturer.id)">
          <v-card-title>{{ manufacturer.nomFabricant }}</v-card-title>
          <v-card-text>
            <p>Pays: {{ manufacturer.paysFabricant }}</p>
            <p>Email: {{ manufacturer.mailFabricant }}</p>
            <p>Téléphone: {{ manufacturer.numTelephoneFabricant }}</p>
            <p>Service Après-Vente: {{ manufacturer.serviceApresVente ? 'Oui' : 'Non' }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'ListeFabricants',
  data() {
    return {
      manufacturers: [],
      search_query: ''
    };
  },
  computed: {
    filtered_manufacturers() {
      if (!this.search_query) {
        return this.manufacturers;
      }
      const search_lower = this.search_query.toLowerCase();
      return this.manufacturers.filter(manufacturer => 
        manufacturer.nomFabricant.toLowerCase().includes(search_lower) ||
        manufacturer.paysFabricant.toLowerCase().includes(search_lower) ||
        manufacturer.mailFabricant.toLowerCase().includes(search_lower)
      );
    }
  },
  methods: {
    async fetch_manufacturers() {
      try {
        const response = await api.getFabricants();
        this.manufacturers = response.data;
      } catch (error) {
        console.error('Erreur lors de la récupération des fabricants:', error);
      }
    },
    go_to_manufacturer_detail(id) {
      this.$router.push(`/ManufacturerDetail/${id}`);
    }
  },
  created() {
    this.fetch_manufacturers();
  }
}
</script>