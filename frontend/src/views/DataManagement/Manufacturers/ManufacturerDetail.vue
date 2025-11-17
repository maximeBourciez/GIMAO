<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card v-if="manufacturer">
          <v-card-title>Détails du fabricant</v-card-title>
          <v-card-text>
            <v-alert v-if="error_message" type="error">
              {{ error_message }}
            </v-alert>
            <v-list>
              <v-list-item>
                <v-list-item-title>Nom du fabricant:</v-list-item-title>
                <v-list-item-subtitle>{{ manufacturer.nomFabricant }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Pays:</v-list-item-title>
                <v-list-item-subtitle>{{ manufacturer.paysFabricant }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Email:</v-list-item-title>
                <v-list-item-subtitle>{{ manufacturer.mailFabricant }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Téléphone:</v-list-item-title>
                <v-list-item-subtitle>{{ manufacturer.numTelephoneFabricant }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Service Après-Vente:</v-list-item-title>
                <v-list-item-subtitle>{{ manufacturer.serviceApresVente ? 'Oui' : 'Non' }}</v-list-item-subtitle>
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
          Chargement du fabricant...
        </v-alert>
        <v-alert v-else type="warning">
          Fabricant non trouvé
        </v-alert>
      </v-col>
    </v-row>
    <v-dialog v-model="show_delete_confirmation" max-width="300">
      <v-card>
        <v-card-title>Confirmer la suppression</v-card-title>
        <v-card-text>
          Êtes-vous sûr de vouloir supprimer ce fabricant ?
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" text @click="show_delete_confirmation = false">Annuler</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
    const manufacturer = ref(null);
    const error_message = ref('');
    const is_loading = ref(true);
    const show_delete_confirmation = ref(false);

    const get_manufacturer = async () => {
      is_loading.value = true;
      error_message.value = '';
      try {
        const response = await api.getFabricant(route.params.id);
        manufacturer.value = response.data;
      } catch (error) {
        console.error('Error fetching manufacturer:', error);
        error_message.value = 'Erreur lors de la récupération du fabricant.';
      } finally {
        is_loading.value = false;
      }
    };

    const go_back = () => {
      router.go(-1);
    };

    onMounted(() => {
      get_manufacturer();
    });

    return {
      manufacturer,
      error_message,
      is_loading,
      go_back,
      show_delete_confirmation
    };
  }
};
</script>