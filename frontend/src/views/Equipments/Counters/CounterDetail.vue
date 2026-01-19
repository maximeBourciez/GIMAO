<template>
  <v-card>
    <!-- Titre -->
    <v-card-title class="d-flex align-center">
      <v-icon left>mdi-counter</v-icon>
      <span>Détails du compteur</span>
    </v-card-title>

    <v-card-text v-if="!loading && counter">
      <!-- Informations générales du compteur -->
      <v-sheet class="pa-4 mb-4" elevation="2" rounded>
        <h3 class="mb-3 text-blue-darken-3">Informations du compteur</h3>

        <v-row dense>
          <v-col cols="12" md="4">
            <strong>Nom :</strong>
            <div class="text-h6">{{ counter.nomCompteur }}</div>
          </v-col>


          <v-col cols="12" md="4">
            <strong>Valeur actuelle :</strong>
            <div class="text-h6">{{ counter.valeurCourante ?? "—" }}</div>
          </v-col>
          <v-col cols="12" md="4">
            <strong>Unité :</strong>
            <div class="text-h6">{{ counter.unite }}</div>
          </v-col>


        </v-row>

        <v-row dense class="mt-2">
          <v-col cols="12" md="4">
            <strong>Statut :</strong>
            <v-chip :color="counter.estPrincipal ? 'primary' : 'grey'" label class="ml-2" size="small">
              {{ counter.estPrincipal ? "Principal" : "Secondaire" }}
            </v-chip>
          </v-col>

          <v-col cols="12" md="4">
            <strong>Équipement :</strong>
            <div>{{ counter.equipement_info?.designation || "—" }}</div>
          </v-col>

          <v-col cols="12" md="4">
            <strong>Lieu :</strong>
            <div>{{ counter.equipement_info?.lieu?.nomLieu || "—" }}</div>
          </v-col>
        </v-row>
      </v-sheet>

      <!-- Liste des seuils avec plans de maintenance -->
      <div v-if="counter.seuils && counter.seuils.length > 0">
        <h3 class="mb-3">Seuils et plans de maintenance associés</h3>

        <v-expansion-panels multiple v-model="openedPanels">
          <v-expansion-panel v-for="(seuil, index) in counter.seuils" :key="seuil.id">
            <v-expansion-panel-title expand-icon="mdi-menu-down">
              <template v-slot:default="{ expanded }">
                <v-row no-gutters align="center">
                  <v-col cols="4" class="text-left">
                    <div class="d-flex align-center">
                      <v-icon left>mdi-calendar-clock</v-icon>
                      <strong class="ml-2">Seuil {{ index + 1 }}</strong>
                    </div>
                  </v-col>
                  <v-col cols="6" class="text-left">
                    <div v-if="seuil.planMaintenance" class="text-truncate">
                      {{ seuil.planMaintenance.nom }}
                    </div>
                    <div v-else class="text-grey">Aucun plan de maintenance associé</div>
                  </v-col>
                  <v-col cols="2" class="text-right">
                    <v-chip :color="getProgressionColor(seuil)" size="small" label>
                      {{ getProgressionText(seuil) }}
                    </v-chip>
                  </v-col>
                </v-row>
              </template>
            </v-expansion-panel-title>

            <v-expansion-panel-text>
              <!-- Détails du seuil -->
              <v-sheet class="pa-3 mb-3" elevation="1" rounded>
                <h4 class="mb-2">Détails du seuil</h4>
                <v-row dense>
                  <v-col cols="12" md="3">
                    <strong>Dernière intervention :</strong>
                    <div>{{ seuil.derniereIntervention }} {{ counter.unite }}</div>
                  </v-col>
                  <v-col cols="12" md="3">
                    <strong>Prochaine maintenance :</strong>
                    <div>{{ seuil.prochaineMaintenance }} {{ counter.unite }}</div>
                  </v-col>
                  <v-col cols="12" md="3">
                    <strong>Intervalle :</strong>
                    <div>{{ seuil.ecartInterventions }} {{ counter.unite }}</div>
                  </v-col>
                  <v-col cols="12" md="3">
                    <strong>Type de seuil :</strong>
                    <v-chip :color="seuil.estGlissant ? 'green' : 'orange'" size="small" label>
                      {{ seuil.estGlissant ? "Glissant" : "Fixe" }}
                    </v-chip>
                  </v-col>
                </v-row>
              </v-sheet>

              <!-- Plan de maintenance -->
              <div v-if="seuil.planMaintenance">
                <v-sheet class="pa-3 mb-3" elevation="1" rounded color="grey-lighten-4">
                  <h4 class="mb-2">Plan de maintenance</h4>

                  <!-- Informations du PM -->
                  <v-row dense class="mb-3">
                    <v-col cols="12" md="6">
                      <strong>Nom :</strong>
                      <div>{{ seuil.planMaintenance.nom }}</div>
                    </v-col>
                    <v-col cols="12" md="6">
                      <strong>Type :</strong>
                      <div>{{ seuil.planMaintenance.type }}</div>
                    </v-col>
                  </v-row>

                  <v-row dense class="mb-3">
                    <v-col cols="12">
                      <strong>Commentaire :</strong>
                      <div>
                        {{ seuil.planMaintenance.commentaire || "Aucun commentaire" }}
                      </div>
                    </v-col>
                  </v-row>

                  <v-row dense class="mb-3">
                    <v-col cols="12">
                      <strong>Requis :</strong>
                      <div class="d-flex gap-3">
                        <v-chip :color="seuil.planMaintenance.necessiteHabilitationElectrique
                          ? 'orange'
                          : 'grey'
                          " size="small" label>
                          <v-icon left small>{{
                            seuil.planMaintenance.necessiteHabilitationElectrique
                              ? "mdi-check"
                              : "mdi-close"
                          }}</v-icon>
                          Habilitation électrique
                        </v-chip>
                        <v-chip :color="seuil.planMaintenance.necessitePermisFeu ? 'red' : 'grey'
                          " size="small" label>
                          <v-icon left small>{{
                            seuil.planMaintenance.necessitePermisFeu
                              ? "mdi-check"
                              : "mdi-close"
                          }}</v-icon>
                          Permis feu
                        </v-chip>
                      </div>
                    </v-col>
                  </v-row>

                  <!-- Consommables -->
                  <v-sheet class="pa-3 mb-3" elevation="0" rounded color="white">
                    <h5 class="mb-2">Consommables nécessaires</h5>

                    <div v-if="!seuil.planMaintenance.consommables?.length" class="text-grey">
                      Aucun consommable requis
                    </div>

                    <v-row v-for="(consommable, consIndex) in seuil.planMaintenance
                      .consommables" :key="consommable.id" dense class="mb-1">
                      <v-col cols="8">
                        <v-icon left small>mdi-package-variant</v-icon>
                        {{ consommable.designation }}
                      </v-col>
                      <v-col cols="4"> Quantité : {{ consommable.quantite }} </v-col>
                    </v-row>
                  </v-sheet>

                  <!-- Documents -->
                  <v-sheet class="pa-3" elevation="0" rounded color="white">
                    <h5 class="mb-2">Documents associés</h5>

                    <div v-if="!seuil.planMaintenance.documents?.length" class="text-grey">
                      Aucun document
                    </div>

                    <v-row v-for="(doc, docIndex) in seuil.planMaintenance.documents" :key="doc.id" dense
                      class="mb-2 align-center">
                      <v-col cols="3">
                        <strong>{{ doc.nom || doc.titre || "Sans titre" }}</strong>
                      </v-col>
                      <v-col cols="5">
                        <v-icon left small>mdi-file</v-icon>
                        {{ getFileName(doc.chemin || doc.path) || "—" }}
                      </v-col>
                      <v-col cols="3">
                        <v-chip size="small" label>
                          {{ doc.type }}
                        </v-chip>
                      </v-col>
                      <v-col cols="1" class="text-right">
                        <v-btn :href="MEDIA_BASE_URL + doc.chemin" target="_blank" icon small>
                          <v-icon>mdi-open-in-new</v-icon>
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-sheet>
                </v-sheet>
              </div>

              <div v-else class="pa-4 text-center text-grey">
                <v-icon large class="mb-2">mdi-alert-circle-outline</v-icon>
                <div>Aucun plan de maintenance associé à ce seuil</div>
              </div>

              <!-- Boutons d'action pour ce seuil -->
              <div class="d-flex justify-end mt-3">
                <v-btn color="primary" size="small" @click="editSeuil(seuil)">
                  <v-icon left small>mdi-pencil</v-icon>
                  Modifier ce seuil
                </v-btn>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </div>

      <!-- Message si aucun seuil -->
      <div v-else class="pa-4 text-center text-grey">
        <v-icon large class="mb-2">mdi-information-outline</v-icon>
        <div>Aucun seuil défini pour ce compteur</div>
      </div>
    </v-card-text>

    <!-- Chargement -->
    <v-card-text v-if="loading" class="text-center">
      <v-progress-circular indeterminate></v-progress-circular>
      <div class="mt-2">Chargement des données...</div>
    </v-card-text>

    <!-- Erreur -->
    <v-card-text v-if="errorMessage" class="text-center text-red">
      <v-icon color="red">mdi-alert-circle</v-icon>
      {{ errorMessage }}
    </v-card-text>

    <!-- Actions -->
    <v-card-actions>
      <v-btn @click="router.back()" color="grey">
        <v-icon left>mdi-arrow-left</v-icon>
        Retour
      </v-btn>
      <v-spacer />
      <v-btn color="primary" @click="showEditCounterDialog(true)">
        <v-icon left>mdi-pencil</v-icon>
        Modifier le compteur
      </v-btn>
      <v-btn color="success" @click="addNewSeuil">
        <v-icon left>mdi-plus</v-icon>
        Ajouter un seuil
      </v-btn>
    </v-card-actions>
  </v-card>

  <v-dialog v-model="showCounterDialog" max-width="1000px">
    <CounterForm :counter="counter" :isCounterEdit="isCounterEdit" @close="closeCounterDialog" />
  </v-dialog>

  <v-dialog v-model="showSeuilDialog" max-width="1200px" scrollable>
    <v-card v-if="currentSeuil">
      <v-card-title class="text-h5 pa-4">
        {{ currentSeuil.id ? 'Modifier le seuil' : 'Ajouter un nouveau seuil' }}
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pa-4">
        <MaintenancePlanInlineForm v-model="currentPlan" :counters="countersForSelect" :types-p-m="typesPM"
          :consumables="consumables" :existing-p-ms="existingPMs" :show-pm-selection="true"
          :is-edit-mode="!!currentSeuil.id" :show-actions="false" @save="handleFormSave" />
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions class="pa-4">
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="closeSeuilDialog">Annuler</v-btn>
        <v-btn color="primary" :loading="saving" @click="handleFormSave({ pmMode: 'new', selectedExistingPMId: null })">
          {{ currentSeuil.id ? 'Enregistrer les modifications' : 'Créer le seuil' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useApi } from "@/composables/useApi";
import { API_BASE_URL, MEDIA_BASE_URL } from "@/utils/constants";
import CounterForm from "./CounterForm.vue";
import MaintenancePlanInlineForm from "@/components/Forms/MaintenancePlanInlineForm.vue";

const route = useRoute();
const router = useRouter();
const counterId = Number(route.params.id);

const counter = ref(null);
const openedPanels = ref([]); // Premier panel ouvert par défaut
const currentSeuil = ref(null);
const currentPlan = ref(null);

const consumables = ref([]);
const typesPM = ref([]);
const typesDocuments = ref([]);
const existingPMs = ref([]);

const loading = ref(true);
const saving = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

const showCounterDialog = ref(false);
const showSeuilDialog = ref(false);

const isCounterEdit = ref(true);

const api = useApi(API_BASE_URL);

// Computed properties
const countersForSelect = computed(() => {
  if (!counter.value) return [];

  return [{
    id: counterId,
    nom: counter.value.nomCompteur || 'Compteur actuel',
    unite: counter.value.unite || 'heures',
    valeurCourante: counter.value.valeurCourante || 0,
    estPrincipal: counter.value.estPrincipal || false
  }];
});

const progressionData = computed(() => {
  if (!counter.value || !counter.value.seuils) return {};

  const data = {};
  counter.value.seuils.forEach((seuil) => {
    if (seuil.prochaineMaintenance && counter.value.valeurCourante) {
      const progression =
        ((counter.value.valeurCourante - seuil.derniereIntervention) /
          (seuil.prochaineMaintenance - seuil.derniereIntervention)) *
        100;
      data[seuil.id] = Math.min(Math.max(progression, 0), 100);
    }
  });
  return data;
});

const getProgressionColor = (seuil) => {
  const progression = progressionData.value[seuil.id];
  if (!progression) return "grey";

  if (progression >= 100) return "red";
  if (progression >= 80) return "orange";
  if (progression >= 50) return "blue";
  return "green";
};

const getProgressionText = (seuil) => {
  const progression = progressionData.value[seuil.id];
  if (!progression) return "N/A";

  if (progression >= 100) return "Dépassé";
  return `${Math.round(progression)}%`;
};

// Méthodes utilitaires
const getFileName = (path) => path?.split("/").pop() || "—";

const getPMTypeLabel = (id) => {
  return typesPM.value.find((t) => t.id === id)?.libelle || "—";
};

const getDocumentTypeLabel = (id) => {
  return typesDocuments.value.find((t) => t.id === id)?.nomTypeDocument || "—";
};

// Méthodes de chargement
const fetchCounter = async () => {
  counter.value = await api.get(`compteurs/${counterId}`);
};

const fetchReferentials = async () => {
  const [cons, pmTypes, docTypes, pms] = await Promise.all([
    api.get("consommables/"),
    api.get("types-plan-maintenance/"),
    api.get("types-documents/"),
    api.get('plans-maintenance/'),
  ]);

  consumables.value = cons;
  typesPM.value = pmTypes;
  typesDocuments.value = docTypes;
  existingPMs.value = pms;
};

const loadPage = async () => {
  loading.value = true;
  errorMessage.value = "";

  try {
    if (!counterId) {
      throw new Error("Identifiant compteur invalide");
    }

    await Promise.all([fetchCounter(), fetchReferentials()]);
  } catch (e) {
    console.error(e);
    errorMessage.value = e.message || "Erreur lors du chargement";
  } finally {
    loading.value = false;
  }
};

// Méthodes pour les actions
const showEditCounterDialog = (isEdit) => {
  isCounterEdit.value = isEdit;
  showCounterDialog.value = true;
};

const closeCounterDialog = () => {
  showCounterDialog.value = false;
};

const addNewSeuil = () => {
  currentSeuil.value = {
    id: null,
    derniereIntervention: 0,
    prochaineMaintenance: 0,
    ecartInterventions: 0,
    estGlissant: false,
    planMaintenance: null,
  };

  currentPlan.value = {
    id: null,
    nom: '',
    type_id: null,
    description: '',
    compteurIndex: 0,
    consommables: [],
    seuil: {
      derniereIntervention: 0,
      ecartInterventions: 0,
      prochaineMaintenance: 0,
      estGlissant: false
    },
    necessiteHabilitationElectrique: false,
    necessitePermisFeu: false
  };

  showSeuilDialog.value = true;
};

const editSeuil = (seuil) => {
  currentSeuil.value = { ...seuil };

  const pm = seuil.planMaintenance;
  currentPlan.value = {
    id: pm?.id || null,
    nom: pm?.nom || '',
    type_id: pm?.type_id || null,
    description: pm?.commentaire || '',
    compteurIndex: 0,
    consommables: pm?.consommables?.map(c => c.consommable_id || c.id) || [],
    seuil: {
      derniereIntervention: seuil.derniereIntervention || 0,
      ecartInterventions: seuil.ecartInterventions || 0,
      prochaineMaintenance: seuil.prochaineMaintenance || 0,
      estGlissant: seuil.estGlissant || false
    },
    necessiteHabilitationElectrique: pm?.necessiteHabilitationElectrique || false,
    necessitePermisFeu: pm?.necessitePermisFeu || false
  };

  showSeuilDialog.value = true;
};

const closeSeuilDialog = () => {
  currentSeuil.value = null;
  currentPlan.value = null;
  showSeuilDialog.value = false;
};

const saveCounter = async (updatedCounter) => {
  try {
    await api.put(`compteurs/${counterId}/`, updatedCounter);
    await fetchCounter(); // Rafraîchir les données
    successMessage.value = "Compteur modifié avec succès";
    showCounterDialog.value = false;
  } catch (e) {
    errorMessage.value = "Erreur lors de la modification du compteur";
    console.error(e);
  }
};

const handleFormSave = (data) => {
  // Stocker les données du formulaire pour saveSeuil
  currentPlan.value.pmMode = data.pmMode;
  currentPlan.value.selectedExistingPMId = data.selectedExistingPMId;
  saveSeuil();
};

const saveSeuil = async () => {
  try {
    saving.value = true;

    let dataToSubmit;

    if (currentPlan.value.pmMode === 'existing') {
      // Mode PM existant
      dataToSubmit = {
        compteur: counterId,
        equipmentId: counter.value?.equipement_info?.id || null,
        planMaintenanceId: currentPlan.value.selectedExistingPMId,
        seuil: currentPlan.value.seuil
      };
    } else {
      // Mode nouveau PM
      dataToSubmit = {
        compteur: counterId,
        equipmentId: counter.value?.equipement_info?.id || null,
        planMaintenance: {
          nom: currentPlan.value.nom,
          type_id: currentPlan.value.type_id,
          description: currentPlan.value.description,
          consommables: currentPlan.value.consommables,
          necessiteHabilitationElectrique: currentPlan.value.necessiteHabilitationElectrique,
          necessitePermisFeu: currentPlan.value.necessitePermisFeu
        },
        seuil: currentPlan.value.seuil
      };
    }

    if (currentSeuil.value?.id) {
      // Mise à jour d'un seuil existant
      await api.put(`declenchements/${currentSeuil.value.id}/`, dataToSubmit);
    } else {
      // Création d'un nouveau seuil
      await api.post("declenchements/", dataToSubmit);
    }

    await fetchCounter(); // Rafraîchir les données
    successMessage.value = currentSeuil.value?.id
      ? "Seuil modifié avec succès"
      : "Seuil ajouté avec succès";
    closeSeuilDialog();
  } catch (e) {
    errorMessage.value = "Erreur lors de la sauvegarde du seuil";
    console.error(e);
  } finally {
    saving.value = false;
  }
};

onMounted(() => {
  loadPage();
});
</script>

<style scoped>
.gap-3 {
  gap: 12px;
}

.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
