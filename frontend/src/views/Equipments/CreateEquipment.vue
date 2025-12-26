<template>
  <v-app>
    <v-main>
      <v-container>
        <BaseForm v-model="formData" title="Créer un Équipement" :loading="loading" :error-message="errorMessage"
          :success-message="successMessage" :loading-message="loadingData ? 'Chargement des données...' : ''"
          :custom-validation="validateForm" submit-button-text="Créer un Équipement" :handleSubmit="handleSubmit">
          <template #default="{ formData }">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field v-model="formData.numSerie" label="Numéro de série" type="text" outlined
                  dense></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field v-model="formData.reference" label="Référence" outlined dense required></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field v-model="formData.designation" label="Désignation" outlined dense required
                  :rules="[v => !!v || 'La désignation est requise']"></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field v-model="formData.dateMiseEnService" label="Date de mise en service" type="date" outlined
                  dense></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field v-model="formData.prixAchat" label="Prix d'achat" type="number" outlined
                  dense></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-file-input label="Image de l'équipement" outlined dense accept="image/*"
                  @change="handleFileUpload"></v-file-input>
              </v-col>

              <v-col cols="12" md="6">
                <v-select v-model="formData.modeleEquipement" :items="equipmentModels" item-title="nom" item-value="id"
                  label="Modèle de l'équipement" outlined dense>
                  <template #append-item>
                    <v-divider class="mt-2" />
                    <v-list-item class="text-primary" @click="openModeleDialog">
                      <v-list-item-title>
                        <v-icon left size="18">mdi-plus</v-icon>
                        Créer un modèle d'équipement
                      </v-list-item-title>
                    </v-list-item>
                  </template>
                </v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-select v-model="formData.fournisseur" :items="fournisseurs" item-title="nom" item-value="id"
                  label="Fournisseur" outlined dense>

                  <template #append-item>
                    <v-divider class="mt-2" />
                    <v-list-item class="text-primary" @click="openFournisseurDialog">
                      <v-list-item-title>
                        <v-icon left size="18">mdi-plus</v-icon>
                        Créer un fournisseur
                      </v-list-item-title>
                    </v-list-item>
                  </template>
                </v-select>
              </v-col>

              <v-col cols="6" md="6">
                <v-select v-model="formData.fabricant" :items="fabricants" item-title="nom" item-value="id"
                  label="Fabricant" outlined dense>
                  <template #append-item>
                    <v-divider class="mt-2" />
                    <v-list-item class="text-primary" @click="openFabricantDialog">
                      <v-list-item-title>
                        <v-icon left size="18">mdi-plus</v-icon>
                        Créer un fabricant
                      </v-list-item-title>
                    </v-list-item>
                  </template>
                </v-select>
              </v-col>


              <v-col cols="6" md="6">
                <v-select v-model="formData.famille" :items="familles" item-title="nom" item-value="id"
                  label="Famille d'équipement" outlined dense>
                  <template #append-item>
                    <v-divider class="mt-2" />
                    <v-list-item class="text-primary" @click="openFamilleDialog">
                      <v-list-item-title>
                        <v-icon left size="18">mdi-plus</v-icon>
                        Créer une famille d'équipement
                      </v-list-item-title>
                    </v-list-item>
                  </template>
                </v-select>
              </v-col>

              <v-col cols="6">
                <LocationTreeView :items="locations" v-model:selected="formData.lieu" />
              </v-col>

              <v-col cols="6">
                <v-select v-model="formData.statut" :items="equipmentStatuses" item-title="label" item-value="value"
                  label="Statut de l'équipement" outlined dense></v-select>
              </v-col>

              <v-col cols="12">
                <v-divider class="my-4"></v-divider>
                <h3 class="mb-3">Consommables Associés</h3>
                <v-select v-model="formData.consommables" :items="consumables" item-title="designation" item-value="id"
                  label="Sélectionner les consommables" multiple chips outlined dense></v-select>
              </v-col>

              <v-divider class="my-4"></v-divider>

              <v-col cols="12">
                <v-row cols="12" class="mb-2" align="center" justify="space-between">
                  <h3 class="mb-3">Compteurs Associés</h3>
                  <v-btn color="primary" class="mr-4 my-1" @click="handleCounterAdd">
                    Ajouter un Compteur
                  </v-btn>
                </v-row>
                <v-data-table :items="formData.compteurs" :headers="counterTableHeaders" class="elevation-1">
                  <template #item.nom="{ item }">
                    {{ item.nom }}
                  </template>
                  <template #item.intervalle="{ item }">
                    {{ item.intervalle }}
                  </template>
                  <template #item.unite="{ item }">
                    {{ item.unite }}
                  </template>
                  <template #item.options="{ item }">
                    <div>
                      <div>
                        {{ item.estGlissant && item.estPrincipal ? 'Glissant et Principal' :
                          item.estGlissant ? 'Glissant' :
                            item.estPrincipal ? 'Principal' :
                              'Aucune' }}
                      </div>
                    </div>
                  </template>
                  <template #item.planMaintenance="{ item }">
                    <div>
                      <v-icon left small>mdi-wrench</v-icon>
                      {{ item.planMaintenance?.nom?.slice(0, 20) || 'Aucun plan associé' }}
                    </div>
                  </template>
                  <template #item.actions="{ item }">
                    <v-row>
                      <v-btn icon color="blue" @click="handleCounterEdit(item)" size="30" class="mr-2">
                        <v-icon size="14">mdi-pencil</v-icon>
                      </v-btn>
                      <v-btn icon color="red" @click="handleCounterDelete(item)" size="30">
                        <v-icon size="14">mdi-delete</v-icon>
                      </v-btn>
                    </v-row>
                  </template>
                </v-data-table>
              </v-col>
            </v-row>
          </template>
        </BaseForm>
      </v-container>
    </v-main>

    <v-dialog v-model="showCounterDialog" max-width="1000px" @click:outside="closeCounterDialog">
      <CounterForm v-model="currentCounter" :existingPMs="existingPMs" :typesPM="typesPM" :consumables="consumables"
        :typesDocuments="typesDocuments" :isEditMode="isEditMode" @save="saveCurrentCounter"
        @close="closeCounterDialog" />
    </v-dialog>

    <v-dialog v-model="showFabricantDialog" max-width="80%">
      <FabricantForm @created="handleFabricantCreated" @close="closeFabricantDialog" />
    </v-dialog>

    <v-dialog v-model="showFournisseurDialog" max-width="80%">
      <FournisseurForm @created="handleFournisseurCreated" @close="closeFournisseurDialog" />
    </v-dialog>

    <v-dialog v-model="showModeleDialog" max-width="80%">
      <ModeleEquipementForm :fabricants="fabricants" @created="handleModeleCreated" @close="closeModeleDialog" />
    </v-dialog>

    <v-dialog v-model="showFamilleDialog" max-width="50%" >
      <FamilleEquipementForm :families="familles" @created="handleFamilleCreated" @close="closeFamilleDialog" />
    </v-dialog>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import BaseForm from '@/components/common/BaseForm.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';
import LocationTreeView from '@/components/LocationTreeView.vue';
import { EQUIPMENT_STATUS } from '@/utils/constants.js';
import CounterForm from '@/components/Forms/CounterForm.vue';
import FabricantForm from '@/components/Forms/FabricantForm.vue';
import FournisseurForm from '@/components/Forms/FournisseurForm.vue';
import ModeleEquipementForm from '@/components/Forms/ModeleEquipementForm.vue';
import FamilleEquipementForm from '@/components/Forms/FamilleEquipementForm.vue';

const router = useRouter();
const api = useApi(API_BASE_URL);

const loading = ref(false);
const loadingData = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const isEditMode = ref(false);
const editingCounterIndex = ref(-1);

const formData = ref({
  numSerie: '',
  reference: '',
  designation: '',
  dateMiseEnService: '',
  prixAchat: null,
  lienImageEquipement: null,
  modeleEquipement: null,
  fournisseur: null,
  fabricant: null,
  famille: null,
  lieu: null,
  statut: null,
  consommables: [],
  compteurs: [],
  createurEquipement: 3
});

const locations = ref([]);
const equipmentModels = ref([]);
const fournisseurs = ref([]);
const fabricants = ref([]);
const consumables = ref([]);
const familles = ref([]);
const typesPM = ref([]);
const typesDocuments = ref([]);

// Modales
const showCounterDialog = ref(false);
const showFabricantDialog = ref(false);
const showFournisseurDialog = ref(false);
const showModeleDialog = ref(false);
const showFamilleDialog = ref(false);

const existingPMs = ref([
  { nom: 'Plan de maintenance vidange', consommables: [{ consommable: 1, quantite: 1 }, { consommable: 2, quantite: 2 }], documents: [], type: 2 },
  { nom: 'Plan de maintenance révision', consommables: [], documents: [], type: 3 },
  { nom: 'Plan de maintenance complet', consommables: [], documents: [], type: 2 }
]);

const equipmentStatuses = computed(() => {
  return Object.entries(EQUIPMENT_STATUS).map(([value, label]) => ({
    value,
    label
  }));
});

const getEmptyCounter = () => ({
  nom: '',
  description: '',
  intervalle: '',
  unite: '',
  valeurActuelle: null,
  derniereIntervention: null,
  estGlissant: false,
  estPrincipal: false,
  habElec: false,
  permisFeu: false,
  planMaintenance: {
    nom: '',
    type: null,
    consommables: [],
    documents: []
  }
});

const currentCounter = ref(getEmptyCounter());

const validateForm = () => {
  const requiredFields = ['numSerie', 'reference', 'designation', 'modeleEquipement', 'lieu', 'statut'];
  let isValid = true;

  requiredFields.forEach(field => {
    if (!formData.value[field]) {
      isValid = false;
    }
  });

  if (formData.value.compteurs.length === 0) {
    errorMessage.value = 'Au moins un compteur est requis';
    isValid = false;
  }

  return isValid;
};

const handleFileUpload = (event) => {
  const file = event.target.files ? event.target.files[0] : event;
  if (file) {
    formData.value.lienImageEquipement = file;
  }
};

const fetchData = async () => {
  loadingData.value = true;
  errorMessage.value = '';

  try {
    const locationsApi = useApi(API_BASE_URL);
    const modelsApi = useApi(API_BASE_URL);
    const fournisseurApi = useApi(API_BASE_URL);
    const fabricantApi = useApi(API_BASE_URL);
    const consumablesApi = useApi(API_BASE_URL);
    const famillesApi = useApi(API_BASE_URL);
    const typesPMApi = useApi(API_BASE_URL);
    const typesDocumentsApi = useApi(API_BASE_URL);

    await Promise.all([
      locationsApi.get('lieux-hierarchy/'),
      modelsApi.get('modele-equipements/'),
      fabricantApi.get('fabricants/'),
      fournisseurApi.get('fournisseurs/'),
      consumablesApi.get('consommables/'),
      famillesApi.get('famille-equipements/'),
      typesPMApi.get('types-plan-maintenance/'),
      typesDocumentsApi.get('types-documents/')
    ]);

    locations.value = locationsApi.data.value;
    equipmentModels.value = modelsApi.data.value;
    fournisseurs.value = fournisseurApi.data.value;
    fabricants.value = fabricantApi.data.value;
    consumables.value = consumablesApi.data.value;
    familles.value = famillesApi.data.value;
    typesPM.value = typesPMApi.data.value;
    typesDocuments.value = typesDocumentsApi.data.value;

  } catch (error) {
    console.error('Erreur lors du chargement des données:', error);
    errorMessage.value = 'Erreur lors du chargement des données. Veuillez réessayer.';
  } finally {
    loadingData.value = false;
  }
};

const handleSubmit = async () => {
  if (!validateForm()) return;

  loading.value = true;
  errorMessage.value = '';

  try {
    const fd = new FormData();

    // Ajouter les champs simples
    for (const key in formData.value) {
      if (key === 'lieu') {
        fd.append('lieu', formData.value.lieu?.id ?? '');
      } else if (key === 'consommables') {
        fd.append(key, JSON.stringify(formData.value[key]));
      } else if (key === 'compteurs') {
        const compteursData = formData.value.compteurs.map(c => ({
          ...c,
          planMaintenance: {
            ...c.planMaintenance,
            documents: c.planMaintenance.documents.map(d => ({
              titre: d.titre,
              type: d.type
            }))
          }
        }));
        fd.append(key, JSON.stringify(compteursData));
      } else if (key === 'lienImageEquipement') {
        if (formData.value[key] instanceof File) {
          fd.append('lienImageEquipement', formData.value[key]);
        }
      } else if (formData.value[key] !== null && formData.value[key] !== undefined) {
        fd.append(key, formData.value[key]);
      }
    }

    // Ajouter les fichiers des documents des plans de maintenance
    formData.value.compteurs.forEach((compteur, compteurIndex) => {
      compteur.planMaintenance.documents.forEach((doc, docIndex) => {
        if (doc.file instanceof File) {
          const fileKey = `compteur_${compteurIndex}_document_${docIndex}`;
          fd.append(fileKey, doc.file);
        }
      });
    });

    await api.post('equipements/', fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    successMessage.value = 'Équipement créé avec succès';
    setTimeout(() => router.back(), 1500);

  } catch (e) {
    console.error('❌ Erreur lors de la création:', e);
    errorMessage.value = 'Erreur lors de la création de l\'équipement';

    if (e.response?.data) {
      const errors = Object.entries(e.response.data)
        .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
        .join('\n');
      errorMessage.value += `\n${errors}`;
    }
  } finally {
    loading.value = false;
  }
};

const counterTableHeaders = [
  { title: 'Nom du compteur', value: 'nom' },
  { title: 'Intervalle de maintenance', value: 'intervalle' },
  { title: 'Unité', value: 'unite' },
  { title: 'Valeur actuelle', value: 'valeurActuelle' },
  { title: 'Dernière intervention', value: 'derniereIntervention' },
  { title: 'Plan de maintenance', value: 'planMaintenance' },
  { title: 'Options', value: 'options', sortable: false },
  { title: 'Actions', value: 'actions', sortable: false }
];

const handleCounterAdd = () => {
  editingCounterIndex.value = -1;
  isEditMode.value = false;
  currentCounter.value = getEmptyCounter();
  showCounterDialog.value = true;
};

const handleCounterEdit = (counter) => {
  editingCounterIndex.value = formData.value.compteurs.indexOf(counter);
  isEditMode.value = true;

  currentCounter.value = {
    ...counter,
    planMaintenance: {
      ...counter.planMaintenance,
      consommables: counter.planMaintenance?.consommables
        ? counter.planMaintenance.consommables.map(c => ({ ...c }))
        : [],
      documents: counter.planMaintenance?.documents
        ? counter.planMaintenance.documents.map(d => ({ ...d }))
        : []
    }
  };

  showCounterDialog.value = true;
};

const handleCounterDelete = (counter) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer ce compteur ?')) {
    formData.value.compteurs = formData.value.compteurs.filter(c => c !== counter);
  }
};

const saveCurrentCounter = () => {
  // Validation déléguée au CounterForm, on suppose que les données sont valides ici

  const counterToSave = {
    ...currentCounter.value,
    planMaintenance: {
      ...currentCounter.value.planMaintenance,
      consommables: currentCounter.value.planMaintenance.consommables
        .filter(c => c.consommable)
        .map(c => ({ ...c })),
      documents: currentCounter.value.planMaintenance.documents
        .filter(d => d.titre || d.file)
        .map(d => ({
          titre: d.titre,
          type: d.type,
          file: d.file
        }))
    }
  };

  if (editingCounterIndex.value >= 0) {
    // Modification
    formData.value.compteurs[editingCounterIndex.value] = counterToSave;
    updateExistingPM(counterToSave);
  } else {
    // Ajout
    formData.value.compteurs.push(counterToSave);

    if (counterToSave.planMaintenance.nom &&
      !existingPMs.value.some(pm => pm.nom === counterToSave.planMaintenance.nom)) {
      existingPMs.value.push({
        nom: counterToSave.planMaintenance.nom,
        type: counterToSave.planMaintenance.type,
        consommables: [...counterToSave.planMaintenance.consommables],
        documents: [...counterToSave.planMaintenance.documents]
      });
    }
  }

  // Fermer la dialog après la sauvegarde
  closeCounterDialog();
};

const updateExistingPM = (counterToSave) => {
  const pmNom = counterToSave.planMaintenance.nom;
  if (!pmNom) return;

  const existingPMIndex = existingPMs.value.findIndex(pm => pm.nom === pmNom);

  if (existingPMIndex >= 0) {
    existingPMs.value[existingPMIndex] = {
      nom: pmNom,
      type: counterToSave.planMaintenance.type || null,
      consommables: [...counterToSave.planMaintenance.consommables],
      documents: [...counterToSave.planMaintenance.documents]
    };
  } else {
    existingPMs.value.push({
      nom: pmNom,
      type: counterToSave.planMaintenance.type || null,
      consommables: [...counterToSave.planMaintenance.consommables],
      documents: [...counterToSave.planMaintenance.documents]
    });
  }
};


// -------------------------------
// Modales Fabricant, Fournisseur, Modele, Famille Equipement
// -------------------------------
// Fabricant
const openFabricantDialog = () => {
  showFabricantDialog.value = true
}

const closeFabricantDialog = () => {
  showFabricantDialog.value = false
}

const handleFabricantCreated = (newFabricant) => {
  fabricants.value.push(newFabricant)
  formData.value.fabricant = newFabricant.id
}

// Fournisseur
const openFournisseurDialog = () => {
  showFournisseurDialog.value = true
}

const closeFournisseurDialog = () => {
  showFournisseurDialog.value = false
}

const handleFournisseurCreated = (newFournisseur) => {
  fournisseurs.value.push(newFournisseur)
  formData.value.fournisseur = newFournisseur.id
}

// Modèle Equipement
const openModeleDialog = () => {
  showModeleDialog.value = true;
};

const closeModeleDialog = () => {
  showModeleDialog.value = false;
};

const handleModeleCreated = (newModele) => {
  equipmentModels.value.push(newModele);
  formData.value.modeleEquipement = newModele.id;
};

// Famille Equipement
const openFamilleDialog = () => {
  showFamilleDialog.value = true;
};

const closeFamilleDialog = () => {
  showFamilleDialog.value = false;
};

const handleFamilleCreated = (newFamille) => {
  console.log('Nouvelle famille créée:', newFamille);
  familles.value.push(newFamille);
  formData.value.famille = newFamille.id;
};




const closeCounterDialog = () => {
  showCounterDialog.value = false;
  editingCounterIndex.value = -1;
  isEditMode.value = false;
  currentCounter.value = getEmptyCounter();
  errorMessage.value = '';
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.rotate-icon {
  transform: rotate(90deg);
  transition: transform 0.2s;
}

.tree-icon-placeholder {
  display: inline-block;
  width: 24px;
}

.location-tree {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 8px;
}
</style>