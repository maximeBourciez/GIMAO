<template>
  <v-container class="pa-4" fluid>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="pa-4">
          <LocationTreeView :items="locations" :showCreateButton="true" />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { API_BASE_URL } from '@/utils/constants.js';
import { useApi } from '@/composables/useApi.js';
import LocationTreeView from '@/components/LocationTreeView.vue';

const api = useApi(API_BASE_URL);
const locations = ref([]);

const fetchLocations = async () => {
  console.log("Fetching locations...");
  try {
    locations.value = await api.get('lieux-hierarchy/');
  } catch (error) {
    console.error(error);
  }
  console.log("Locations fetched:", locations.value);
};

onMounted(async () => {
  await fetchLocations()
});
</script>
