<template>
  <BaseForm v-model="formData" title="Ajouter des documents à la défaillance" :loading="loading"
    :error-message="errorMessage" :success-message="successMessage" submit-button-text="Enregistrer tous les documents"
    @submit="handleSubmit">
    <template #default="{ formData }">
      <v-row v-for="(document, index) in documents" :key="index" class="mb-2">
        <v-col cols="5">
          <v-text-field v-model="document.document_name" label="Nom du document" required
            :rules="[v => !!v || 'Le nom est requis']"></v-text-field>
        </v-col>
        <v-col cols="5">
          <v-file-input v-model="document.document_file" label="Fichier du document" required
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
import BaseForm from '@/components/common/BaseForm.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const route = useRoute();
const router = useRouter();
const api = useApi(API_BASE_URL);

const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const formData = ref({});
const documents = ref([{ document_name: '', document_file: null }]);

const addDocument = () => {
  documents.value.push({ document_name: '', document_file: null });
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
    const failure_id = route.params.id;
    let allSuccess = true;
    const errors = [];

    for (const doc of documents.value) {
      if (doc.document_name && doc.document_file) {
        const formData = new FormData();
        formData.append('nomDocumentDefaillance', doc.document_name);
        formData.append('lienDocumentDefaillance', doc.document_file);
        formData.append('defaillance', failure_id);

        try {
          await api.post('document-defaillances/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
        } catch (error) {
          console.error("Erreur lors de l'ajout du document:", error);
          allSuccess = false;
          errors.push(doc.document_name);
        }
      }
    }

    if (allSuccess) {
      successMessage.value = 'Tous les documents ont été enregistrés avec succès !';
      setTimeout(() => {
        router.push({ name: 'FailureDetail', params: { id: failure_id } });
      }, 1500);
    } else {
      errorMessage.value = `Certains documents n'ont pas pu être enregistrés: ${errors.join(', ')}`;
    }
  } catch (error) {
    console.error("Erreur générale lors de l'ajout des documents:", error);
    errorMessage.value = "Erreur lors de l'ajout des documents. Veuillez réessayer.";
  } finally {
    loading.value = false;
  }
};
</script>