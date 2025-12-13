<template>
  <v-app>
    <v-main>
      <v-container>
        <BaseForm v-model="formData" title="Créer un Équipement" :loading="loading" :error-message="errorMessage"
          :success-message="successMessage" :loading-message="loadingData ? 'Chargement des données...' : ''"
          :custom-validation="validateForm" submit-button-text="Créer un Équipement" @submit="handleSubmit">
          <template #default="{ formData }">
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field v-model="formData.numSerie" label="Numéro de série" type="text" outlined
                  dense></v-text-field>
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field v-model="formData.reference" label="Référence" outlined dense required
                  :rules="[v => !!v || 'La référence est requise']"></v-text-field>
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
                  label="Modèle de l'équipement" outlined dense></v-select>
              </v-col>

              <v-col cols="12" md="6">
                <v-select v-model="formData.fournisseur" :items="fournisseurs" item-title="nom" item-value="id"
                  label="Fournisseur" outlined dense></v-select>
              </v-col>

              <v-col cols="6" md="6">
                <v-select v-model="formData.fabricant" :items="fabricants" item-title="nom" item-value="id"
                  label="Fabricant" outlined dense></v-select>
              </v-col>

              <v-col cols="6" md="6">
                <v-select v-model="formData.famille" :items="familles" item-title="nom" item-value="id"
                  label="Famille d'équipement" outlined dense></v-select>
              </v-col>

              <v-col cols="6">
                <LocationTreeView :items="locations" v-model:selected="formData.lieu" />
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
                  <template #item.actions="{ item }">
                    <v-btn icon color="red" @click="handleCounterDelete(item)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                    <v-btn icon color="blue" @click="handleCounterEdit(item)">
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                  </template>
                </v-data-table>
              </v-col>
            </v-row>
          </template>
        </BaseForm>
      </v-container>
    </v-main>

    <v-dialog v-model="showCounterDialog" max-width="1000px" @click:outside="closeCounterDialog">
      <v-card>
        <v-card-title>{{ isEditMode ? 'Modifier un compteur' : 'Ajouter un compteur' }}</v-card-title>

        <v-card-text>
          <v-text-field v-model="currentCounter.nom" label="Nom du compteur" outlined dense
            :rules="[v => !!v?.trim() || 'Le nom est requis']"></v-text-field>

          <v-text-field v-model="currentCounter.intervalle" type="number" label="Intervalle" outlined dense
            :rules="[v => !!v?.trim() || 'L\'intervalle est requis']"></v-text-field>

          <v-text-field v-model="currentCounter.unite" label="Unité" outlined dense
            :rules="[v => !!v?.trim() || 'L\'unité est requise']"></v-text-field>

          <v-divider class="my-4"></v-divider>

          <h4>Plan de maintenance associé (optionnel)</h4>

          <v-select v-model="currentCounter.planMaintenance.nom" :items="existingPMs" v-if="existingPMs.length > 0" item-title="nom" item-value="nom"
            label="Sélectionner un plan de maintenance" outlined dense clearable
            @update:model-value="applyExistingPM" />

          <div>
            <v-text-field v-model="currentCounter.planMaintenance.nom" label="Nom du plan de maintenance" outlined
              dense></v-text-field>

            <v-row class="mt-4">
              <v-col cols="12">
                <h4>Consommables du plan de maintenance</h4>

                <v-btn color="primary" class="my-2" @click="addPMConsumable">
                  Ajouter un consommable
                </v-btn>
              </v-col>
            </v-row>

            <v-row v-for="(c, index) in currentCounter.planMaintenance.consommables" :key="index" class="mb-3">
              <v-col cols="6">
                <v-select v-model="c.consommable" :items="consumables" item-title="designation" item-value="id"
                  label="Consommable" outlined dense></v-select>
              </v-col>

              <v-col cols="3">
                <v-text-field v-model.number="c.quantite" type="number" min="1" label="Quantité" outlined
                  dense></v-text-field>
              </v-col>

              <v-col cols="3" class="d-flex align-center">
                <v-btn icon color="red" @click="removePMConsumable(index)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>

            <v-row class="mt-4">
              <v-col cols="12">
                <v-file-input v-model="pmDocuments" label="Documents du PM" multiple outlined dense accept="*"
                  @update:model-value="handlePMDocuments" />
              </v-col>
            </v-row>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeCounterDialog">Annuler</v-btn>
          <v-btn color="primary" @click="saveCurrentCounter">
            {{ isEditMode ? 'Modifier' : 'Ajouter' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import BaseForm from '@/components/common/BaseForm.vue';
import { useApi } from '@/composables/useApi';
import { useFormValidation } from '@/composables/useFormValidation';
import { API_BASE_URL } from '@/utils/constants';
import LocationTreeView from '@/components/LocationTreeView.vue';

const router = useRouter();
const api = useApi(API_BASE_URL);

const loading = ref(false);
const loadingData = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const isEditMode = ref(false);
const editingCounterIndex = ref(-1);
const pmDocuments = ref([]);

const formData = ref({
  "reference": "Référence de test",
  "designation": "Désignation test",
  "dateCreation": "2025-12-12T22:00:31.543Z",
  "dateMiseEnService": "2025-12-12",
  "prixAchat": "2500",
  "lienImageEquipement": "[object File]",
  "createurEquipement": 2,
  "lieu": {
    "id": 2,
    "nomLieu": "Atelier principal",
    "children": [
      {
        "id": 4,
        "nomLieu": "Zone de production A",
        "children": []
      },
      {
        "id": 5,
        "nomLieu": "Zone de production B",
        "children": []
      }
    ]
  },
  "modeleEquipement": 3,
  "fournisseur": 2,
  "fabricant": 2,
  "famille": 2,
  "consommables": [
    2,
    1,
    3
  ],
  "compteurs": [
    {
      "nom": "Compteur tets",
      "intervalle": "5",
      "unite": "jours",
      "planMaintenance": {
        "nom": "PM Test",
        "consommables": [
          {
            "consommable": 5,
            "quantite": 1
          },
          {
            "consommable": 7,
            "quantite": 5
          }
        ],
        "documents": [
          {
            "titre": "epoustouflan.jpg",
            "file": {}
          }
        ]
      }
    }
  ],
  "numSerie": "SN589874"
});

const locations = ref([]);
const equipmentModels = ref([]);
const fournisseurs = ref([]);
const fabricants = ref([]);
const consumables = ref([]);
const familles = ref([]);
const openNodes = ref(new Set());
const showCounterDialog = ref(false);
const existingPMs = ref([
  { nom: 'Plan de maintenance vidange', consommables: [{ id: 1, quantite: 1 }, { id: 2, quantite: 2 }], documents: [] },
  { nom: 'Plan de maintenance révision', consommables: [], documents: [] },
  { nom: 'Plan de maintenance complet', consommables: [], documents: [] }
]);

// DÉPLACER getEmptyCounter AVANT son utilisation
const getEmptyCounter = () => ({
  nom: '',
  intervalle: '',
  unite: '',
  planMaintenance: {
    nom: '',
    consommables: [],
    documents: []
  }
});

// Initialiser currentCounter après la déclaration de getEmptyCounter
const currentCounter = ref(getEmptyCounter());

const addPMConsumable = () => {
  currentCounter.value.planMaintenance.consommables.push({
    consommable: null,
    quantite: 1
  });
};

const removePMConsumable = (index) => {
  currentCounter.value.planMaintenance.consommables.splice(index, 1);
};

const handlePMDocuments = (files) => {
  if (files) {
    currentCounter.value.planMaintenance.documents = Array.from(files).map(file => ({
      titre: file.name,
      file: file
    }));
  } else {
    currentCounter.value.planMaintenance.documents = [];
  }
};

const validation = useFormValidation(formData, {
  reference: [v => !!v || 'La référence est requise'],
  designation: [v => !!v || 'La désignation est requise'],
  modeleEquipement: [v => !!v || 'Le modèle d\'équipement est requis'],
});

const validateForm = () => {
  const requiredFields = ['reference', 'designation', 'modeleEquipement'];
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

    await Promise.all([
      locationsApi.get('lieux-hierarchy/'),
      modelsApi.get('modele-equipements/'),
      fabricantApi.get('fabricants/'),
      fournisseurApi.get('fournisseurs/'),
      consumablesApi.get('consommables/'),
      famillesApi.get('famille-equipements/')
    ]);

    locations.value = locationsApi.data.value;
    equipmentModels.value = modelsApi.data.value;
    fournisseurs.value = fournisseurApi.data.value;
    fabricants.value = fabricantApi.data.value;
    consumables.value = consumablesApi.data.value;
    familles.value = famillesApi.data.value;

  } catch (error) {
    console.error('Erreur lors du chargement des données:', error);
    errorMessage.value = 'Erreur lors du chargement des données. Veuillez réessayer.';
  } finally {
    loadingData.value = false;
  }
};

const handleSubmit = async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    // Validation supplémentaire
    if (!validateForm()) {
      loading.value = false;
      return;
    }

    formData.value.dateCreation = new Date().toISOString();

    // Préparer les données des compteurs pour l'API
    const compteursData = formData.value.compteurs.map(counter => ({
      nom: counter.nom,
      intervalle: counter.intervalle,
      unite: counter.unite,
      planMaintenance: counter.planMaintenance.nom ? {
        nom: counter.planMaintenance.nom,
        consommables: counter.planMaintenance.consommables,
        documents: counter.planMaintenance.documents
      } : null
    }));

    const form_data = new FormData();
    
    // Ajouter les champs de base
    for (const key in formData.value) {
      if (formData.value[key] !== null && key !== 'lienImageEquipement' && key !== 'compteurs') {
        if (key === 'lieu') {
          form_data.append(key, formData.value.lieu?.id?.toString() || '');
        } else if (key === 'consommables') {
          // Ajouter les consommables comme JSON
          form_data.append(key, JSON.stringify(formData.value[key]));
        } else {
          form_data.append(key, formData.value[key]);
        }
      }
    }

    // Ajouter l'image
    if (formData.value.lienImageEquipement instanceof File) {
      form_data.append('lienImageEquipement', formData.value.lienImageEquipement);
    }

    // Ajouter les compteurs
    form_data.append('compteurs', JSON.stringify(compteursData));

    const response = await api.post('equipements/', form_data, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    if (response) {
      const equipement_id = response.reference || response.id;

      // Créer le statut de l'équipement
      const information_statut_data = {
        statutEquipement: 'En fonctionnement',
        dateChangement: new Date().toISOString(),
        equipement: equipement_id,
        informationStatutParent: null,
        ModificateurStatut: 1
      };

      await api.post('information-statuts/', information_statut_data, {
        headers: { 'Content-Type': 'application/json' }
      });

      // Associer les consommables
      for (const consumable_id of formData.value.consommables) {
        await api.post('constituer/', {
          equipement: equipement_id,
          consommable: consumable_id
        });
      }

      successMessage.value = 'Équipement créé avec succès !';

      setTimeout(() => {
        router.go(-1);
      }, 1500);
    }
  } catch (error) {
    console.error('Erreur lors de la création de l\'équipement:', error);
    errorMessage.value = error.response?.data?.message || 'Erreur lors de la création de l\'équipement. Veuillez réessayer.';
  } finally {
    loading.value = false;
  }
};

const counterTableHeaders = [
  { title: 'Nom du compteur', value: 'nom' },
  { title: 'Intervalle de maintenance', value: 'intervalle' },
  { title: 'Unité', value: 'unite' },
  { title: 'Actions', value: 'actions', sortable: false }
];

const handleCounterAdd = () => {
  editingCounterIndex.value = -1;
  isEditMode.value = false;
  currentCounter.value = getEmptyCounter();
  pmDocuments.value = [];
  showCounterDialog.value = true;
};

const handleCounterEdit = (counter) => {
  const index = formData.value.compteurs.findIndex(c => c === counter);
  editingCounterIndex.value = index;
  isEditMode.value = true;
  
  currentCounter.value = {
    nom: counter.nom,
    intervalle: counter.intervalle,
    unite: counter.unite,
    planMaintenance: {
      nom: counter.planMaintenance?.nom || '',
      consommables: JSON.parse(JSON.stringify(counter.planMaintenance?.consommables || [])),
      documents: JSON.parse(JSON.stringify(counter.planMaintenance?.documents || []))
    }
  };
  
  // Mettre à jour les fichiers pour l'affichage
  pmDocuments.value = currentCounter.value.planMaintenance.documents
    .filter(doc => doc.file)
    .map(doc => doc.file);

  showCounterDialog.value = true;
};

const handleCounterDelete = (counter) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer ce compteur ?')) {
    formData.value.compteurs = formData.value.compteurs.filter(c => c !== counter);
  }
};

const applyExistingPM = (nom) => {
  const pm = existingPMs.value.find(p => p.nom === nom);
  if (!pm) return;

  currentCounter.value.planMaintenance = {
    nom: pm.nom,
    consommables: pm.consommables ? JSON.parse(JSON.stringify(pm.consommables)) : [],
    documents: pm.documents ? JSON.parse(JSON.stringify(pm.documents)) : []
  };
  
  // Mettre à jour les fichiers pour l'affichage
  pmDocuments.value = currentCounter.value.planMaintenance.documents
    .filter(doc => doc.file)
    .map(doc => doc.file);
};

const saveCurrentCounter = () => {
  // Validation
  if (!currentCounter.value.nom?.trim() || 
      !currentCounter.value.intervalle?.trim() || 
      !currentCounter.value.unite?.trim()) {
    errorMessage.value = 'Veuillez remplir tous les champs obligatoires du compteur';
    return;
  }

  const counterToSave = JSON.parse(JSON.stringify(currentCounter.value));
  
  // S'assurer que les consommables ont le bon format
  if (counterToSave.planMaintenance.consommables) {
    counterToSave.planMaintenance.consommables = counterToSave.planMaintenance.consommables
      .filter(c => c.consommable) // Filtrer les consommables non sélectionnés
      .map(c => ({
        consommable: c.consommable,
        quantite: c.quantite || 1
      }));
  }

  if (editingCounterIndex.value >= 0 && editingCounterIndex.value < formData.value.compteurs.length) {
    // MODIFICATION
    formData.value.compteurs[editingCounterIndex.value] = counterToSave;
    updateExistingPM(counterToSave);
  } else {
    // AJOUT
    formData.value.compteurs.push(counterToSave);
    
    // Ajouter le PM à la liste existante s'il n'existe pas déjà
    if (counterToSave.planMaintenance.nom && 
        !existingPMs.value.some(pm => pm.nom === counterToSave.planMaintenance.nom)) {
      existingPMs.value.push({
        nom: counterToSave.planMaintenance.nom,
        consommables: [...counterToSave.planMaintenance.consommables],
        documents: [...counterToSave.planMaintenance.documents]
      });
    }
  }

  closeCounterDialog();
};

const updateExistingPM = (counterToSave) => {
  const pmNom = counterToSave.planMaintenance.nom;
  if (!pmNom) return;
  
  const existingPMIndex = existingPMs.value.findIndex(pm => pm.nom === pmNom);
  
  if (existingPMIndex >= 0) {
    // Mettre à jour le PM existant
    existingPMs.value[existingPMIndex] = {
      nom: pmNom,
      consommables: [...counterToSave.planMaintenance.consommables],
      documents: [...counterToSave.planMaintenance.documents]
    };
  } else {
    // Ajouter comme nouveau PM
    existingPMs.value.push({
      nom: pmNom,
      consommables: [...counterToSave.planMaintenance.consommables],
      documents: [...counterToSave.planMaintenance.documents]
    });
  }
};

const closeCounterDialog = () => {
  showCounterDialog.value = false;
  resetCounterDialog();
};

const resetCounterDialog = () => {
  editingCounterIndex.value = -1;
  isEditMode.value = false;
  currentCounter.value = getEmptyCounter();
  pmDocuments.value = [];
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