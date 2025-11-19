<template>
  <v-container>
    <v-row class="mb-4">
      <!-- Search bar -->
      <v-col cols="9">
        <v-text-field
          v-model="search_query"
          label="Rechercher un fournisseur"
          prepend-icon="mdi-magnify"
          clearable
        ></v-text-field>
      </v-col>
      <v-col cols="3" class="align-center">
        <v-btn 
          color="primary"
          @click="$router.push('/CreateSupplier')"
          class="ml-2"
          height="50%"
        >
          Créer un fournisseur
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col v-for="supplier in filtered_suppliers" :key="supplier.id" cols="12" sm="6" md="4">
        <v-card @click="go_to_supplier_details(supplier.id)">
          <v-card-title>{{ supplier.nomFournisseur }}</v-card-title>
          <v-card-text>
            <p>Ville: {{ supplier.ville }}</p>
            <p>Pays: {{ supplier.paysFournisseur }}</p>
            <p>Email: {{ supplier.mailFournisseur }}</p>
            <p>Service Après-Vente: {{ supplier.serviceApresVente ? 'Oui' : 'Non' }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const api = useApi(API_BASE_URL);

export default {
  name: 'SupplierList',
  data() {
    return {
      suppliers: [],
      search_query: ''
    };
  },
  computed: {
    filtered_suppliers() {
      if (!this.search_query) {
        return this.suppliers;
      }
      const search_lower = this.search_query.toLowerCase();
      return this.suppliers.filter(supplier => 
        supplier.nomFournisseur.toLowerCase().includes(search_lower) ||
        supplier.ville.toLowerCase().includes(search_lower) ||
        supplier.paysFournisseur.toLowerCase().includes(search_lower)
      );
    }
  },
  methods: {
    async fetch_suppliers() {
      try {
        const response = await api.get('fournisseurs/');
        this.suppliers = response;
      } catch (error) {
        console.error('Erreur lors de la récupération des fournisseurs:', error);
      }
    },
    go_to_supplier_details(id) {
      this.$router.push(`/SupplierDetail/${id}`);
    }
  },
  created() {
    this.fetch_suppliers();
  }
}
</script>