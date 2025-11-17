<template>
  <v-app>
    <v-main>
      <v-container>
        <v-card v-if="location">
          <v-card-title>Détails du Lieu</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Nom du Lieu</v-list-item-title>
                  <v-list-item-subtitle>{{ location.nomLieu }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Type du Lieu</v-list-item-title>
                  <v-list-item-subtitle>{{ location.typeLieu }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item v-if="location.lieuParent">
                <v-list-item-content>
                  <v-list-item-title>Lieu Parent</v-list-item-title>
                  <v-list-item-subtitle>{{ location.lieuParent.nomLieu }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
        <v-alert v-else type="error">Lieu non trouvé</v-alert>
        <v-btn color="primary" class="mt-4" @click="go_back">Retour</v-btn>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { useApi } from '@/composables/useApi';
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { API_BASE_URL } from '@/utils/constants';

export default {
  name: 'LocationDetails',
  setup() {
    const router = useRouter();
    const route = useRoute();
    const api = useApi(API_BASE_URL);
    const location = computed(() => api.data.value);

    const fetch_location = async () => {
      try {
        await api.get(`lieux/${route.params.id}/`);
      } catch (error) {
        console.error('Error loading the location:', error);
      }
    };

    const go_back = () => {
      router.go(-1);
    };

    onMounted(() => {
      fetch_location();
    });

    return {
      location,
      go_back,
    };
  },
};
</script>