<template>
  <BaseForm title="Créer un nouveau lieu" :loading="loading" :errorMessage="errorMessage"
    :successMessage="successMessage" :dismissibleAlerts="true" :submitButtonText="'Créer le lieu'" @submit="onSubmit">
    <v-container>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field v-model="formData.nomLieu" label="Nom du lieu*"
            :rules="[v => !!v || 'Le nom du lieu est requis']" required>
          </v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field v-model="formData.typeLieu" label="Type de lieu (pièce, étage, bâtiment, etc.)*"
            :rules="[v => !!v || 'Le type de lieu est requis']" required>
          </v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-select v-model="formData.parentId" :items="locationOptions" item-title="nomLieu" item-value="id"
            label="Lieu parent" clearable>
          </v-select>
        </v-col>
      </v-row>
    </v-container>
  </BaseForm>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import BaseForm from '@/components/common/BaseForm.vue';
import { useApi } from '@/composables/useApi.js';
import { API_BASE_URL } from '@/utils/constants.js';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

// Données du formulaire
const formData = ref({
  nomLieu: '',
  typeLieu: '',
  parentId: null, // Simple valeur numérique (ID)
});

const locationOptions = ref([]);
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const api = useApi(API_BASE_URL);

const fetchAvailableLocations = async () => {
  try {
    locationOptions.value = await api.get('lieux/');

    // Une fois les lieux chargés, définir le parent si présent dans la route
    const parentIdFromRoute = route.query.parentId;
    if (parentIdFromRoute && parentIdFromRoute !== 'root') {
      // Convertir en nombre si c'est une chaîne
      formData.value.parentId = parseInt(parentIdFromRoute, 10);
      console.log("Parent ID défini depuis la route:", formData.value.parentId);
    }
  } catch (error) {
    console.error("Erreur lors de la récupération des lieux :", error);
  }
};

// Gestionnaire de soumission du formulaire
const onSubmit = async () => {
  loading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    // Préparer les données à envoyer
    const dataToSend = {
      nomLieu: formData.value.nomLieu,
      typeLieu: formData.value.typeLieu,
      parentId: formData.value.parentId || null, // Directement l'ID numérique ou null
    };

    console.log("Données envoyées:", dataToSend);

    await api.post('lieux/', dataToSend);
    successMessage.value = 'Lieu créé avec succès !';

    // Rediriger après un court délai
    setTimeout(() => {
      router.push({ name: 'LocationList' });
    }, 1500);

  } catch (error) {
    console.error("Erreur lors de la création du lieu :", error);
    errorMessage.value = error.message || 'Une erreur est survenue lors de la création du lieu.';
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await fetchAvailableLocations();
  console.log("CreateLocation mounted. Route params:", route);
  console.log("Form data:", formData.value);
});

// Watch pour déboguer les changements
watch(() => formData.value.parentId, (newVal) => {
  console.log("parentId changé:", newVal, "Type:", typeof newVal);
});
</script>