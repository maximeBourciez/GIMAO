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
import api from '@/services/api';
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'LocationDetails',
  setup() {
    const router = useRouter();
    const route = useRoute();
    const location = ref(null);

    const fetch_location = async () => {
      try {
        const response = await api.getLieu(route.params.id);
        location.value = response.data;
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