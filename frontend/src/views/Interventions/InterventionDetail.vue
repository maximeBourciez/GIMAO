<template>
  <BaseDetailView title="Détail du Bon de Travail" :data="intervention" :loading="isLoading" :show-edit-button="false"
    :show-delete-button="false">
    <template #actions>
      <v-btn color="warning" class="mx-1" @click="reopen_intervention" :disabled="!can_supprimer">
        Refuser la clôture
      </v-btn>
      <v-btn color="success" class="mx-1" @click="close_intervention" :disabled="!can_cloturer">
        Clôturer
      </v-btn>
    </template>

    <template #default="{ data }">
      <v-row v-if="data">
        <!-- Left column with information -->
        <v-col cols="12" md="6">
          <h3 class="text-h6 mb-4 text-primary">Informations de l'intervention</h3>

          <div v-for="(value, key) in format_label_intervention" :key="key" class="detail-field">
            <label class="detail-label">{{ key }}</label>
            <div class="detail-value">{{ value }}</div>
          </div>
        </v-col>

        <!-- Right column with additional information -->
        <v-col cols="12" md="6">
          <h3 class="text-h6 mb-4 text-primary">Commentaires</h3>

          <div class="detail-field">
            <label class="detail-label">Commentaire</label>
            <div class="detail-value">{{ data.commentaire || 'Aucun commentaire' }}</div>
          </div>

          <div v-if="data.commentaire_refus_cloture" class="detail-field">
            <label class="detail-label">Commentaire de refus de clôture</label>
            <div class="detail-value">{{ data.commentaire_refus_cloture }}</div>
          </div>

          <!-- Section DI expandable -->
          <v-card class="mt-4" elevation="2">
            <v-card-title class="text-h6 d-flex align-center cursor-pointer" @click="toggle_defaillance_details">
              Demande d'intervention
              <v-spacer></v-spacer>
              <v-btn color="primary" size="small" class="mr-2" @click.stop="open_failure" :disabled="!defaillance_id">
                Ouvrir
              </v-btn>
              <v-icon>
                {{ show_defaillance_details ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
              </v-icon>
            </v-card-title>
            <v-expand-transition>
              <div v-show="show_defaillance_details">
                <v-divider></v-divider>
                <v-card-text>
                  <div v-for="(value, key) in format_label_defaillance" :key="key" class="detail-field">
                    <label class="detail-label">{{ key }}</label>
                    <div class="detail-value">{{ value }}</div>
                  </div>
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-card>

          <!-- Section Documents -->
          <v-card class="mt-4" elevation="2">
            <v-card-title class="text-h6 d-flex align-center cursor-pointer" @click="toggle_documents_details">
              Documents du bon de travail
              <v-spacer></v-spacer>
              <v-btn color="primary" size="small" class="mr-2" @click.stop="add_document">
                Ajouter
              </v-btn>
              <v-icon>
                {{ show_documents_details ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
              </v-icon>
            </v-card-title>
            <v-expand-transition>
              <div v-show="show_documents_details">
                <v-divider></v-divider>
                <v-card-text>
                  <v-toolbar flat class="mb-2">
                    <v-spacer></v-spacer>
                    <v-btn color="primary" size="small" @click="toggle_action_mode">
                      {{ action_mode === 'download' ? 'Mode suppression' : 'Mode téléchargement' }}
                    </v-btn>
                  </v-toolbar>

                  <v-data-table :headers="headers" :items="data.liste_documents_intervention || []" class="elevation-1"
                    hide-default-footer :items-per-page="-1">
                    <template v-slot:item.actions="{ item }">
                      <v-btn icon size="small" :color="action_mode === 'download' ? 'primary' : 'error'"
                        @click="action_mode === 'download' ? download_document(item) : delete_document(item)">
                        <v-icon size="small">
                          {{ action_mode === 'download' ? 'mdi-download' : 'mdi-delete' }}
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
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BaseDetailView from '@/components/common/BaseDetailView.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL, BASE_URL } from '@/utils/constants';

const router = useRouter();
const route = useRoute();
const interventionApi = useApi(API_BASE_URL);

const action_mode = ref('download');
const intervention = ref(null);
const isLoading = ref(false);
const show_defaillance_details = ref(false);
const show_documents_details = ref(false);

const headers = [
  { title: 'Nom du document', value: 'nomDocumentIntervention' },
  { title: 'Actions', value: 'actions', sortable: false }
];

const defaillance_id = computed(() => intervention.value?.demande_intervention?.id);

const date_format = (dateString) => {
  if (!dateString) return 'Non spécifié';
  const date = new Date(dateString);
  return date.toLocaleString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const format_label_intervention = computed(() => {
  if (!intervention.value) return {};
  return {
    'Nom': intervention.value.nom,
    'Type': intervention.value.type,
    'Statut': intervention.value.statut,
    'Date d\'assignation': date_format(intervention.value.date_assignation),
    'Date de clôture': date_format(intervention.value.date_cloture),
    'Date de début': date_format(intervention.value.date_debut),
    'Date de fin': date_format(intervention.value.date_fin),
  };
});

const format_label_defaillance = computed(() => {
  if (!intervention.value || !intervention.value.demande_intervention) return {};
  const demande = intervention.value.demande_intervention;
  return {
    'Nom de la demande': demande.nom,
    'Date de commencement': date_format(demande.date_commencement),
    'Date de traitement': date_format(demande.date_traitement),
    'Commentaire': demande.commentaire || 'Aucun commentaire',
  };
});

const can_supprimer = computed(() => intervention.value && !intervention.value.date_cloture);
const can_cloturer = computed(() => intervention.value && !intervention.value.date_cloture);

const fetch_data = async () => {
  isLoading.value = true;
  try {
    const response = await interventionApi.get(`bons-travail/${route.params.id}`);
    intervention.value = response;
  } catch (error) {
    console.error('Erreur lors de la récupération des données:', error);
  } finally {
    isLoading.value = false;
  }
};

const open_failure = () => {
  if (defaillance_id.value) {
    router.push({ name: 'FailureDetail', params: { id: defaillance_id.value } });
  }
};

const toggle_action_mode = () => {
  action_mode.value = action_mode.value === 'download' ? 'delete' : 'download';
};

const reopen_intervention = async () => {
  if (confirm('Êtes-vous sûr de vouloir refuser la clôture de ce bon de travail ?')) {
    try {
      await interventionApi.patch(`bons-travail/${intervention.value.id}/`, { date_cloture: null });
      await fetch_data();
    } catch (error) {
      console.error('Erreur lors de la réouverture du bon de travail:', error);
    }
  }
};

const close_intervention = async () => {
  if (confirm('Êtes-vous sûr de vouloir clôturer ce bon de travail ?')) {
    try {
      await interventionApi.post(`bons-travail/${intervention.value.id}/cloturer`);
      router.go(-1);
    } catch (error) {
      console.error('Erreur lors de la clôture du bon de travail:', error);
    }
  }
};

const download_document = (item) => {
  const cleanedLink = item.lienDocumentIntervention.startsWith('/media/')
    ? item.lienDocumentIntervention
    : `/media/${item.lienDocumentIntervention.split('/media/').pop()}`;
  const fullUrl = `${BASE_URL}${cleanedLink}`;

  fetch(fullUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.blob();
    })
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = item.nomDocumentIntervention;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    })
    .catch(error => {
      console.error('Erreur lors du téléchargement:', error);
      alert('Erreur lors du téléchargement du fichier. Veuillez réessayer.');
    });
};

const delete_document = async (item) => {
  if (confirm(`Êtes-vous sûr de vouloir supprimer le document "${item.nomDocumentIntervention}" ?`)) {
    try {
      await fetch_data();
      alert(`Le document "${item.nomDocumentIntervention}" a été supprimé avec succès.`);
    } catch (error) {
      console.error('Erreur lors de la suppression du document:', error);
      alert('Une erreur est survenue lors de la suppression du document.');
    }
  }
};

const toggle_defaillance_details = () => {
  show_defaillance_details.value = !show_defaillance_details.value;
};

const toggle_documents_details = () => {
  show_documents_details.value = !show_documents_details.value;
};

const add_document = () => {
  router.push({ name: 'AddDocumentIntervention', params: { id: intervention.value.id } });
};

onMounted(fetch_data);
</script>

<style scoped>
.detail-field {
  margin-bottom: 16px;
}

.detail-label {
  font-weight: 600;
  color: rgb(var(--v-theme-primary));
  display: block;
  margin-bottom: 4px;
}

.detail-value {
  color: rgba(0, 0, 0, 0.87);
}

.cursor-pointer {
  cursor: pointer;
}
</style>