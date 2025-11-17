<template>
  <v-app>
    <v-main>
      <v-container class="py-5">
        <v-card class="pa-4">
          <h1 class="text-primary text-center">Clôturer le bon de travail</h1>

          <v-row>
            <!-- Colonne de gauche avec les informations -->
            <v-col cols="6">
              <v-row>
                <!-- Champ NomIntervention -->
                <v-col cols="12">
                  <p><strong>Nom Intervention :</strong> {{ intervention.nomIntervention }}</p>
                </v-col>
                <!-- Switch Champ interventionCurative -->
                <v-col cols="12">
                  <p><strong>Intervention Curative ? :</strong> {{ intervention.interventionCurative ? 'Oui' : 'Non' }}</p>
                </v-col>
                <!-- Champ DateAssignation -->
                <v-col cols="12">
                  <p><strong>Date Assignation :</strong> {{ intervention.dateAssignation }}</p>
                </v-col>
                <!-- Champ DebutIntervention -->
                <v-col cols="12">
                  <p><strong>Date début Intervention :</strong> {{ intervention.dateDebutIntervention || 'Non spécifié' }}</p>
                </v-col>
                <!-- Champ FinIntervention -->
                <v-col cols="12">
                  <p><strong>Date fin Intervention :</strong> {{ intervention.dateFinIntervention || 'Non spécifié' }}</p>
                </v-col>
                <!-- Champ Responsable -->
                <v-col cols="12">
                  <p><strong>Nom du Responsable :</strong> {{ intervention.responsable || 'Non spécifié' }}</p>
                </v-col>
              </v-row>
            </v-col>

            <!-- Colonne de droite avec le commentaire -->
            <v-col cols="6">
              <p><strong>Commentaire :</strong></p>
              <p>{{ intervention.commentaireIntervention }}</p>
            </v-col>
          </v-row>

          <!-- Boutons -->
          <v-row justify="center" class="mt-4">
            <v-btn color="primary" class="text-white mx-2" @click="cancelCloture">
              Annuler
            </v-btn>
            <v-btn color="error" class="text-white mx-2" @click="refuseCloture">
              Refuser
            </v-btn>
            <v-btn color="success" class="text-white mx-2" @click="validationCloture">
              Valider
            </v-btn>
          </v-row>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

export default {
  name: 'CloseIntervention',
  setup() {
    const router = useRouter();
    const api = useApi(API_BASE_URL);
    const intervention = reactive({
      nomIntervention: "",
      interventionCurative: false,
      dateAssignation: "",
      dateDebutIntervention: null,
      dateFinIntervention: null,
      responsable: "", // Ajout de la propriété pour le responsable
      commentaireIntervention: "",
    });

    const fetchData = async () => {
      try {
        const interventionsRes = await api.get('interventions/');

        if (interventionsRes && interventionsRes.length > 0) {
          // Assigner les données du premier élément du tableau intervention
          Object.assign(intervention, interventionsRes[0]);
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des données:', error);
      }
    };

    // Annuler la cloture du bon de travail
    const cancelCloture = () => {
      router.push('/');
    };

    // Refuser la cloture du bon de travail
    const refuseCloture = () => {
      router.push('/');
    };

    // Valider la cloture du bon de travail
    const validationCloture = () => {
      router.push('/');
    };

    onMounted(fetchData);

    return {
      intervention, // Exposez l'objet intervention
      cancelCloture,
      refuseCloture,
      validationCloture,
    };
  },
};
</script>