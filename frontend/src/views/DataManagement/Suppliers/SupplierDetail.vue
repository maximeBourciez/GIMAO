<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card v-if="supplier">
          <v-card-title>Détails du fournisseur</v-card-title>
          <v-card-text>
            <v-alert v-if="error_message" type="error">
              {{ error_message }}
            </v-alert>
            <v-list>
              <v-list-item>
                <v-list-item-title>Nom du fournisseur:</v-list-item-title>
                <v-list-item-subtitle>{{ supplier.nomFournisseur }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Adresse:</v-list-item-title>
                <v-list-item-subtitle>
                  {{ supplier.numRue }} {{ supplier.nomRue }}, {{ supplier.codePostal }} {{ supplier.ville }}
                </v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Pays:</v-list-item-title>
                <v-list-item-subtitle>{{ supplier.paysFournisseur }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Email:</v-list-item-title>
                <v-list-item-subtitle>{{ supplier.mailFournisseur }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Téléphone:</v-list-item-title>
                <v-list-item-subtitle>{{ supplier.numTelephoneFournisseur }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Service Après-Vente:</v-list-item-title>
                <v-list-item-subtitle>{{ supplier.serviceApresVente ? 'Oui' : 'Non' }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="go_back">
              Retour
            </v-btn>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
        <v-alert v-else-if="is_loading" type="info">
          Chargement du fournisseur...
        </v-alert>
        <v-alert v-else type="warning">
          Fournisseur non trouvé
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '@/services/api';

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();
    const supplier = ref(null);
    const error_message = ref('');
    const is_loading = ref(true);
    const show_delete_confirmation = ref(false);

    const get_supplier = async () => {
      is_loading.value = true;
      error_message.value = '';
      try {
        const response = await api.getFournisseur(route.params.id);
        supplier.value = response.data;
      } catch (error) {
        console.error('Error fetching supplier:', error);
        error_message.value = 'Erreur lors de la récupération du fournisseur.';
      } finally {
        is_loading.value = false;
      }
    };

    const go_back = () => {
      router.go(-1);
    };

    onMounted(() => {
      get_supplier();
    });

    return {
      supplier,
      error_message,
      is_loading,
      go_back,
      show_delete_confirmation
    };
  }
};
</script>