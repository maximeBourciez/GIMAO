<template>
  <v-app>
    <v-main>
      <v-container>
        <!-- Section d'information sur la défaillance -->
        <v-row>
          <v-col cols="12">
            <v-card elevation="1" class="rounded-lg pa-4 mb-4">
              <h1 class="text-primary text-center mb-4">Demande d'intervention</h1>
              <v-row>
                <v-col cols="6">
                  <div class="mb-3">
                    <strong>Equipement:</strong> {{ recoveredInformation.designation }}
                  </div>
                  <div class="mb-3">
                    <strong>Salle:</strong> {{ recoveredInformation.nomLieu }}
                  </div>
                  <div class="mb-3">
                    <strong>Etat de la machine:</strong>
                    <v-chip :color="getFailureLevelColor(recoveredInformation.statutEquipement)" dark class="ml-2">
                      {{ recoveredInformation.statutEquipement }}
                    </v-chip>
                  </div>
                </v-col>

                <v-col cols="6">
                  <div>
                    <strong>Informations sur la défaillance</strong>
                    <p class="mt-2">{{ recoveredInformation.commentaireDefaillance }}</p>
                  </div>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>

        <!-- Formulaire d'intervention -->
        <BaseForm v-model="formData" title="Informations du bon de travail" :loading="loading"
          :error-message="errorMessage" :success-message="successMessage"
          :loading-message="loadingData ? 'Chargement des données...' : ''" :custom-validation="validateForm"
          submit-button-text="Valider" submit-button-color="success" @submit="handleSubmit">
          <template #default="{ formData }">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field v-model="formData.intervention_name" label="Nom du bon de travail" outlined dense required
                  :rules="validation.getFieldRules('intervention_name')"></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field v-model="formData.start_date" label="Date de début d'intervention" type="datetime-local"
                  outlined dense required :rules="validation.getFieldRules('start_date')"></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-switch v-model="formData.curative_intervention" label="Intervention Curative" color="primary"
                  inset></v-switch>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field v-model="formData.estimated_time" label="Temps estimé (en heures)" type="number" outlined
                  dense min="0" step="1" hint="Facultatif" persistent-hint></v-text-field>
              </v-col>

              <v-col cols="12">
                <v-textarea v-model="formData.comment_to_fill_in" label="Commentaire" rows="8" outlined required
                  :rules="validation.getFieldRules('comment_to_fill_in')"></v-textarea>
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
import BaseForm from '@/components/BaseForm.vue';
import { useApi } from '@/composables/useApi';
import { useFormValidation } from '@/composables/useFormValidation';
import { getFailureLevelColor } from '@/utils/helpers';
import { API_BASE_URL } from '@/utils/constants';
import '@/assets/css/global.css';

const router = useRouter();
const route = useRoute();
const failureApi = useApi(API_BASE_URL);
const usersApi = useApi(API_BASE_URL);
const interventionApi = useApi(API_BASE_URL);

const loading = ref(false);
const loadingData = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const recoveredInformation = ref({
  designation: '',
  nomLieu: '',
  commentaireDefaillance: '',
  statutEquipement: ''
});

const formData = ref({
  intervention_name: '',
  start_date: '',
  curative_intervention: false,
  estimated_time: null,
  comment_to_fill_in: ''
});

const technicians = ref([]);

const validation = useFormValidation(formData, {
  intervention_name: [v => !!v || 'Le nom du bon de travail est requis'],
  start_date: [v => !!v || 'La date de début est requise'],
  comment_to_fill_in: [v => !!v || 'Le commentaire est requis']
});

const validateForm = () => {
  return validation.checkRequiredFields(['intervention_name', 'start_date', 'comment_to_fill_in']);
};

const fetchData = async () => {
  loadingData.value = true;
  errorMessage.value = '';

  try {
    const failure_id = route.params.id;
    if (!failure_id) {
      throw new Error('ID de défaillance manquant');
    }

    await Promise.all([
      failureApi.get(`defaillance/${failure_id}/affichage/`),
      usersApi.get('utilisateurs/')
    ]);

    const failureData = failureApi.data.value;
    const usersData = usersApi.data.value;

    if (failureData) {
      recoveredInformation.value = {
        designation: failureData.equipement.designation,
        nomLieu: failureData.equipement.lieu.nomLieu,
        commentaireDefaillance: failureData.commentaireDefaillance,
        statutEquipement: failureData.equipement.dernier_statut.statutEquipement
      };
    }

    if (usersData) {
      technicians.value = usersData
        .filter(user => user.role === 'Technicien')
        .map(tech => ({
          text: `${tech.prenom} ${tech.nom}`,
          value: tech.id
        }));
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
    const interventionData = {
      nomIntervention: formData.value.intervention_name,
      interventionCurative: formData.value.curative_intervention,
      dateAssignation: new Date().toISOString(),
      dateCloture: null,
      dateDebutIntervention: formData.value.start_date,
      dateFinIntervention: null,
      tempsEstime: formData.value.estimated_time
        ? `${formData.value.estimated_time.toString().padStart(2, '0')}:00:00`
        : null,
      commentaireIntervention: formData.value.comment_to_fill_in,
      commentaireRefusCloture: null,
      defaillance: parseInt(route.params.id),
      createurIntervention: 1,
      responsable: 1
    };

    await interventionApi.post('interventions/', interventionData);
    successMessage.value = 'Intervention créée avec succès !';

    setTimeout(() => {
      router.push({ name: 'Dashboard' });
    }, 1500);
  } catch (error) {
    console.error('Erreur lors de la création de l\'intervention:', error);
    errorMessage.value = "Erreur lors de la création de l'intervention. Veuillez réessayer.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.text-primary {
  color: #05004E;
}
</style>
