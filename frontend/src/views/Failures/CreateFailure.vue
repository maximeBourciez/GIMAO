<template>
  <v-app>
    <v-main>
      <v-container>
        <BaseForm v-model="formData" title="Créer une Demande d'intervention" :loading="loading" :error-message="errorMessage"
          :success-message="successMessage" :loading-message="loadingData ? 'Chargement des données...' : ''"
          :custom-validation="validateForm" submit-button-text="Valider" submit-button-color="success" @submit="handleSubmit">
          <template #default="{ formData }">


            <v-row>
              <v-col cols="12" md="6">
                <v-text-field v-model="formData.nom" label="Nom de la demande d'intervention *" outlined required
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

              <!-- Documents -->
              <v-col cols="12">
                <v-sheet class="pa-4 mb-4" elevation="1" rounded>
                  <h4 class="mb-3">Documents</h4>

                  <v-row v-for="(doc, index) in formData.documents" :key="index" dense class="mb-3 align-center">
                    <v-col cols="4">
                      <v-text-field v-model="doc.nomDocument" label="Titre *" outlined dense hide-details />
                    </v-col>

                    <v-col cols="4">
                      <v-file-input v-model="doc.file" dense outlined show-size label="Document *"
                        hide-details prepend-icon="" prepend-inner-icon="mdi-paperclip"></v-file-input>
                    </v-col>

                    <v-col cols="3">
                      <v-select v-model="doc.typeDocument" :items="typesDocuments" item-title="nomTypeDocument"
                        item-value="id" label="Type *" outlined dense hide-details />
                    </v-col>

                    <v-col cols="1" class="d-flex justify-center">
                      <v-btn icon color="error" size="small" @click="removeDocument(index)">
                        <v-icon>mdi-delete</v-icon>
                      </v-btn>
                    </v-col>
                  </v-row>

                  <v-btn color="primary" variant="outlined" class="mt-2" @click="addDocument">
                    <v-icon left>mdi-plus</v-icon>
                    Ajouter un document
                  </v-btn>
                </v-sheet>
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
const documentsApi = useApi(API_BASE_URL);

const loading = ref(false);
const loadingData = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const equipments = ref([]);
const typesDocuments = ref([]);
const equipmentReference = ref(null);
const connectedUser = computed(() => store.getters.currentUser);

const formData = ref({
  equipement_id: null,
  commentaire: '',
  nom: '',
  documents: []
});

const validation = useFormValidation(formData, {
  nom: [v => !!v || 'Le nom est requis'],
  equipement_id: [v => !!v || "L'équipement est requis"],
  commentaire: [
    v => !v || v.length <= 300 || 'Le commentaire ne doit pas dépasser 300 caractères'
  ]
});

const validateForm = () => {
  return validation.validateAll(formData.value);
};

const addDocument = () => {
  formData.value.documents.push({
    nomDocument: '',
    file: null,
    typeDocument: null
  });
};

const removeDocument = (index) => {
  formData.value.documents.splice(index, 1);
};

const fetchData = async () => {
  loadingData.value = true;
  errorMessage.value = '';

  try {
    const [equipmentsResponse, typesDocumentsResponse] = await Promise.all([
      equipmentsApi.get('equipements/'),
      documentsApi.get('types-documents/')
    ]);
    
    equipments.value = equipmentsResponse;
    typesDocuments.value = typesDocumentsResponse;
    console.log(typesDocuments.value);

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
    // Utilisation de FormData pour envoyer les fichiers
    const formDataToSend = new FormData();
    formDataToSend.append('nom', formData.value.nom);
    formDataToSend.append('commentaire', formData.value.commentaire || '');
    formDataToSend.append('equipement_id', formData.value.equipement_id);
    formDataToSend.append('utilisateur_id', connectedUser.value.id);

    // Préparation des documents (métadonnées en JSON, fichiers séparés)
    const validDocs = formData.value.documents
      .filter(doc => doc.file && doc.typeDocument && doc.nomDocument);

    if (validDocs.length > 0) {
      const docMetadata = validDocs.map((doc, index) => ({
        nomDocument: doc.nomDocument,
        typeDocument_id: doc.typeDocument
      }));
      formDataToSend.append('documents', JSON.stringify(docMetadata));

      // Ajouter chaque fichier avec la convention document_{index}
      validDocs.forEach((doc, index) => {
        const file = doc.file[0] || doc.file;
        formDataToSend.append(`document_${index}`, file);
      });
    }

    console.log('FormData entries:');
    for (let [key, value] of formDataToSend.entries()) {
      console.log(key, value);
    }

    const response = await api.post('demandes-intervention/', formDataToSend, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    const newFailureId = response.id;

    successMessage.value = 'Demande d\'intervention créée avec succès !';

    setTimeout(() => {
      router.push({ name: 'FailureDetail', params: { id: newFailureId } });
    }, 1500);
  } catch (error) {
    console.error('Erreur lors de la création de la Demande d\'intervention:', error);
    errorMessage.value = 'Une erreur est survenue lors de la création de la demande d\'intervention.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchData();
});
</script>
