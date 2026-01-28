<template>
  <BaseDetailView :data="defaillance" :loading="loading" :error-message="errorMessage" :title="'Détail de la demande d\'intervention'"
    :success-message="successMessage" :auto-display="false" :show-edit-button="false"
    @delete="handleDelete" @clear-error="errorMessage = ''" @clear-success="successMessage = ''">
    <!-- Contenu personnalisé -->
    <template #default="{ data }">
      <v-row v-if="data">
        <!-- Colonne gauche: Demande d'intervention -->
        <v-col cols="12" md="6">
          <h3 class="text-h6 mb-4 text-primary">{{ data.nom }}</h3>

          <div class="detail-field">
            <label class="detail-label">Commentaire</label>
            <div class="detail-value">{{ data.commentaire }}</div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Statut</label>
            <div class="detail-value">
              <v-chip :color="data.statut ? FAILURE_STATUS_COLORS[data.statut] : 'grey'" dark>
                {{ FAILURE_STATUS[data.statut] }}
              </v-chip>
            </div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Créateur</label>
            <div class="detail-value">{{ data.utilisateur.prenom ?? ''}} {{data.utilisateur.nomFamille ?? '' }}</div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Date de création</label>
            <div class="detail-value">{{ formatDate(data.date_creation) }}</div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Date de changement de statut</label>
            <div class="detail-value">{{ formatDate(data.date_changementStatut) }}</div>
          </div>


          
          <v-row>
            <v-col cols="12">
              <v-btn color="primary" block :disabled="!canCreateIntervention" @click="openCreateInterventionModal">
                <v-icon class="mx-2" left>mdi-wrench</v-icon>
                Transformer en bon de travail
              </v-btn>
            </v-col>
            <v-col cols="6">
              <v-btn color="success" block :disabled="!canAccept" @click="openAcceptModal">
                Accepter la demande
              </v-btn>
            </v-col>
            <v-col cols="6">
              <v-btn color="error" block :disabled="!canClose" @click="openRejectModal">
                Refuser la demande
              </v-btn>
            </v-col>
          </v-row>
        </v-col>

        <!-- Colonne droite: Équipement et Documents -->
        <v-col cols="12" md="6">
          <!-- Section Équipement -->
          <v-card elevation="2" class="mb-4">
            <v-card-title class="d-flex align-center"  @click="showEquipmentDetails = !showEquipmentDetails">
              <span>Équipement</span>
              <v-spacer></v-spacer>
              <v-btn color="primary" class="mr-2" size="small" @click="openEquipment" :disabled="!data.equipement">
                Détails
              </v-btn>
              <v-icon>
                {{ showEquipmentDetails ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
              </v-icon>
            </v-card-title>

            <v-expand-transition>
              <v-card-text v-show="showEquipmentDetails" v-if="data.equipement">
                <div class="detail-field" v-for="(value, key) in formattedEquipmentLabel" :key="key">
                  <label class="detail-label">{{ key }}</label>
                  <div v-if="key !== 'Statut'" class="detail-value">{{ value }}</div>
                  <v-chip v-else :color="getStatusColor(value)" variant="tonal">{{ getStatusLabel(value) }}</v-chip>
                </div>
              </v-card-text>
            </v-expand-transition>
          </v-card>

          <!-- Section Documents -->
          <v-card elevation="2">
            <v-card-title class="d-flex align-center"  @click="showDocumentsDetails = !showDocumentsDetails">
              <span>Documents</span>
              <v-spacer></v-spacer>
              <v-btn color="primary" class="mr-2" size="small" @click="handleAddDocument">
                <v-icon left>mdi-plus</v-icon>
                Ajouter
              </v-btn>
              <v-icon>
                {{ showDocumentsDetails ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
              </v-icon>
            </v-card-title>

            <v-expand-transition>
              <v-card-text v-show="showDocumentsDetails">

                <v-data-table :headers="documentHeaders" :items="data.documentsDI || []"
                  class="elevation-1" hide-default-footer :items-per-page="-1">
                  <template #item.name="{ item }">
                    {{ item.titre }}
                  </template>
                  <template #item.actions="{ item }">
                    <v-btn icon size="small" :color="'primary'" class="mr-2"
                      @click="downloadDocument(item)">
                      <v-icon>
                        mdi-download
                      </v-icon>
                    </v-btn>
                    <v-btn icon size="small" :color="'error'"
                      @click="deleteDocument(item)">
                      <v-icon>
                        mdi-delete
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

  <!-- Modale de confirmation pour accepter la demande -->
  <ConfirmationModal
    v-model="showAcceptModal"
    type="success"
    title="Accepter la demande"
    message="Êtes-vous sûr de vouloir accepter cette demande d'intervention ? \n\nCette action changera le statut de la demande."
    confirm-text="Accepter"
    cancel-text="Annuler"
    confirm-icon="mdi-check"
    :loading="acceptLoading"  
    @confirm="handleChangeStatusFailure('ACCEPTEE')"
    @cancel="showAcceptModal = false"
  />

  <!-- Modale de confirmation pour rejeter la demande -->
  <ConfirmationModal
    v-model="showRejectModal"
    type="error"
    title="Rejeter la demande"
    message="Êtes-vous sûr de vouloir rejeter cette demande d'intervention ? \n\nCette action changera le statut de la demande."
    confirm-text="Rejeter"
    cancel-text="Annuler"
    confirm-icon="mdi-check"
    :loading="rejectLoading"  
    @confirm="handleChangeStatusFailure('REFUSEE')"
    @cancel="showRejectModal = false"
  />

  <!-- Modale de confirmation pour transformer la demande -->
  <ConfirmationModal
    v-model="showCreateInterventionModal"
    type="success"
    title="Transformer la demande"
    message="Êtes-vous sûr de vouloir transformer cette demande d'intervention en bon de travail ? \n\nCette action changera le statut de la demande."
    confirm-text="Transformer"
    cancel-text="Annuler"
    confirm-icon="mdi-check" 
    :loading="createInterventionLoading"  
    @confirm="handleCreateIntervention()"
    @cancel="showCreateInterventionModal = false"
  />

  <!-- Bouton modifier -->
  <v-btn
    v-if="canEditFailure"
    color="primary"
    size="large"
    icon
    class="floating-edit-button"
    elevation="4"
    @click="editCurrentFailure()"
  >
    <v-icon size="large">mdi-pencil</v-icon>
    <v-tooltip activator="parent" location="left">
      Modifier la demande
    </v-tooltip>
  </v-btn>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BaseDetailView from '@/components/common/BaseDetailView.vue';
import ConfirmationModal from '@/components/common/ConfirmationModal.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL, MEDIA_BASE_URL, FAILURE_STATUS, FAILURE_STATUS_COLORS } from '@/utils/constants';
import { useStore } from 'vuex';
import { getStatusColor, getStatusLabel } from '@/utils/helpers';
import { BASE_URL } from '../../utils/constants';

const store = useStore();
const router = useRouter();
const route = useRoute();
const failureApi = useApi(API_BASE_URL);
const equipmentApi = useApi(API_BASE_URL);
const patchApi = useApi(API_BASE_URL);

// Récupération de l'utilisateur connecté
const currentUser = computed(() => store.getters.currentUser);
const userRole = computed(() => store.getters.userRole);

const defaillance = ref(null);
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const showEquipmentDetails = ref(false);
const showDocumentsDetails = ref(false);
const actionMode = ref('download');
const selectedStatus = ref('pas de changement');
const showAcceptModal = ref(false);
const acceptLoading = ref(false);
const showRejectModal = ref(false);
const rejectLoading = ref(false);
const showCreateInterventionModal = ref(false);
const createInterventionLoading = ref(false);

const formatDate = (dateString) => {
  if (!dateString) return 'Non spécifié';
  return new Date(dateString).toLocaleString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const documentHeaders = [
  { title: 'Nom du document', key: 'name' },
  { title: 'Actions', key: 'actions', sortable: false }
];

const canClose = computed(() => FAILURE_STATUS[ defaillance.value?.statut] === FAILURE_STATUS.EN_ATTENTE || FAILURE_STATUS[defaillance.value?.statut] === FAILURE_STATUS.ACCEPTEE);
const canCreateIntervention = computed(() => FAILURE_STATUS[defaillance.value?.statut] === FAILURE_STATUS.EN_ATTENTE || FAILURE_STATUS[defaillance.value?.statut] === FAILURE_STATUS.ACCEPTEE);
const canAccept = computed(() => FAILURE_STATUS[defaillance.value?.statut] === FAILURE_STATUS.EN_ATTENTE);

// Permission de modification: rôle "Opérateur" OU créateur de la demande
const canEditFailure = computed(() => {
  if (!currentUser.value || !defaillance.value) return false;
  const isOperateur = userRole.value === 'Opérateur';
  const isCreator = defaillance.value.utilisateur?.id === currentUser.value.id;
  return isOperateur || isCreator;
});

const formattedEquipmentLabel = computed(() => {
  if (!defaillance.value?.equipement) return {};
  const eq = defaillance.value.equipement;
  return {
    'Référence': eq.reference || 'Non spécifié',
    'Désignation': eq.designation || 'Non spécifié',
    'Lieu': eq.lieu || 'Non spécifié',
    'Statut': eq.dernier_statut?.statut || 'Non spécifié'
  };
});

const fetchData = async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    const response = await failureApi.get(`demandes-intervention/${route.params.id}/`);
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
      await patchApi.delete(`demandes-intervention/${route.params.id}/`);
      successMessage.value = 'Défaillance supprimée avec succès';
      setTimeout(() => router.push({ name: 'FailureList' }), 1500);
    } catch (error) {
      errorMessage.value = 'Erreur lors de la suppression';
    }
  }
};

const handleChangeStatusFailure = async (newStatus) => {
  rejectLoading.value = true;
  acceptLoading.value = true;
  try {
    await patchApi.patch(`demandes-intervention/${route.params.id}/updateStatus/`, {
      statut: newStatus
    });
    successMessage.value = 'Demande d\'intervention ' + FAILURE_STATUS[newStatus] + ' avec succès';
    showRejectModal.value = false;
    showAcceptModal.value = false;
    await fetchData();
  } catch (error) {
    switch (newStatus) {
      case 'ACCEPTEE':
          errorMessage.value = 'Erreur lors de l\'acceptation de la demande';
        break;
      case 'REFUSEE':
          errorMessage.value = 'Erreur lors du rejet de la demande';
        break;
      default:
        errorMessage.value = 'Erreur lors du changement du statut de la demande';
    }
    
  } finally {
    rejectLoading.value = false;
    acceptLoading.value = false;
  }
};

const handleCreateIntervention = async () => {
  createInterventionLoading.value = true;
  try {
    const response =await patchApi.post(`demandes-intervention/${route.params.id}/transform_to_bon_travail/`, 
      {
        responsable: store.getters.currentUser.id
      }
    );
    successMessage.value = 'Demande d\'intervention transformée avec succès';
    showCreateInterventionModal.value = false;

    setTimeout(() => {
      router.push({ name: 'InterventionDetail', params: { id: response.id } });
    }, 1500);
  } catch (error) {
    errorMessage.value = 'Erreur lors de la transformation de la demande';
  } finally {
    createInterventionLoading.value = false;
  }
};

// Fonctions pour les modales
const openAcceptModal = () => {
  showAcceptModal.value = true;
};
const openRejectModal = () => {
  showRejectModal.value = true;
};
const openCreateInterventionModal = () => {
  showCreateInterventionModal.value = true;
};

const openEquipment = () => {
  if (defaillance.value?.equipement?.id) {
    router.push({
      name: 'EquipmentDetail',
      params: { id: defaillance.value.equipement.id },
      query:  {from: 'failure', failureID: defaillance.value.id}
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
    const response = await fetch(`${BASE_URL}${MEDIA_BASE_URL}${item.path}`);
    const blob = await response.blob(); 
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = item.path.split('/').pop();
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    successMessage.value = 'Document téléchargé';
  } catch (error) {
    console.log(error);
    errorMessage.value = 'Erreur lors du téléchargement';
  }
};

const deleteDocument = async (item) => {
  if (confirm(`Êtes-vous sûr de vouloir supprimer le document "${item.titre}" ?`)) {
    try {
      console.log("kawabunga");
      const response = await failureApi.patch(`demandes-intervention/${route.params.id}/delink_document/`, {
        document_id: item.id
      });
      console.log(response);
      await fetchData();
      successMessage.value = 'Document supprimé';
    } catch (error) {
      errorMessage.value = 'Erreur lors de la suppression du document';
    }
  }
};

const editCurrentFailure = () => {
  router.push({
    name: 'EditFailure',
    params: { id: route.params.id },
  });
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

/*****************
  Bouton flottant
*****************/
.floating-edit-button {
  position: fixed !important;
  bottom: 24px;
  right: 24px;
  z-index: 100;
}
</style>
