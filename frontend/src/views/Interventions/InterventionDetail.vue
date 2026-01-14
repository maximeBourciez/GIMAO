<template>
  <BaseDetailView
    :title="'Détail du bon de travail'"
    :data="intervention"
    :loading="loading"
    :error-message="errorMessage"
    :success-message="successMessage"
    :auto-display="false"
    :show-edit-button="false"
    :show-delete-button="false"
    @clear-error="errorMessage = ''"
    @clear-success="successMessage = ''"
  >
    <template #default="{ data }">
      <v-row v-if="data">
        <!-- Colonne gauche : champs du BT -->
        <v-col cols="12" md="6">
          <h3 class="text-h6 mb-4 text-primary">{{ data.nom }}</h3>

          <div class="detail-field">
            <label class="detail-label">ID</label>
            <div class="detail-value">{{ data.id || 'Non spécifié' }}</div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Type</label>
            <div class="detail-value">{{ data.type || 'Non spécifié' }}</div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Statut</label>
            <div class="detail-value">
              <v-chip
                :color="getInterventionStatusColor(data.statut)"
                dark
                size="small"
              >
                {{ INTERVENTION_STATUS[data.statut] || data.statut || 'Non spécifié' }}
              </v-chip>
            </div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Diagnostic</label>
            <div class="detail-value text-pre">{{ data.diagnostic || 'Non spécifié' }}</div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Date d'assignation</label>
            <div class="detail-value">{{ formatDateTime(data.date_assignation) }}</div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Date prévue</label>
            <div class="detail-value">{{ formatDateTime(data.date_prevue) }}</div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Date de début</label>
            <div class="detail-value">{{ formatDateTime(data.date_debut) }}</div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Date de fin</label>
            <div class="detail-value">{{ formatDateTime(data.date_fin) }}</div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Date de clôture</label>
            <div class="detail-value">{{ formatDateTime(data.date_cloture) }}</div>
          </div>

          <!-- Boutons d'action -->
          <v-row class="mt-6">
            <v-col cols="12" md="6" class="py-1">
              <v-btn color="warning" block :disabled="!canStart" @click="openStartModal">Démarrer l'intervention</v-btn>
            </v-col>
            <v-col cols="12" md="6" class="py-1">
              <v-btn color="warning" block :disabled="!canFinish" @click="openFinishModal">Terminer l'intervention</v-btn>
            </v-col>
            <v-col cols="12" md="6" class="py-1">
              <v-btn color="primary" block @click="goToEditIntervention">Modifier le bon de travail</v-btn>
            </v-col>
            <v-col cols="12" md="6" class="py-1">
              <v-btn color="success" block :disabled="!canClose" @click="openCloseModal">Clôturer le bon de travail</v-btn>
            </v-col>
            <v-col cols="12" class="py-1">
              <v-btn color="error" block @click="openDeleteModal">Supprimer le bon de travail</v-btn>
            </v-col>
          </v-row>
        </v-col>

        <!-- Colonne droite : commentaires + FK en sous-sections -->
        <v-col cols="12" md="6">
          <h3 class="text-h6 mb-4 text-primary">Commentaires</h3>
          <div class="detail-field">
            <label class="detail-label">Commentaire</label>
            <div class="detail-value text-pre">{{ data.commentaire || 'Aucun commentaire' }}</div>
          </div>

          <div class="detail-field">
            <label class="detail-label">Commentaire de refus de clôture</label>
            <div class="detail-value text-pre">{{ data.commentaire_refus_cloture || 'Non spécifié' }}</div>
          </div>

          <!-- Section Affectation -->
          <v-card class="mt-4" elevation="2">
            <v-card-title class="text-h6 d-flex align-center cursor-pointer" @click="showAffectation = !showAffectation">
              Affectation
              <v-spacer></v-spacer>
              <v-icon>
                {{ showAffectation ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
              </v-icon>
            </v-card-title>
            <v-expand-transition>
              <div v-show="showAffectation">
                <v-divider></v-divider>
                <v-card-text>
                  <div class="detail-field">
                    <label class="detail-label">Responsable</label>
                    <div class="detail-value">
                      <span v-if="data.responsable">{{ data.responsable.prenom }} {{ data.responsable.nomFamille }}</span>
                      <span v-else>Non spécifié</span>
                    </div>
                  </div>
                  <div class="detail-field">
                    <label class="detail-label">Utilisateurs assignés</label>
                    <div class="detail-value">
                      <div v-if="Array.isArray(data.utilisateur_assigne) && data.utilisateur_assigne.length">
                        <div v-for="u in data.utilisateur_assigne" :key="u.id">
                          - {{ u.prenom }} {{ u.nomFamille }}
                        </div>
                      </div>
                      <div v-else>Non spécifié</div>
                    </div>
                  </div>
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-card>

          <!-- Section DI -->
          <v-card class="mt-4" elevation="2">
            <v-card-title class="text-h6 d-flex align-center cursor-pointer" @click="toggleDemandeDetails">
              Demande d'intervention
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                size="small"
                class="mr-2"
                @click.stop="openFailure"
                :disabled="!demandeId"
              >
                Ouvrir
              </v-btn>
              <v-icon>
                {{ showDemandeDetails ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
              </v-icon>
            </v-card-title>
            <v-expand-transition>
              <div v-show="showDemandeDetails">
                <v-divider></v-divider>
                <v-card-text>
                  <div v-for="(value, key) in formattedDemande" :key="key" class="detail-field">
                    <label class="detail-label">{{ key }}</label>
                    <div class="detail-value">{{ value }}</div>
                  </div>
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-card>

      <!-- Section Équipement (provient de la DI) -->
      <v-card class="mt-4" elevation="2">
        <v-card-title class="text-h6 d-flex align-center cursor-pointer" @click="toggleEquipementDetails">
          Équipement
          <v-spacer></v-spacer>
      <v-btn
        color="primary"
        size="small"
        class="mr-2"
        @click.stop="openEquipement"
        :disabled="!equipementId"
      >
        Ouvrir
      </v-btn>
          <v-icon>
            {{ showEquipementDetails ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
          </v-icon>
        </v-card-title>
        <v-expand-transition>
          <div v-show="showEquipementDetails">
            <v-divider></v-divider>
            <v-card-text>
              <div v-if="!equipement">
                Aucun équipement associé
              </div>
              <div v-else>
                <div v-for="(value, key) in formattedEquipement" :key="key" class="detail-field">
                  <label class="detail-label">{{ key }}</label>
                  <div class="detail-value">{{ value }}</div>
                </div>
              </div>
            </v-card-text>
          </div>
        </v-expand-transition>
      </v-card>

          <!-- Section Documents -->
          <v-card class="mt-4" elevation="2">
            <v-card-title class="text-h6 d-flex align-center cursor-pointer" @click="toggleDocumentsDetails">
              Documents du bon de travail
              <v-spacer></v-spacer>
              <v-btn color="primary" size="small" class="mr-2" @click.stop="addDocument">
                Ajouter
              </v-btn>
              <v-icon>
                {{ showDocumentsDetails ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
              </v-icon>
            </v-card-title>
            <v-expand-transition>
              <div v-show="showDocumentsDetails">
                <v-divider></v-divider>
                <v-card-text>
                  <v-toolbar flat class="mb-2">
                    <v-spacer></v-spacer>
                    <v-btn color="primary" size="small" @click="toggleActionMode">
                      {{ actionMode === 'download' ? 'Mode suppression' : 'Mode téléchargement' }}
                    </v-btn>
                  </v-toolbar>

                  <v-data-table
                    :headers="documentHeaders"
                    :items="data.liste_documents_intervention || []"
                    class="elevation-1"
                    hide-default-footer
                    :items-per-page="-1"
                  >
                    <template #item.actions="{ item }">
                      <v-btn
                        icon
                        size="small"
                        :color="actionMode === 'download' ? 'primary' : 'error'"
                        @click="actionMode === 'download' ? downloadDocument(item) : deleteDocument(item)"
                      >
                        <v-icon size="small">
                          {{ actionMode === 'download' ? 'mdi-download' : 'mdi-delete' }}
                        </v-icon>
                      </v-btn>
                    </template>
                  </v-data-table>
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </BaseDetailView>

    <!-- Bouton flottant (+) : créer un nouveau BT -->
    <v-btn
      v-if="demandeId"
      color="primary"
      size="large"
      icon
      elevation="4"
      class="floating-create-button"
      @click="handleCreateBonTravail"
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>

    <!-- Modales de confirmation (comme DI) -->
    <ConfirmationModal
      v-model="showStart"
      type="warning"
      title="Démarrer l'intervention"
      message="Êtes-vous sûr de vouloir démarrer cette intervention ?"
      confirm-text="Démarrer"
      confirm-icon="mdi-play"
      :loading="actionLoading"
      @confirm="startIntervention"
      @cancel="showStart = false"
    />
    <ConfirmationModal
      v-model="showFinish"
      type="warning"
      title="Terminer l'intervention"
      message="Êtes-vous sûr de vouloir terminer cette intervention ?"
      confirm-text="Terminer"
      confirm-icon="mdi-check"
      :loading="actionLoading"
      @confirm="finishIntervention"
      @cancel="showFinish = false"
    />
    <ConfirmationModal
      v-model="showClose"
      type="success"
      title="Clôturer le bon de travail"
      message="Êtes-vous sûr de vouloir clôturer ce bon de travail ?"
      confirm-text="Clôturer"
      confirm-icon="mdi-check-circle-outline"
      :loading="actionLoading"
      @confirm="closeBonTravail"
      @cancel="showClose = false"
    />
    <ConfirmationModal
      v-model="showDelete"
      type="error"
      title="Supprimer le bon de travail"
      message="Êtes-vous sûr de vouloir supprimer ce bon de travail ?"
      confirm-text="Supprimer"
      confirm-icon="mdi-delete"
      :loading="actionLoading"
      @confirm="deleteBonTravail"
      @cancel="showDelete = false"
    />

</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BaseDetailView from '@/components/common/BaseDetailView.vue';
import ConfirmationModal from '@/components/common/ConfirmationModal.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL, BASE_URL, INTERVENTION_STATUS } from '@/utils/constants';
import { formatDateTime, getInterventionStatusColor } from '@/utils/helpers';

const router = useRouter();
const route = useRoute();

const api = useApi(API_BASE_URL);

const intervention = ref(null);
const loading = ref(false);
const actionLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const actionMode = ref('download');
const showDemandeDetails = ref(false);
const showDocumentsDetails = ref(false);
const showAffectation = ref(false);
const showEquipementDetails = ref(false);

const showStart = ref(false);
const showFinish = ref(false);
const showClose = ref(false);
const showDelete = ref(false);

const documentHeaders = [
  { title: 'Nom du document', value: 'nomDocumentIntervention' },
  { title: 'Actions', value: 'actions', sortable: false }
];

const demandeId = computed(() => intervention.value?.demande_intervention?.id);

const equipement = computed(() => intervention.value?.demande_intervention?.equipement || null);
const equipementId = computed(() => equipement.value?.id);

const formattedDemande = computed(() => {
  const demande = intervention.value?.demande_intervention;
  if (!demande) return {};
  return {
    'Nom de la demande': demande.nom || 'Non spécifié',
    'Date de commencement': formatDateTime(demande.date_commencement),
    'Date de traitement': formatDateTime(demande.date_traitement),
    'Commentaire': demande.commentaire || 'Aucun commentaire'
  };
});

const formattedEquipement = computed(() => {
	const e = equipement.value;
	if (!e) return {};
	return {
		'Désignation': e.designation || 'Non spécifié',
		'Code': e.code || e.identifiant || 'Non spécifié',
		'Localisation': e.localisation || e.emplacement || 'Non spécifié',
		'État': e.etat || 'Non spécifié'
	};
});

const canClose = computed(() => !!intervention.value && !intervention.value.date_cloture);
const canStart = computed(() => intervention.value?.statut === 'EN_ATTENTE');
const canFinish = computed(() => intervention.value?.statut === 'EN_COURS');

const openStartModal = () => {
  showStart.value = true;
};

const openFinishModal = () => {
  showFinish.value = true;
};

const openCloseModal = () => {
  showClose.value = true;
};

const openDeleteModal = () => {
  showDelete.value = true;
};

const goToEditIntervention = () => {
  const id = intervention.value?.id ?? route.params.id;
  if (!id) return;
  router.push({ name: 'EditIntervention', params: { id } });
};

const handleCreateBonTravail = () => {
  if (!demandeId.value) return;
  router.push({ name: 'CreateIntervention', params: { id: demandeId.value } });
};

const fetchData = async () => {
  loading.value = true;
  errorMessage.value = '';
  try {
    intervention.value = await api.get(`bons-travail/${route.params.id}`);
  } catch (error) {
    errorMessage.value = 'Erreur lors du chargement des données';
  } finally {
    loading.value = false;
  }
};

const toggleActionMode = () => {
  actionMode.value = actionMode.value === 'download' ? 'delete' : 'download';
};

const toggleDemandeDetails = () => {
  showDemandeDetails.value = !showDemandeDetails.value;
};

const toggleDocumentsDetails = () => {
  showDocumentsDetails.value = !showDocumentsDetails.value;
};

const toggleEquipementDetails = () => {
	showEquipementDetails.value = !showEquipementDetails.value;
};

const openFailure = () => {
  if (demandeId.value) {
  router.push({
    name: 'FailureDetail',
    params: { id: demandeId.value },
    query: { from: 'intervention', interventionId: route.params.id }
  });
  }
};

const openEquipement = () => {
  if (!equipementId.value) return;
  router.push({
    name: 'EquipmentDetail',
    params: { id: equipementId.value },
    query: { from: 'intervention', interventionId: route.params.id }
  });
};

const addDocument = () => {
  if (!intervention.value?.id) return;
  router.push({ name: 'AddDocumentIntervention', params: { id: intervention.value.id } });
};

const closeBonTravail = async () => {
  if (!intervention.value?.id) return;
  actionLoading.value = true;
  try {
    await api.post(`bons-travail/${intervention.value.id}/cloturer`);
    successMessage.value = 'Bon de travail clôturé';
    showClose.value = false;
    await fetchData();
  } catch (error) {
    errorMessage.value = 'Erreur lors de la clôture du bon de travail';
  } finally {
    actionLoading.value = false;
  }
};

const startIntervention = async () => {
  if (!intervention.value?.id) return;
  actionLoading.value = true;
  try {
    await api.post(`bons-travail/${intervention.value.id}/demarrer`);
    successMessage.value = 'Intervention démarrée';
    showStart.value = false;
    await fetchData();
  } catch (error) {
    errorMessage.value = 'Erreur lors du démarrage de l\'intervention';
  } finally {
    actionLoading.value = false;
  }
};

const finishIntervention = async () => {
  if (!intervention.value?.id) return;
  actionLoading.value = true;
  try {
    await api.patch(`bons-travail/${intervention.value.id}/`, {
      date_fin: new Date().toISOString(),
      statut: 'TERMINE'
    });
    successMessage.value = 'Intervention terminée';
    showFinish.value = false;
    await fetchData();
  } catch (error) {
    errorMessage.value = 'Erreur lors de la fin de l\'intervention';
  } finally {
    actionLoading.value = false;
  }
};

const deleteBonTravail = async () => {
  if (!intervention.value?.id) return;
  actionLoading.value = true;
  try {
    await api.delete(`bons-travail/${intervention.value.id}/`);
    successMessage.value = 'Bon de travail supprimé';
    showDelete.value = false;
    setTimeout(() => router.push({ name: 'InterventionList' }), 800);
  } catch (error) {
    errorMessage.value = 'Erreur lors de la suppression du bon de travail';
  } finally {
    actionLoading.value = false;
  }
};

const downloadDocument = (item) => {
  const link = item?.lienDocumentIntervention;
  if (!link) return;
  const cleanedLink = link.startsWith('/media/') ? link : `/media/${link.split('/media/').pop()}`;
  const fullUrl = `${BASE_URL}${cleanedLink}`;

  fetch(fullUrl)
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return response.blob();
    })
    .then((blob) => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = item.nomDocumentIntervention || 'document';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    })
    .catch(() => {
      alert('Erreur lors du téléchargement du fichier. Veuillez réessayer.');
    });
};

const deleteDocument = async (item) => {
  if (!confirm(`Êtes-vous sûr de vouloir supprimer le document "${item.nomDocumentIntervention}" ?`)) return;
  // TODO: impl API suppression document
  await fetchData();
};

onMounted(fetchData);
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

.cursor-pointer {
  cursor: pointer;
}

.text-pre {
  white-space: pre-wrap;
}

.floating-create-button {
  position: fixed !important;
  bottom: 24px;
  right: 24px;
  z-index: 100;
}
</style>