<template>
  <BaseForm v-model="formData" title="Ajouter des documents à l'intervention" :loading="loading"
    :error-message="errorMessage" :success-message="successMessage" submit-button-text="Sauvegarder les documents"
    @submit="handleSubmit">
    <template #default="{ formData }">
      <v-row v-for="(document, index) in documents" :key="index" class="mb-2">
        <v-col cols="5">
          <v-text-field v-model="document.name" label="Nom du document" required
            :rules="[v => !!v || 'Le nom est requis']"></v-text-field>
        </v-col>
        <v-col cols="5">
          <v-file-input v-model="document.file" label="Fichier" required
            :rules="[v => !!v || 'Le fichier est requis']"></v-file-input>
        </v-col>
        <v-col cols="2" class="d-flex align-center">
          <v-btn color="error" @click="removeDocument(index)" icon :disabled="documents.length === 1">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-col>
      </v-row>

      <v-btn color="secondary" @click="addDocument" class="mt-2" prepend-icon="mdi-plus">
        Ajouter un autre document
      </v-btn>
    </template>
  </BaseForm>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import BaseForm from '@/components/BaseForm.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const route = useRoute();
const router = useRouter();
const api = useApi(API_BASE_URL);

const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const formData = ref({});
const documents = ref([{ name: '', file: null }]);

const addDocument = () => {
  documents.value.push({ name: '', file: null });
};

const removeDocument = (index) => {
  if (documents.value.length > 1) {
    documents.value.splice(index, 1);
  }
};

const handleSubmit = async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    const intervention_id = route.params.id;
    let allSuccess = true;
    const errors = [];

    for (const doc of documents.value) {
      if (doc.name && doc.file) {
        const formData = new FormData();
        formData.append('nomDocumentIntervention', doc.name);
        formData.append('lienDocumentIntervention', doc.file);
        formData.append('intervention', intervention_id);

        try {
          await api.post('document-interventions/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
        } catch (error) {
          console.error('Error while adding the document:', error);
          allSuccess = false;
          errors.push(doc.name);
        }
      }
    }

    if (allSuccess) {
      successMessage.value = 'Tous les documents ont été sauvegardés avec succès !';
      setTimeout(() => {
        router.push({ name: 'InterventionDetail', params: { id: intervention_id } });
      }, 1500);
    } else {
      errorMessage.value = `Certains documents n'ont pas pu être sauvegardés: ${errors.join(', ')}`;
    }
  } catch (error) {
    console.error('General error while adding documents:', error);
    errorMessage.value = "Erreur lors de l'ajout des documents. Veuillez réessayer.";
  } finally {
    loading.value = false;
  }
};
</script>