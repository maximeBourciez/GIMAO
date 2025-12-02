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
            <label class="detail-label" v-if="key !== 'id'">{{ formatLabel(key) }}</label>
            <div class="detail-value" v-if="key !== 'id'">
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
              <v-data-table v-if="technicalDocuments.length > 0" 
                :headers="technicalDocumentsHeaders" 
                :items="technicalDocuments"
                class="elevation-1 mb-4" 
                hide-default-footer>
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
              <v-data-table :headers="othersDocumentsHeaders" :items="othersDocuments"
                class="elevation-1 mb-4" hide-default-footer>
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
        <v-col cols="12" md="6">
          <!-- Section image -->
          <v-card elevation="2" class="mb-4">
            <v-img v-if="data.lienImage" :src="data.lienImage" aspect-ratio="4/3" class="rounded-lg" 
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
              <v-data-table v-if="data.consommables && data.consommables.length > 0" 
                :items="data.consommables" 
                :headers="consumableHeaders" 
                class="elevation-1" 
                hide-default-footer>
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

          <!-- Historique des interventions -->
          <v-card elevation="2">
            <v-card-title class="text-h6">Interventions</v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <v-data-table v-if="data.liste_interventions && data.liste_interventions.length > 0" 
                :items="data.liste_interventions" 
                :headers="interventionsHeaders" 
                class="elevation-1" 
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
              <p v-else class="text-caption text-grey">Aucune intervention enregistrée</p>
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
  { title: 'Fabricant', key: 'fabricant' }
];

const interventionsHeaders = [
  { title: 'Nom', key: 'nomIntervention' },
  { title: "Date d'assignation", key: 'dateAssignation' },
  { title: 'Visualiser', key: 'action', align: 'start' }
];

// Documents techniques (corrigé)
const technicalDocuments = computed(() => {
  return equipement.value.liste_documents_techniques || [];
});

// Autres documents (défaillances et interventions)
const othersDocuments = computed(() => {
  const documents = [];
  
  // Documents de défaillance
  (equipement.value.liste_documents_defaillance || []).forEach(doc => {
    documents.push({
      type: 'Défaillance',
      nomDocument: doc.nomDocumentDefaillance || 'Document sans nom',
      lienDocument: doc.lienDocumentDefaillance,
      source: 'defaillance'
    });
  });
  
  // Documents d'intervention
  (equipement.value.liste_documents_intervention || []).forEach(doc => {
    documents.push({
      type: 'Intervention',
      nomDocument: doc.nomDocumentIntervention || 'Document sans nom',
      lienDocument: doc.lienDocumentIntervention,
      source: 'intervention'
    });
  });
  
  // Documents généraux de l'équipement
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
  const {id,
    reference, designation, dateMiseEnService, prixAchat,
    preventifGlissant, joursIntervalleMaintenance
  } = equipement.value;

  console.log('Equipement value:', equipement.value);
  const lieu = equipement.value.lieu?.nomLieu || '';
  const modele = equipement.value.modele?.nom || '';
  const fournisseur = equipement.value.fournisseur?.nomFournisseur || '';
  const fabricant = equipement.value.fabricant?.nomFabricant || '';
  const statut = equipement.value.dernier_statut?.statut || '';

  return {id,
    reference, designation, dateMiseEnService, prixAchat,
    preventifGlissant, joursIntervalleMaintenance,
    lieu, modele, fournisseur, fabricant, statut
  };
});

const fetchEquipmentData = async () => {
  errorMessage.value = '';
  try {
    await api.get(`equipement/${route.params.id}/affichage/`);
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

// Détecte un ISO 8601 de type complet (ex: 2025-12-02T22:15:30Z ou 2025-12-02T22:15:30+01:00)
const isoDateTimeRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$/;

// Formatage de date (tu peux adapter les options)
const formatDate = (isoString) => {
  const d = new Date(isoString);
  if (isNaN(d.getTime())) return isoString; // fallback
  return new Intl.DateTimeFormat('fr-FR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(d);
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

    // Si la chaîne correspond strictement au pattern ISO datetime, on la formate.
    if (isoDateTimeRegex.test(trimmed)) {
      
      const ts = Date.parse(trimmed);
      if (!isNaN(ts)) {
        return formatDate(trimmed);
      }
      return trimmed;
    }

    // Reconnaissance d'une date ISO sans time (YYYY-MM-DD)
    const isoDateOnly = /^\d{4}-\d{2}-\d{2}$/;
    if (isoDateOnly.test(trimmed)) {
      const ts = Date.parse(trimmed);
      if (!isNaN(ts)) {
        return new Intl.DateTimeFormat('fr-FR', { year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(ts));
      }
      return trimmed;
    }

    // Aucun format date reconnu -> on renvoie la chaîne telle quelle 
    return trimmed === '' ? '-' : trimmed;
  }

  // Par défaut
  return String(value) || '-';
};


const viewIntervention = (intervention) => {
  if (intervention && intervention.id) {
    router.push({
      name: 'InterventionDetail',
      params: { id: intervention.id }
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
    // Nettoyer le lien
    let cleanedLink = lien;
    if (lien.includes('/media/')) {
      cleanedLink = lien.split('/media/')[1];
    }
    
    // S'assurer que cleanedLink n'a pas de slash au début
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