<template>
  <v-app>
    <v-main>
      <v-container>
        <BaseForm
          v-model="formData"
          :title="`Modifier la demande d'intervention #${failureId}`"
          :loading="submitting"
          :error-message="errorMessage"
          :success-message="successMessage"
          :loading-message="loading ? 'Chargement des données...' : ''"
          submit-button-text="Enregistrer les modifications"
          :handle-submit="handleSubmit"
          @cancel="handleCancel"
        >
          <template #default>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="formData.nom"
                  label="Nom de la demande *"
                  :rules="[rules.required]"
                  variant="outlined"
                  prepend-inner-icon="mdi-file-document"
                  placeholder="Entrez le nom de la demande"
                ></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-textarea
                  v-model="formData.commentaire"
                  label="Description / Commentaire"
                  variant="outlined"
                  prepend-inner-icon="mdi-text"
                  placeholder="Décrivez le problème ou ajoutez des détails..."
                  rows="5"
                  auto-grow
                ></v-textarea>
              </v-col>
            </v-row>
          </template>
        </BaseForm>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { BaseForm } from '@/components/common';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const router = useRouter();
const route = useRoute();
const api = useApi(API_BASE_URL);

const failureId = computed(() => route.params.id || null);
const loading = ref(false);
const submitting = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const formData = ref({
  nom: '',
  commentaire: ''
});

const initialData = ref(null);

const rules = {
  required: value => !!value || 'Ce champ est requis'
};

const fetchFailureData = async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    const response = await api.get(`demandes-intervention/${failureId.value}/`);
    
    const data = {
      nom: response.nom || '',
      commentaire: response.commentaire || ''
    };
    
    formData.value = { ...data };
    initialData.value = { ...data };
    
  } catch (error) {
    console.error('Erreur lors de la récupération des données:', error);
    errorMessage.value = 'Erreur lors du chargement des données de la demande';
  } finally {
    loading.value = false;
  }
};

const detectChanges = () => {
  if (!initialData.value) return { hasChanges: false, changes: {} };

  const changes = {};
  let hasChanges = false;

  if (formData.value.nom !== initialData.value.nom) {
    changes.nom = formData.value.nom;
    hasChanges = true;
  }

  if (formData.value.commentaire !== initialData.value.commentaire) {
    changes.commentaire = formData.value.commentaire;
    hasChanges = true;
  }

  return { hasChanges, changes };
};

const handleSubmit = async () => {
  if (!formData.value.nom) {
    errorMessage.value = 'Veuillez remplir les champs obligatoires';
    return;
  }

  const { hasChanges, changes } = detectChanges();

  if (!hasChanges) {
    errorMessage.value = 'Aucune modification détectée';
    return;
  }

  submitting.value = true;
  errorMessage.value = '';

  try {
    await api.patch(`demandes-intervention/${failureId.value}/`, changes);
    
    successMessage.value = 'Demande d\'intervention modifiée avec succès';
    
    setTimeout(() => {
      router.back();
    }, 1500);
  } catch (error) {
    console.error('Erreur lors de la modification:', error);
    errorMessage.value = 'Erreur lors de la modification de la demande';

    if (error.response?.data) {
      const errors = Object.entries(error.response.data)
        .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
        .join('\n');
      errorMessage.value += `\n${errors}`;
    }
  } finally {
    submitting.value = false;
  }
};

const handleCancel = () => {
  router.back();
};

onMounted(() => {
  fetchFailureData();
});
</script>
