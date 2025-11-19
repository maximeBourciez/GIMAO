<template>
  <BaseDetailView title="Détail de la Défaillance" :data="defaillance" :loading="loading" :error-message="errorMessage"
    :success-message="successMessage" :auto-display="false" :show-edit-button="false" :show-delete-button="canDelete"
    @delete="handleDelete" @clear-error="errorMessage = ''" @clear-success="successMessage = ''">
    <!-- Contenu personnalisé -->
    <template #default="{ data }">
      <v-row v-if="data">
        <!-- Colonne gauche: Informations défaillance -->
        <v-col cols="12" md="6">
          <h3 class="text-h6 mb-4 text-primary">Informations de la défaillance</h3>

          <div class="detail-field">
            <label class="detail-label">Description</label>
            <div class="detail-value">{{ data.commentaireDefaillance }}</div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Niveau</label>
            <div class="detail-value">
              <v-chip :color="getFailureLevelColor(data.niveau)" dark>
                {{ data.niveau }}
              </v-chip>
            </div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Traitée</label>
            <div class="detail-value">
              <v-chip :color="data.dateTraitementDefaillance ? 'green' : 'red'" dark>
                {{ data.dateTraitementDefaillance ? 'Oui' : 'Non' }}
              </v-chip>
            </div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Changer le statut de l'équipement</label>
            <v-select v-model="selectedStatus" :items="statusOptions" outlined dense></v-select>
          </div>

          <v-row class="mt-4">
            <v-col>
              <v-btn color="success" block :disabled="canTreat" @click="handleCreateIntervention">
                <v-icon left>mdi-wrench</v-icon>
                Transformer en bon de travail
              </v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn color="warning" block :disabled="!canTreat" @click="handleTreatFailure">
                Mettre en attente la demande
              </v-btn>
            </v-col>
          </v-row>
        </v-col>

        <!-- Colonne droite: Équipement et Documents -->
        <v-col cols="12" md="6">
          <!-- Section Équipement -->
          <v-card elevation="2" class="mb-4">
            <v-card-title class="d-flex align-center">
              <span>Équipement</span>
              <v-spacer></v-spacer>
              <v-btn color="primary" size="small" @click="openEquipment" :disabled="!data.equipement">
                Détails
              </v-btn>
              <v-btn icon size="small" @click="showEquipmentDetails = !showEquipmentDetails">
                <v-icon>
                  {{ showEquipmentDetails ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                </v-icon>
              </v-btn>
            </v-card-title>

            <v-expand-transition>
              <v-card-text v-show="showEquipmentDetails" v-if="data.equipement">
                <div class="detail-field" v-for="(value, key) in formattedEquipmentLabel" :key="key">
                  <label class="detail-label">{{ key }}</label>
                  <div class="detail-value">{{ value }}</div>
                </div>
              </v-card-text>
            </v-expand-transition>
          </v-card>

          <!-- Section Documents -->
          <v-card elevation="2">
            <v-card-title class="d-flex align-center">
              <span>Documents de la défaillance</span>
              <v-spacer></v-spacer>
              <v-btn color="primary" size="small" @click="handleAddDocument">
                <v-icon left>mdi-plus</v-icon>
                Ajouter
              </v-btn>
              <v-btn icon size="small" @click="showDocumentsDetails = !showDocumentsDetails">
                <v-icon>
                  {{ showDocumentsDetails ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                </v-icon>
              </v-btn>
            </v-card-title>

            <v-expand-transition>
              <v-card-text v-show="showDocumentsDetails">
                <div class="d-flex justify-end mb-2">
                  <v-btn size="small" @click="toggleActionMode">
                    {{ actionMode === 'download' ? 'Mode suppression' : 'Mode téléchargement' }}
                  </v-btn>
                </div>

                <v-data-table :headers="documentHeaders" :items="data.liste_documents_defaillance || []"
                  class="elevation-1" hide-default-footer :items-per-page="-1">
                  <template #item.actions="{ item }">
                    <v-btn icon size="small" :color="actionMode === 'download' ? 'primary' : 'error'"
                      @click="actionMode === 'download' ? downloadDocument(item) : deleteDocument(item)">
                      <v-icon>
                        {{ actionMode === 'download' ? 'mdi-download' : 'mdi-delete' }}
                      </v-icon>
                    </v-btn>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-expand-transition>
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
import { getFailureLevelColor } from '@/utils/helpers';
import { API_BASE_URL, BASE_URL } from '@/utils/constants';

const router = useRouter();
const route = useRoute();
const failureApi = useApi(API_BASE_URL);
const equipmentApi = useApi(API_BASE_URL);
const patchApi = useApi(API_BASE_URL);

const defaillance = ref(null);
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const showEquipmentDetails = ref(false);
const showDocumentsDetails = ref(false);
const actionMode = ref('download');
const selectedStatus = ref('pas de changement');

const statusOptions = [
  'pas de changement',
  'En fonctionnement',
  'Dégradé',
  "À l'arrêt"
];

const documentHeaders = [
  { title: 'Nom du document', key: 'nomDocumentDefaillance' },
  { title: 'Actions', key: 'actions', sortable: false }
];

const canDelete = computed(() => !defaillance.value?.dateTraitementDefaillance);
const canTreat = computed(() => !defaillance.value?.dateTraitementDefaillance);

const formattedEquipmentLabel = computed(() => {
  if (!defaillance.value?.equipement) return {};
  const eq = defaillance.value.equipement;
  return {
    'Référence': eq.reference || 'Non spécifié',
    'Désignation': eq.designation || 'Non spécifié',
    'Lieu': eq.lieu?.nomLieu || 'Non spécifié',
    'Statut': eq.dernier_statut?.statutEquipement || 'Non spécifié'
  };
});

const fetchData = async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    const response = await failureApi.get(`defaillance/${route.params.id}/affichage/`);
    const defaillanceData = response;

    if (defaillanceData.equipement && typeof defaillanceData.equipement === 'object') {
      defaillanceData.equipement.dernier_statut = defaillanceData.equipement.dernier_statut || {};
    } else if (typeof defaillanceData.equipement === 'string') {
      const equipementResponse = await equipmentApi.get(`equipement/${defaillanceData.equipement}/affichage/`);
      defaillanceData.equipement = equipementResponse;
      defaillanceData.equipement.dernier_statut = defaillanceData.equipement.dernier_statut || {};
    } else {
      defaillanceData.equipement = { dernier_statut: {} };
    }

    defaillance.value = defaillanceData;
  } catch (error) {
    console.error('Erreur lors de la récupération des données:', error);
    errorMessage.value = 'Erreur lors du chargement des données';
  } finally {
    loading.value = false;
  }
};

const handleDelete = async () => {
  if (confirm('Êtes-vous sûr de vouloir supprimer cette défaillance ?')) {
    try {
      await patchApi.delete(`defaillances/${route.params.id}/`);
      successMessage.value = 'Défaillance supprimée avec succès';
      setTimeout(() => router.push({ name: 'FailureList' }), 1500);
    } catch (error) {
      errorMessage.value = 'Erreur lors de la suppression';
    }
  }
};

const handleTreatFailure = async () => {
  try {
    await patchApi.patch(`defaillances/${route.params.id}/`, {
      dateTraitementDefaillance: new Date().toISOString()
    });
    successMessage.value = 'Défaillance mise en attente';
    await fetchData();
  } catch (error) {
    errorMessage.value = 'Erreur lors de la mise à jour';
  }
};

const handleCreateIntervention = () => {
  router.push({ name: 'CreateIntervention', params: { id: route.params.id } });
};

const openEquipment = () => {
  if (defaillance.value?.equipement?.reference) {
    router.push({
      name: 'EquipmentDetail',
      params: { reference: defaillance.value.equipement.reference }
    });
  }
};

const handleAddDocument = () => {
  router.push({
    name: 'AddDocumentFailure',
    params: { id: route.params.id }
  });
};

const toggleActionMode = () => {
  actionMode.value = actionMode.value === 'download' ? 'delete' : 'download';
};

const downloadDocument = async (item) => {
  try {
    const response = await fetch(`${BASE_URL}${item.lienDocumentDefaillance}`);
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = item.nomDocumentDefaillance;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    successMessage.value = 'Document téléchargé';
  } catch (error) {
    errorMessage.value = 'Erreur lors du téléchargement';
  }
};

const deleteDocument = async (item) => {
  if (confirm(`Êtes-vous sûr de vouloir supprimer le document "${item.nomDocumentDefaillance}" ?`)) {
    try {
      // TODO: Implémenter l'API de suppression de document
      await fetchData();
      successMessage.value = 'Document supprimé';
    } catch (error) {
      errorMessage.value = 'Erreur lors de la suppression du document';
    }
  }
};

onMounted(() => {
  fetchData();
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
</style>
