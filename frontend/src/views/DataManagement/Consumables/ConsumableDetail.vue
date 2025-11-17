<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card v-if="consumable">
          <v-card-title>Détails du consommable</v-card-title>
          <v-card-text>
            <v-alert v-if="error_message" type="error">
              {{ error_message }}
            </v-alert>
            <v-img
              v-if="consumable.lienImageConsommable"
              :src="consumable.lienImageConsommable"
              height="200"
              contain
            ></v-img>
            <v-list>
              <v-list-item>
                <v-list-item-title>Désignation:</v-list-item-title>
                <v-list-item-subtitle>{{ consumable.designation }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Fabricant:</v-list-item-title>
                <v-list-item-subtitle>{{ manufacturer_name }}</v-list-item-subtitle>
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
          Chargement du consommable...
        </v-alert>
        <v-alert v-else type="warning">
          Consommable non trouvé
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '@/services/api';

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();
    const consumable = ref(null);
    const fabricant = ref(null);
    const error_message = ref('');
    const is_loading = ref(true);
    const show_delete_confirmation = ref(false);

    const manufacturer_name = computed(() => {
      return fabricant.value ? fabricant.value.nomFabricant : 'Non spécifié';
    });

    const get_consumable = async () => {
      is_loading.value = true;
      error_message.value = '';
      try {
        const response = await api.getConsommable(route.params.id);
        consumable.value = response.data;
        if (consumable.value.fabricant) {
          await get_manufacturer(consumable.value.fabricant);
        }
      } catch (error) {
        console.error('Error fetching consommable:', error);
        error_message.value = 'Erreur lors de la récupération du consommable.';
      } finally {
        is_loading.value = false;
      }
    };

    const get_manufacturer = async (id) => {
      try {
        const response = await api.getFabricant(id);
        fabricant.value = response.data;
      } catch (error) {
        console.error('Error fetching fabricant:', error);
        error_message.value = 'Erreur lors de la récupération du fabricant.';
      }
    };

    const go_back = () => {
      router.go(-1);
    };

    onMounted(() => {
      get_consumable();
    });

    return {
      consumable,
      manufacturer_name,
      error_message,
      is_loading,
      go_back,
      show_delete_confirmation
    };
  }
};
</script>