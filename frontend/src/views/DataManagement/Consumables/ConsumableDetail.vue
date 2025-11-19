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
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();
    const consumableApi = useApi(API_BASE_URL);
    const fabricantApi = useApi(API_BASE_URL);
    const consumable = computed(() => consumableApi.data.value);
    const fabricant = computed(() => fabricantApi.data.value);
    const error_message = ref('');
    const is_loading = computed(() => consumableApi.loading.value || fabricantApi.loading.value);
    const show_delete_confirmation = ref(false);

    const manufacturer_name = computed(() => {
      return fabricant.value ? fabricant.value.nomFabricant : 'Non spécifié';
    });

    const get_consumable = async () => {
      error_message.value = '';
      try {
        const response = await consumableApi.get(`consommables/${route.params.id}/`);
        if (response.fabricant) {
          await get_manufacturer(response.fabricant);
        }
      } catch (error) {
        console.error('Error fetching consommable:', error);
        error_message.value = 'Erreur lors de la récupération du consommable.';
      }
    };

    const get_manufacturer = async (id) => {
      try {
        await fabricantApi.get(`fabricants/${id}/`);
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