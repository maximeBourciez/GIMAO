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
                <v-select v-model="formData.niveau" label="Niveau" :items="levels" outlined dense required
                  :rules="validation.getFieldRules('niveau')"></v-select>
              </v-col>

              <v-col cols="12">
                <v-textarea v-model="formData.commentaireDefaillance" label="Commentaires" rows="5" outlined
                  counter="300" required :rules="validation.getFieldRules('commentaireDefaillance')"></v-textarea>
              </v-col>
            </v-row>
          </template>
        </BaseForm>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BaseForm from '@/components/common/BaseForm.vue';
import { useApi } from '@/composables/useApi';
import { useFormValidation } from '@/composables/useFormValidation';
import { API_BASE_URL } from '@/utils/constants';
import '@/assets/css/global.css';

const router = useRouter();
const route = useRoute();
const api = useApi(API_BASE_URL);
const equipmentsApi = useApi(API_BASE_URL);

const loading = ref(false);
const loadingData = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const levels = ['Mineur', 'Majeur', 'Critique'];
const equipmentReference = ref(null);
const connectedUser = {
  id: 1,
  username: 'admin',
  first_name: 'admin',
  last_name: 'admin',
  email: 'admin@a.com'
};

const formData = ref({
  equipement: null,
  commentaireDefaillance: '',
  niveau: null
});

const validation = useFormValidation(formData, {
  niveau: [v => !!v || 'Le niveau est requis'],
  commentaireDefaillance: [
    v => !!v?.trim() || 'Le commentaire est requis',
    v => (v && v.length <= 300) || 'Le commentaire ne doit pas dépasser 300 caractères',
    v => (v && v.trim().length > 0) || 'Le commentaire ne doit pas être vide ou contenir uniquement des espaces'
  ]
});

const validateForm = () => {
  return validation.checkRequiredFields(['niveau', 'commentaireDefaillance']);
};

const fetchData = async () => {
  loadingData.value = true;
  errorMessage.value = '';

  try {
    await equipmentsApi.get('equipements/');

    const equipmentId = route.params.equipmentId;
    if (equipmentId) {
      equipmentReference.value = equipmentId;
      formData.value.equipement = equipmentId;
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

  try {
    const failureData = {
      commentaireDefaillance: formData.value.commentaireDefaillance,
      niveau: formData.value.niveau,
      equipement: formData.value.equipement,
      utilisateur: connectedUser.id,
      dateTraitementDefaillance: null
    };

    const response = await api.post('defaillances/', failureData);
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
