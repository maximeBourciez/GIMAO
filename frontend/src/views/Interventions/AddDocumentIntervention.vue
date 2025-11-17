<template>
  <v-container>
    <v-card>
      <v-card-title>Ajouter un/des documents à l'intervention</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submit_form">
          <v-container>
            <v-row v-for="(document, index) in documents" :key="index">
              <v-col cols="5">
                <v-text-field
                  v-model="document.name"
                  label="Nom du document"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="5">
                <v-file-input
                  v-model="document.file"
                  label="Fichier"
                  required
                ></v-file-input>
              </v-col>
              <v-col cols="2">
                <v-btn color="error" @click="remove_document(index)" icon>
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
          <v-btn color="secondary" @click="go_back" class="mb-4 mr-2">
            Retour
          </v-btn>
          
          <v-btn color="secondary" @click="add_document" class="mb-4">
            Ajouter un autre document
          </v-btn>
          <v-btn type="submit" color="primary" block>Sauvegarder les documents</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
    <v-snackbar v-model="snackbar.show" :color="snackbar.color">
      {{ snackbar.message }}
    </v-snackbar>
  </v-container>
</template>

<script>
import { ref, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

export default {
  name: 'AddDocumentIntervention',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const api = useApi(API_BASE_URL);
    const documents = ref([{ name: '', file: null }]);
    const snackbar = reactive({
      show: false,
      message: '',
      color: 'success'
    });

    const add_document = () => {
      documents.value.push({ name: '', file: null });
    };

    const go_back = () => {
      router.go(-1);
    };

    const remove_document = (index) => {
      documents.value.splice(index, 1);
    };

    const show_snackbar = (message, color = 'success') => {
      snackbar.message = message;
      snackbar.color = color;
      snackbar.show = true;
    };

    const submit_form = async () => {
      try {
        const intervention_id = route.params.id;
        let all_success = true;

        for (const doc of documents.value) {
          if (doc.name && doc.file) {
            const formData = new FormData();
            formData.append('nomDocumentIntervention', doc.name);
            formData.append('lienDocumentIntervention', doc.file);
            formData.append('intervention', intervention_id);

            try {
              const response = await api.post('document-interventions/', formData);
            } catch (error) {
              console.error('Error while adding the document:', error);
              all_success = false;
            }
          }
        }

        if (all_success) {
          show_snackbar('All documents have been saved successfully');
          router.push({ name: 'InterventionDetail', params: { id: intervention_id } });
        } else {
          show_snackbar('Some documents could not be saved', 'warning');
        }
      } catch (error) {
        console.error('General error while adding documents:', error);
        show_snackbar('Error while adding documents. Please try again.', 'error');
      }
    };

    return {
      documents,
      add_document,
      remove_document,
      submit_form,
      snackbar,
      go_back
    };
  },
};
</script>

<style scoped>
/* add specific styles here if necessary */
</style>