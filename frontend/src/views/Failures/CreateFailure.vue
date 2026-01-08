<template>
  <v-app>
    <v-main>
      <v-container>
        <BaseForm v-model="formData" title="Créer une Défaillance" :loading="loading" :error-message="errorMessage"
          :success-message="successMessage" :loading-message="loadingData ? 'Chargement des données...' : ''"
          :custom-validation="validateForm" submit-button-text="Valider" submit-button-color="success"
          :show-reset-button="true" @submit="handleSubmit">
          <template #default="{ formData }">


            <v-row>
              <v-col cols="12" md="6">
                <v-text-field v-model="formData.nom" label="Nom de la défaillance *" outlined required
                  :rules="validation.getFieldRules('nom')"></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-autocomplete
                  v-model="formData.equipement_id"
                  :items="equipments"
                  item-title="designation"
                  item-value="id"
                  label="Équipement *"
                  outlined
                  required
                  :rules="validation.getFieldRules('equipement_id')"
                ></v-autocomplete>
              </v-col>

              <v-col cols="12">
                <v-textarea v-model="formData.commentaire" label="Commentaires" rows="5" outlined
                  counter="300" :rules="validation.getFieldRules('commentaire')"></v-textarea>
              </v-col>
            </v-row>
          </template>
        </BaseForm>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useStore } from 'vuex';
import BaseForm from '@/components/common/BaseForm.vue';
import { useApi } from '@/composables/useApi';
import { useFormValidation } from '@/composables/useFormValidation';
import { API_BASE_URL } from '@/utils/constants';
import '@/assets/css/global.css';

const router = useRouter();
const route = useRoute();
const store = useStore();
const api = useApi(API_BASE_URL);
const equipmentsApi = useApi(API_BASE_URL);

const loading = ref(false);
const loadingData = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const equipments = ref([]);
const equipmentReference = ref(null);
const connectedUser = computed(() => store.getters.currentUser);

const formData = ref({
  equipement_id: null,
  commentaire: '',
  nom: ''
});

const validation = useFormValidation(formData, {
  nom: [v => !!v || 'Le nom est requis'],
  equipement_id: [v => !!v || "L'équipement est requis"],
  commentaire: [
    v => (v && v.length <= 300) || 'Le commentaire ne doit pas dépasser 300 caractères'
  ]
});

const validateForm = () => {
  return validation.checkRequiredFields(['nom', 'equipement_id']);
};

const fetchData = async () => {
  loadingData.value = true;
  errorMessage.value = '';

  try {
    const response = await equipmentsApi.get('equipements/');
    equipments.value = response;

    const equipmentId = route.params.equipmentId;
    if (equipmentId) {
      equipmentReference.value = equipmentId;
      formData.value.equipement_id = parseInt(equipmentId);
    }
  } catch (error) {
    console.error('Erreur lors de la récupération des données:', error);
    errorMessage.value = 'Erreur lors de la récupération des données. Veuillez réessayer.';
  } finally {
    loadingData.value = false;
  }
};

const handleSubmit = async () => {
  loading.value = true;
  errorMessage.value = '';

  if (!connectedUser.value) {
    errorMessage.value = "Erreur: Utilisateur non connecté";
    loading.value = false;
    return;
  }

  try {
    const failureData = {
      nom: formData.value.nom,
      commentaire: formData.value.commentaire,
      equipement_id: formData.value.equipement_id,
      utilisateur_id: connectedUser.value.id
    };

    const response = await api.post('demandes-intervention/', failureData);
    const newFailureId = response.id;

    successMessage.value = 'Défaillance créée avec succès !';

    setTimeout(() => {
      router.push({ name: 'FailureDetail', params: { id: newFailureId } });
    }, 1500);
  } catch (error) {
    console.error('Erreur lors de la création de la défaillance:', error);
    errorMessage.value = 'Une erreur est survenue lors de la création de la défaillance.';
  } finally {
    loading.value = false;
  }
};


onMounted(() => {
  fetchData();
});
</script>
