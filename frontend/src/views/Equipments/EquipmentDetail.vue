<template>
  <BaseDetailView :title="equipement.designation || 'Détail de l\'équipement'" :data="equipement" :loading="isLoading"
    :error-message="errorMessage" :success-message="successMessage" :auto-display="false" :show-edit-button="false"
    :show-delete-button="false" @clear-error="errorMessage = ''" @clear-success="successMessage = ''">
    <template #default="{ data }">
      <v-row v-if="data">
        <!-- Section gauche : Détails de l'équipement -->
        <v-col cols="12" md="6">
          <h3 class="text-h6 mb-4 text-primary">Description de l'équipement</h3>

          <div v-for="(value, key) in equipmentDetails" :key="key" class="detail-field">
            <label class="detail-label">{{ formatLabel(key) }}</label>
            <div class="detail-value">
              <v-chip v-if="key === 'statut'" :color="getStatusColor(value)" dark size="small">
                {{ value }}
              </v-chip>
              <span v-else>{{ formatValue(value) }}</span>
            </div>
          </div>


          <!-- Section documentation -->
          <v-card elevation="2" class="mt-4">
            <v-card-title class="text-h6">Documentation</v-card-title>
            <v-divider></v-divider>

            <!-- Documents techniques -->
            <v-card-text>
              <h4 class="mb-2">Documents techniques</h4>
              <v-data-table :headers="technicalDocumentsHeaders" :items="data.liste_documents_techniques || []"
                class="elevation-1 mb-4" hide-default-footer>
                <template #item.action="{ item }">
                  <v-btn icon size="small" color="primary"
                    @click="downloadDocument(item.lienDocumentTechnique, item.nomDocumentTechnique)">
                    <v-icon>mdi-download</v-icon>
                  </v-btn>
                </template>
              </v-data-table>

              <!-- Autres documents -->
              <h4 class="mb-2 mt-4">Autres documents</h4>
              <v-data-table :headers="othersDocumentsHeaders" :items="othersDocuments" class="elevation-1"
                hide-default-footer>
                <template #item.action="{ item }">
                  <v-btn icon size="small" color="primary"
                    @click="downloadDocument(item.lienDocument, item.nomDocument)">
                    <v-icon>mdi-download</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Section droite : Image, consommables, interventions et actions -->
        <v-col cols="12" md="6">
          <!-- Section image -->
          <v-card elevation="2" class="mb-4">
            <v-img :src="data.lienImageEquipement" aspect-ratio="4/3" class="rounded-lg" style="max-height: 30vh;"
              alt="Image de l'équipement"></v-img>
          </v-card>

          <!-- Boutons d'action -->
          <v-card elevation="2" class="mb-4">
            <v-card-actions class="justify-center pa-4">
              <v-btn color="warning" prepend-icon="mdi-alert-circle" @click="signalFailure">
                Signaler une défaillance
              </v-btn>
            </v-card-actions>
          </v-card>

          <!-- Section consommables -->
          <v-card elevation="2" class="mb-4">
            <v-card-title class="text-h6">Consommables</v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <v-data-table :items="data.liste_consommables || []" :headers="consumableHeaders" class="elevation-1"
                hide-default-footer></v-data-table>
            </v-card-text>
          </v-card>

          <!-- Historique des interventions -->
          <v-card elevation="2">
            <v-card-title class="text-h6">Interventions</v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <v-data-table :items="data.liste_interventions || []" :headers="interventionsHeaders" class="elevation-1"
                hide-default-footer>
                <template #item.dateAssignation="{ item }">
                  {{ formatDate(item.dateAssignation) }}
                </template>
                <template #item.action="{ item }">
                  <v-btn icon size="small" @click="viewIntervention(item)">
                    <v-icon>mdi-eye</v-icon>
                  </v-btn>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </BaseDetailView>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BaseDetailView from '@/components/common/BaseDetailView.vue';
import { useApi } from '@/composables/useApi';
import { getStatusColor } from '@/utils/helpers';
import { API_BASE_URL, BASE_URL } from '@/utils/constants';

const router = useRouter();
const route = useRoute();
const api = useApi(API_BASE_URL);

const equipement = computed(() => api.data.value || {});
const isLoading = computed(() => api.loading.value);
const errorMessage = ref('');
const successMessage = ref('');

const technicalDocumentsHeaders = [
  { title: 'Document technique', key: 'nomDocumentTechnique', align: 'start' },
  { title: 'Télécharger', key: 'action', align: 'start', sortable: false }
];

const othersDocumentsHeaders = [
  { title: 'Type', key: 'type', align: 'start' },
  { title: 'Document', key: 'nomDocument', align: 'start' },
  { title: 'Télécharger', key: 'action', align: 'start', sortable: false }
];

const consumableHeaders = [
  { title: 'Désignation', key: 'designation' },
  { title: 'Fabricant', key: 'fabricant.nomFabricant' }
];

const interventionsHeaders = [
  { title: 'Nom', key: 'nomIntervention' },
  { title: "Date d'assignation", key: 'dateAssignation' },
  { title: 'Visualiser', key: 'action', align: 'start' }
];

const equipmentDetails = computed(() => {
  if (!equipement.value) return {};
  const {
    reference, designation, dateMiseEnService, prixAchat,
    preventifGlissant, joursIntervalleMaintenance
  } = equipement.value;
  const lieu = equipement.value.lieu?.nomLieu || '';
  const modele = equipement.value.modeleEquipement?.nomModeleEquipement || '';
  const fournisseur = equipement.value.fournisseur?.nomFournisseur || '';
  const fabricant = equipement.value.fabricant?.nomFabricant || '';
  const statut = equipement.value.dernier_statut?.statutEquipement || '';

  return {
    reference, designation, dateMiseEnService, prixAchat,
    preventifGlissant, joursIntervalleMaintenance,
    lieu, modele, fournisseur, fabricant, statut
  };
});

const othersDocuments = computed(() => {
  const documentsFailure = (equipement.value.liste_documents_defaillance || []).map(doc => ({
    type: 'Demande de BT',
    nomDocument: doc.nomDocumentDefaillance,
    lienDocument: doc.lienDocumentDefaillance
  }));
  const documentsIntervention = (equipement.value.liste_documents_intervention || []).map(doc => ({
    type: 'Intervention',
    nomDocument: doc.nomDocumentIntervention,
    lienDocument: doc.lienDocumentIntervention
  }));
  return [...documentsFailure, ...documentsIntervention];
});

const fetchEquipmentData = async () => {
  errorMessage.value = '';
  try {
    await api.get(`equipement/${route.params.reference}/affichage/`);
  } catch (error) {
    console.error("Erreur lors de la récupération des données de l'équipement:", error);
    errorMessage.value = "Erreur lors du chargement de l'équipement";
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  }).replace(',', '');
};

const formatLabel = (key) => {
  const labels = {
    reference: 'Référence',
    designation: 'Désignation',
    dateMiseEnService: 'Date de mise en service',
    prixAchat: "Prix d'achat",
    preventifGlissant: 'Préventif glissant',
    joursIntervalleMaintenance: 'Intervalle de maintenance (jours)',
    lieu: 'Lieu',
    modele: 'Modèle',
    fournisseur: 'Fournisseur',
    fabricant: 'Fabricant',
    statut: 'Statut'
  };
  return labels[key] || key;
};

const formatValue = (value) => {
  if (typeof value === 'boolean') {
    return value ? 'Oui' : 'Non';
  }
  if (typeof value === 'number') {
    return value.toLocaleString();
  }
  return value || '-';
};

const viewIntervention = (intervention) => {
  router.push({
    name: 'InterventionDetail',
    params: { id: intervention.id }
  });
};

const signalFailure = () => {
  router.push({
    name: 'CreateFailure',
    params: { equipementReference: equipement.value.reference }
  });
};

const downloadDocument = async (lien, nomFichier) => {
  try {
    const cleanedLink = lien.startsWith('/media/') ? lien : `/media/${lien.split('/media/').pop()}`;
    const fullUrl = `${BASE_URL}${cleanedLink}`;

    const response = await fetch(fullUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = nomFichier;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);

    successMessage.value = 'Document téléchargé avec succès';
  } catch (error) {
    console.error('Erreur lors du téléchargement:', error);
    errorMessage.value = 'Erreur lors du téléchargement du fichier';
  }
};

onMounted(() => {
  fetchEquipmentData();
});
</script>

<style scoped>
.detail-field {
  margin-bottom: 16px;
}

.detail-label {
  display: block;
  font-weight: 600;
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 1rem;
  color: #333;
  padding: 8px 0;
  border-bottom: 1px solid #e0e0e0;
}

.text-primary {
  color: #05004E;
}
</style>
