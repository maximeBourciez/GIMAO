<template>
  <v-container>
    <v-card>
      <v-card-title>Ajouter des documents à la demande d'intervention</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submit_form">
          <v-container>
            <v-row v-for="(document, index) in documents" :key="index">
              <v-col cols="5">
                <v-text-field
                  v-model="document.document_name"
                  label="Nom du document"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="5">
                <v-file-input
                  v-model="document.document_file"
                  label="Fichier du document"
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
          <v-btn type="submit" color="primary" block>Enregistrer tous les documents</v-btn>
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
import api from '@/services/api';

export default {
  name: 'AddDocumentFailure',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const documents = ref([{ document_name: '', document_file: null }]);
    const snackbar = reactive({
      show: false,
      message: '',
      color: 'success'
    });

    const add_document = () => {
      documents.value.push({ document_name: '', document_file: null });
    };

    const go_back = () => {
      router.go(-1);
    };

    const remove_document = (index) => {
      documents.value.splice(index, 1);
    };

    const showSnackbar = (message, color = 'success') => {
      snackbar.message = message;
      snackbar.color = color;
      snackbar.show = true;
    };

    const submit_form = async () => {
      try {
        const failure_id = route.params.id;
        let allSuccess = true;

        for (const doc of documents.value) {
          if (doc.document_name && doc.document_file) {
            const formData = new FormData();
            formData.append('nomDocumentDefaillance', doc.document_name);
            formData.append('lienDocumentDefaillance', doc.document_file);
            formData.append('defaillance', failure_id);

            try {
              const response = await api.postDefaillanceDocument(formData);
            } catch (error) {
              console.error("Erreur lors de l'ajout du document:", error);
              allSuccess = false;
            }
          }
        }

        if (allSuccess) {
          showSnackbar('Tous les documents ont été enregistrés avec succès');
          router.push({ name: 'FailureDetail', params: { id: failure_id } });
        } else {
          showSnackbar("Certains documents n'ont pas pu être enregistrés", 'warning');
        }
      } catch (error) {
        console.error("Erreur générale lors de l'ajout des documents:", error);
        showSnackbar("Erreur lors de l'ajout des documents. Veuillez réessayer.", 'error');
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
/* Vous pouvez ajouter des styles spécifiques ici si nécessaire */
</style>