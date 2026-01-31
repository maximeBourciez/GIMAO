<template>
  <BaseDetailView :title="equipement.designation || 'Détail de l\'équipement'" :data="equipement" :loading="isLoading"
    :error-message="errorMessage" :success-message="successMessage" :auto-display="false" :show-edit-button="false"
    :show-delete-button="false" @clear-error="errorMessage = ''" @clear-success="successMessage = ''">
    <template #default="{ data }">
      <v-row v-if="data">
        <!-- Section gauche : Détails de l'équipement -->
        <v-col cols="12" md="4">
          <h3 class="text-h6 mb-4 text-primary">Description de l'équipement</h3>

          <div v-for="(value, key) in equipmentDetails" :key="key" class="detail-field">
            <label class="detail-label" v-if="key !== 'id'">{{ formatLabel(key) }}</label>
            <div class="detail-value" v-if="key !== 'id'">
              <v-chip v-if="key === 'statut'" :color="getStatusColor(value)" dark size="small">
                {{ getStatusLabel(value) || 'Inconnu' }}
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
              <v-data-table v-if="technicalDocuments.length > 0" :headers="technicalDocumentsHeaders"
                :items="technicalDocuments" class="elevation-1 mb-4" hide-default-footer>
                <template #item.action="{ item }">
                  <v-btn v-if="item.lienDocumentTechnique" icon size="small" color="primary"
                    @click="downloadDocument(item.lienDocumentTechnique, item.nomDocumentTechnique)">
                    <v-icon>mdi-download</v-icon>
                  </v-btn>
                  <span v-else class="text-caption text-grey">Non disponible</span>
                </template>
              </v-data-table>
              <p v-else class="text-caption text-grey">Aucun document technique disponible</p>
            </v-card-text>

            <!-- Autres documents (défaillances et interventions) -->
            <v-card-text v-if="othersDocuments.length > 0">
              <h4 class="mb-2">Documents associés</h4>
              <v-data-table :headers="TABLE_HEADERS.DOCUMENTS" :items="othersDocuments" class="elevation-1 mb-4"
                hide-default-footer>
                <template #item.action="{ item }">
                  <v-btn v-if="item.lienDocument" icon size="small" color="primary"
                    @click="downloadDocument(item.lienDocument, item.nomDocument)">
                    <v-icon>mdi-download</v-icon>
                  </v-btn>
                  <span v-else class="text-caption text-grey">Non disponible</span>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Section droite : Image, consommables, interventions et actions -->
        <v-col cols="12" md="8">
          <!-- Section image -->
          <v-card elevation="2" class="mb-4">
            <v-img v-if="data.lienImage" :src="`${BASE_URL}/media/${data.lienImage}`" aspect-ratio="4/3" class="rounded-lg"
              style="max-height: 30vh; object-fit: cover;" alt="Image de l'équipement">
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-icon size="64" color="grey-lighten-2">mdi-image-off</v-icon>
                </v-row>
              </template>
            </v-img>
            <div v-else class="d-flex align-center justify-center pa-8">
              <v-icon size="64" color="grey-lighten-2">mdi-image-off</v-icon>
            </div>
          </v-card>

          <!-- Boutons d'action -->
          <v-card elevation="2" class="mb-4">
            <v-card-actions class="justify-center pa-4">
              <v-btn color="warning" prepend-icon="mdi-alert-circle" @click="signalFailure" v-if="store.getters.hasPermission('di:create')">
                Créer une demande d'intervention (DI)
              </v-btn>
            </v-card-actions>
          </v-card>

          <!-- Section compteurs -->
          <div>
            <v-card elevation="2" class="mb-4" v-if="store.getters.hasPermission('cp:viewList')">
              <v-card-title class="text-h6">Compteurs</v-card-title>
              <v-divider></v-divider>
              <v-card-text>

                <v-data-table v-if="data.compteurs && data.compteurs.length > 0" :items="data.compteurs"
                  :headers="TABLE_HEADERS.COUNTER" class="elevation-1" hide-default-footer>

                  <template #item.action="{ item }">
                    <v-btn icon size="small" @click="viewCounter(item)">
                      <v-icon>mdi-eye</v-icon>
                    </v-btn>
                  </template>
                </v-data-table>
                <p v-else class="text-caption text-grey">Aucun compteur disponible</p>

              </v-card-text>
              <div class="justify-end d-flex">
                <v-btn text color="primary align-self-end" class="my-2 mx-2" @click="openAddCounterDialog" v-if="store.getters.hasPermission('cp:create')">
                  Ajouter un compteur
                </v-btn>
              </div>
            </v-card>

          </div>


          <!-- Historique des interventions -->
          <div>
            <v-card elevation="2" class="mb-4">
              <v-card-title class="text-h6">Interventions</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-data-table v-if="data.bons_travail && data.bons_travail.length > 0" :items="data.bons_travail"
                  :headers="TABLE_HEADERS.INTERVENTIONS_EQUIPMENT" class="elevation-1" hide-default-footer>
                  <template #item.date_assignation="{ item }">
                    {{ formatDate(item.date_assignation) }}
                  </template>
                  <template #item.statut="{ item }">
                    <v-chip :color="getStatusColor(item.statut)" dark size="small">
                      {{ INTERVENTION_STATUS[item.statut] || item.statut }}
                    </v-chip>
                  </template>
                  <template #item.action="{ item }">
                    <v-btn icon size="small" @click="viewIntervention(item)">
                      <v-icon>mdi-eye</v-icon>
                    </v-btn>
                  </template>
                </v-data-table>
                <p v-else class="text-caption text-grey">Aucune intervention enregistrée</p>
              </v-card-text>
            </v-card>


          </div>


          <!-- Section consommables -->
          <v-card elevation="2" class="mb-4">
            <v-card-title class="text-h6">Consommables</v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <v-data-table v-if="data.consommables && data.consommables.length > 0" :items="data.consommables"
                :headers="TABLE_HEADERS.CONSUMABLES" class="elevation-1" hide-default-footer>
                <template #item.reference="{ item }">
                  {{ item.reference || 'Non spécifié' }}
                </template>
                <template #item.fabricant="{ item }">
                  {{ item.fabricant || 'Non spécifié' }}
                </template>
                <template #item.designation="{ item }">
                  {{ item.designation || 'Sans nom' }}
                </template>

              </v-data-table>
              <p v-else class="text-caption text-grey">Aucun consommable associé</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </BaseDetailView>

  <!-- Bouton flottant en bas à droite -->
  <v-btn v-if="showEditButton" color="primary" size="large" icon class="floating-edit-button" elevation="4"
    @click="editCurrentEquip()">
    <v-icon size="large">mdi-pencil</v-icon>
    <v-tooltip activator="parent" location="left">
      {{ editButtonText }}
    </v-tooltip>
  </v-btn>

  <!-- Dialog pour ajouter un compteur -->
  <v-dialog v-model="showCounterDialog" max-width="600px" @click:outside="closeCounterDialog">
    <v-card>
      <v-card-title>Ajouter un compteur</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <CounterInlineForm 
          v-if="currentCounter"
          v-model="currentCounter" 
          :is-edit-mode="false"
          @save="saveCounter" 
          @cancel="closeCounterDialog"
        />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';
import BaseDetailView from '@/components/common/BaseDetailView.vue';
import CounterInlineForm from '@/components/Forms/CounterInlineForm.vue';
import { useApi } from '@/composables/useApi';
import { getStatusColor, getStatusLabel } from '@/utils/helpers';
import { API_BASE_URL, BASE_URL, INTERVENTION_STATUS, TABLE_HEADERS } from '@/utils/constants';

const router = useRouter();
const route = useRoute();
const api = useApi(API_BASE_URL);
const store = useStore();

const equipement = computed(() => api.data.value || {});
const isLoading = computed(() => api.loading.value);
const errorMessage = ref('');
const successMessage = ref('');
const showEditButton = ref(store.getters.hasPermission('eq:edit'));
const editButtonText = ref('Modifier l\'équipement');

// Dialog compteur
const showCounterDialog = ref(false);
const currentCounter = ref(null);

const getEmptyCounter = () => ({
  nom: '',
  unite: 'heures',
  valeurCourante: 0,
  estPrincipal: false,
});

const technicalDocumentsHeaders = [
  { title: 'Document technique', key: 'nomDocumentTechnique', align: 'start' },
  { title: 'Télécharger', key: 'action', align: 'start', sortable: false }
];

const othersDocumentsHeaders = [
  { title: 'Type', key: 'type', align: 'start' },
  { title: 'Document', key: 'nomDocument', align: 'start' },
  { title: 'Télécharger', key: 'action', align: 'start', sortable: false }
];

// Documents techniques (corrigé)
const technicalDocuments = computed(() => {
  return equipement.value.liste_documents_techniques || [];
});

const othersDocuments = computed(() => {
  const documents = [];

  (equipement.value.liste_documents_defaillance || []).forEach(doc => {
    documents.push({
      type: 'Défaillance',
      nomDocument: doc.nomDocumentDefaillance || 'Document sans nom',
      lienDocument: doc.lienDocumentDefaillance,
      source: 'defaillance'
    });
  });

  (equipement.value.liste_documents_intervention || []).forEach(doc => {
    documents.push({
      type: 'Intervention',
      nomDocument: doc.nomDocumentIntervention || 'Document sans nom',
      lienDocument: doc.lienDocumentIntervention,
      source: 'intervention'
    });
  });

  (equipement.value.documents || []).forEach(doc => {
    documents.push({
      type: 'Équipement',
      nomDocument: doc.nomDocument || 'Document sans nom',
      lienDocument: doc.lienDocument,
      source: 'equipement'
    });
  });

  return documents;
});

const equipmentDetails = computed(() => {
  if (!equipement.value) return {};
  const { id,
    reference, designation, dateMiseEnService, prixAchat
  } = equipement.value;

  const lieu = equipement.value.lieu?.nomLieu || '';
  const modele = equipement.value.modele?.nom || '';
  const fournisseur = equipement.value.fournisseur?.nom || '';
  const fabricant = equipement.value.fabricant?.nom || '';
  const statut = equipement.value.dernier_statut?.statut || '';

  return {
    id,
    reference, designation, dateMiseEnService, prixAchat,
    lieu, modele, fournisseur, fabricant, statut
  };
});

const fetchEquipmentData = async () => {
  errorMessage.value = '';
  try {
    await api.get(`equipement/${route.params.id}/affichage/?seuils_lite=true`);
  } catch (error) {
    console.error("Erreur lors de la récupération des données de l'équipement:", error);
    errorMessage.value = "Erreur lors du chargement de l'équipement";
  }
};

const formatLabel = (key) => {
  const labels = {
    reference: 'Référence',
    designation: 'Désignation',
    dateMiseEnService: 'Date de mise en service',
    prixAchat: "Prix d'achat",
    lieu: 'Lieu',
    modele: 'Modèle',
    fournisseur: 'Fournisseur',
    fabricant: 'Fabricant',
    statut: 'Statut'
  };
  return labels[key] || key;
};

const isoDateTimeRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?$/;

const formatDate = (isoString) => {
  const d = new Date(isoString);
  if (isNaN(d.getTime())) return isoString;

  return d.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).replace(' ', ' à ');
};

const formatValue = (value) => {
  if (value === null || value === undefined) return '-';

  if (typeof value === 'boolean') {
    return value ? 'Oui' : 'Non';
  }

  if (typeof value === 'number') {
    return value.toLocaleString('fr-FR');
  }

  if (typeof value === 'string') {
    const trimmed = value.trim();

    if (isoDateTimeRegex.test(trimmed)) {
      const ts = Date.parse(trimmed);
      if (!isNaN(ts)) {
        return formatDate(trimmed);
      }
      return trimmed;
    }

    const isoDateOnly = /^\d{4}-\d{2}-\d{2}$/;
    if (isoDateOnly.test(trimmed)) {
      const ts = Date.parse(trimmed);
      if (!isNaN(ts)) {
        return new Intl.DateTimeFormat('fr-FR', { year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(ts));
      }
      return trimmed;
    }

    return trimmed === '' ? '-' : trimmed;
  }

  return String(value) || '-';
};


const viewIntervention = (intervention) => {
  if (intervention && intervention.id) {
    if(route.query.from === 'dashboard') {
      router.push({
        name: 'InterventionDetail',
        params: { id: intervention.id },
        query: { from: route.query.from }
      });
      return;
    }


    router.push({
      name: 'InterventionDetail',
      params: { id: intervention.id },
      query: { from: 'equipment', equipmentId: equipement.value.id }
    });
  }
};

const signalFailure = () => {
  if (equipement.value.reference) {
    router.push({
      name: 'CreateFailure',
      params: { equipementId: equipement.value.id }
    });
  }
};

const downloadDocument = async (lien, nomFichier) => {
  if (!lien) {
    errorMessage.value = 'Aucun lien de document disponible';
    return;
  }

  try {
    let cleanedLink = lien;
    if (lien.includes('/media/')) {
      cleanedLink = lien.split('/media/')[1];
    }

    if (cleanedLink.startsWith('/')) {
      cleanedLink = cleanedLink.substring(1);
    }

    const fullUrl = `${BASE_URL}/media/${cleanedLink}`;
    console.log('Téléchargement depuis:', fullUrl);

    const response = await fetch(fullUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = nomFichier || 'document';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

    successMessage.value = 'Document téléchargé avec succès';
    setTimeout(() => successMessage.value = '', 3000);
  } catch (error) {
    console.error('Erreur lors du téléchargement:', error);
    errorMessage.value = 'Erreur lors du téléchargement du fichier';
  }
};

const viewCounter = (counter) => {
  router.push({
    name: 'CounterDetail',
    params: { id: counter.id },
    query: { from: 'equipment', equipmentId: equipmentDetails.value.id }
  })
}

const openAddCounterDialog = () => {
  currentCounter.value = getEmptyCounter();
  showCounterDialog.value = true;
};

const closeCounterDialog = () => {
  showCounterDialog.value = false;
  currentCounter.value = null;
};

const saveCounter = async () => {
  try {
    const fd = new FormData();

    const counterData = {
      nom: currentCounter.value.nom,
      unite: currentCounter.value.unite,
      valeurCourante: currentCounter.value.valeurCourante ?? 0,
      estPrincipal: currentCounter.value.estPrincipal,
      equipement: route.params.id
    };

    fd.append('compteur', JSON.stringify(counterData));

    const counterApi = useApi(API_BASE_URL);
    await counterApi.post('compteurs/', fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    successMessage.value = 'Compteur créé avec succès';
    closeCounterDialog();
    await fetchEquipmentData();

    setTimeout(() => successMessage.value = '', 3000);
  } catch (error) {
    console.error('Erreur lors de la création du compteur:', error);
    errorMessage.value = 'Erreur lors de la création du compteur';
  }
};

onMounted(() => {
  fetchEquipmentData();
});

const editCurrentEquip = () => [
  router.push({
    name: 'EditEquipment',
    params: { id: equipmentDetails.value.id },
    query: { from: 'equipment', equipmentId: equipmentDetails.value.id }
  })
]
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