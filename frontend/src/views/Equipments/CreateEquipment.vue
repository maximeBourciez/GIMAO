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
                      {{ item.planMaintenance?.nom.slice(0, 20) || 'Aucun plan associé' }}
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
      <v-card>
        <v-card-title>{{ isEditMode ? 'Modifier un compteur' : 'Ajouter un compteur' }}</v-card-title>

        <v-card-text>
          <!-- Informations générales -->
          <v-sheet class="pa-4 mb-4" elevation="1" rounded>
            <h4 class="mb-3">Informations générales</h4>
            <v-row dense>
              <v-col cols="12" md="6">
                <v-text-field v-model="currentCounter.nom" label="Nom du compteur" outlined dense
                  :rules="[v => !!v?.trim() || 'Le nom du compteur est requis']"></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="currentCounter.description" label="Description (optionnel)" outlined
                  dense></v-text-field>
              </v-col>
            </v-row>
            <v-row dense>
              <v-col cols="6">
                <v-text-field v-model="currentCounter.intervalle" type="number" label="Intervalle" outlined dense
                  :rules="[v => v > 0 || 'L\'intervalle doit être positif']"></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field v-model="currentCounter.unite" label="Unité" outlined dense
                  :rules="[v => !!v?.trim() || 'L\'unité est requise']"></v-text-field>
              </v-col>
            </v-row>
          </v-sheet>

          <!-- Options avancées -->
          <v-sheet class="pa-4 mb-4" elevation="1" rounded>
            <h4 class="mb-3">Options du compteur</h4>
            <v-row dense>
              <v-col cols="6">
                <v-text-field v-model.number="currentCounter.valeurActuelle" label="Valeur actuelle" type="number"
                  outlined dense></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field v-model="currentCounter.derniereIntervention" label="Dernière intervention" outlined
                  dense></v-text-field>
              </v-col>
            </v-row>
            <v-row dense justify="space-around">
              <v-checkbox v-model="currentCounter.estGlissant" label="Compteur glissant" dense outlined
                color="primary"></v-checkbox>
              <v-checkbox v-model="currentCounter.estPrincipal" label="Compteur principal" dense outlined
                color="primary"></v-checkbox>
            </v-row>
            <v-row dense>
              <v-col>
                <p class="mb-2">La maintenance nécessite :</p>
                <v-row justify="space-around" dense>
                  <v-checkbox v-model="currentCounter.habElec" label="Une habilitation électrique" dense outlined
                    color="primary"></v-checkbox>
                  <v-checkbox v-model="currentCounter.permisFeu" label="Un permis feu" dense outlined
                    color="primary"></v-checkbox>
                </v-row>

              </v-col>
            </v-row>
          </v-sheet>

          <v-divider class="my-4"></v-divider>

          <!-- Plan de maintenance -->
          <v-sheet class="pa-4 mb-4" elevation="1" rounded>
            <h4 class="mb-3">Plan de maintenance associé</h4>
            <v-row>
              <v-col cols="8">
                <v-select v-if="existingPMs.length" v-model="currentCounter.planMaintenance.nom" :items="existingPMs"
                  item-title="nom" item-value="nom" label="Sélectionner un plan existant" outlined dense clearable
                  @update:model-value="applyExistingPM" />
              </v-col>
              <v-col cols="4">
                <v-select v-model="currentCounter.planMaintenance.type" :items="typesPM" item-title="libelle"
                  item-value="id" label="Type de plan de maintenance" outlined dense></v-select>
              </v-col>
            </v-row>

            <v-text-field v-model="currentCounter.planMaintenance.nom" label="Nom du plan de maintenance" outlined dense
              :rules="[v => !!v || 'Le nom est requis']"></v-text-field>
          </v-sheet>

          <!-- Consommables -->
          <v-sheet class="pa-4 mb-4" elevation="1" rounded>
            <h4 class="mb-3">Consommables du plan</h4>
            <v-row v-for="(c, index) in currentCounter.planMaintenance.consommables" :key="index" class="mb-3" dense>
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
            <v-btn color="primary" class="mb-3" @click="addPMConsumable">Ajouter un consommable</v-btn>
          </v-sheet>

          <!-- Documents -->
          <v-sheet class="pa-4 mb-4" elevation="1" rounded>
            <h4 class="mb-3 mt-4">Documents du plan</h4>
            <v-row v-for="(doc, index) in currentCounter.planMaintenance.documents" :key="index" class="mb-3" dense>
              <v-col cols="4">
                <v-text-field v-model="doc.titre" label="Nom du document" outlined dense></v-text-field>
              </v-col>
              <v-col cols="4">
                <v-file-input label="Fichier" outlined dense accept="*" v-model="doc.file"
                  @change="handlePmDocumentUpload($event, index)"></v-file-input>
              </v-col>
              <v-col cols="4">
                <v-select v-model="doc.type" :items="typesDocuments" item-title="nomTypeDocument" item-value="id"
                  label="Type de document" outlined dense></v-select>
              </v-col>
            </v-row>
            <v-btn color="primary" class="mb-3" @click="addPMDocument">Ajouter un document</v-btn>

          </v-sheet>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeCounterDialog">Annuler</v-btn>
          <v-btn color="primary" @click="saveCurrentCounter">{{ isEditMode ? 'Modifier' : 'Ajouter' }}</v-btn>
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
  "lienImageEquipement": null,
  "createurEquipement": 2,
  "lieu": {
    "id": 2,
    "nomLieu": "Atelier principal",
    "children": [
      { "id": 4, "nomLieu": "Zone de production A", "children": [] },
      { "id": 5, "nomLieu": "Zone de production B", "children": [] }
    ]
  },
  "modeleEquipement": 3,
  "fournisseur": 2,
  "fabricant": 2,
  "famille": 2,
  "consommables": [2, 1, 3],
  "numSerie": "SN589874",

  "compteurs": [
    {
      "nom": "Compteur heures moteur",
      "description": "Suivi des heures de fonctionnement",
      "intervalle": "250",
      "unite": "heures",
      "valeurActuelle": 120,
      "derniereIntervention": "0",
      "estGlissant": true,
      "estPrincipal": true,
      "habElec": false,
      "permisFeu": false,
      "planMaintenance": {
        "nom": "Maintenance moteur",
        "type": 3,
        "consommables": [
          { "consommable": 1, "quantite": 1 },
          { "consommable": 2, "quantite": 2 }
        ],
        "documents": [
          { "titre": "Rapport_controle_elec.pdf", "file": {}, "type": 3 }
        ]
      }
    },
  ]
}
);

const locations = ref([]);
const equipmentModels = ref([]);
const fournisseurs = ref([]);
const fabricants = ref([]);
const consumables = ref([]);
const familles = ref([]);
const typesPM = ref([]);
const typesDocuments = ref([]);
const openNodes = ref(new Set());
const showCounterDialog = ref(false);
const existingPMs = ref([
  { nom: 'Plan de maintenance vidange', consommables: [{ consommable: 1, quantite: 1 }, { consommable: 2, quantite: 2 }], documents: [], type: 2 },
  { nom: 'Plan de maintenance révision', consommables: [], documents: [], type: 3 },
  { nom: 'Plan de maintenance complet', consommables: [], documents: [], type: 2 }
]);

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
    consommables: [''],
    documents: [
      { titre: '', file: null, type: null }
    ]
  }
});

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

const validation = useFormValidation(formData, {
  reference: [v => !!v || 'La référence est requise'],
  designation: [v => !!v || 'La désignation est requise'],
  modeleEquipement: [v => !!v || 'Le modèle d\'équipement est requis'],
  currentCounter: {
    nom: [v => !!v?.trim() || 'Le nom du compteur est requis'],
    intervalle: [v => !!v?.trim() || 'L\'intervalle du compteur est requis'],
    unite: [v => !!v?.trim() || 'L\'unité du compteur est requise'],
    planMaintenance: {
      nom: [v => !!v?.trim() || 'Le nom du plan de maintenance est requis']
    }
  }
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

const handlePmDocumentUpload = (event, index) => {
  console.log('📄 Gestion du téléchargement du document pour l\'index:', index);
  const files = event.target.files ? event.target.files : event;
  console.log('📂 Fichiers reçus:', files, ' - length :', files.length);
  if (files && files.length > 0) {
    const file = files[0];

    console.log('📑 Fichier sélectionné:', file);

    if (file instanceof File) {
      currentCounter.value.planMaintenance.documents[index].file = file;

      console.log('📋 Mise à jour du document à l\'index', index, 'avec le fichier:', file);

      console.log('✅ Fichier ajouté:', {
        index,
        titre: currentCounter.value.planMaintenance.documents[index].titre,
        fileName: file.name,
        fileSize: file.size,
        type: currentCounter.value.planMaintenance.documents[index].type
      });
    }
  } else {
    currentCounter.value.planMaintenance.documents[index].file = null;
    console.log('🗑️ Fichier supprimé pour document', index);
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

    // -------------------------
    // Ajouter les champs simples
    // -------------------------
    for (const key in formData.value) {
      if (key === 'lieu') {
        // Lieu : envoyer seulement l'ID
        fd.append('lieu', formData.value.lieu?.id ?? '');
        
      } else if (key === 'consommables') {
        // Consommables : JSON
        fd.append(key, JSON.stringify(formData.value[key]));
        
      } else if (key === 'compteurs') {
        // Compteurs : JSON sans les fichiers
        const compteursData = formData.value.compteurs.map(c => ({
          ...c,
          planMaintenance: {
            ...c.planMaintenance,
            // Documents sans les fichiers (juste métadonnées)
            documents: c.planMaintenance.documents.map(d => ({
              titre: d.titre,
              type: d.type
            }))
          }
        }));
        fd.append(key, JSON.stringify(compteursData));
        
      } else if (key === 'lienImageEquipement') {
        // Image de l'équipement
        if (formData.value[key] instanceof File) {
          fd.append('lienImageEquipement', formData.value[key]);
        }
        
      } else if (formData.value[key] !== null && formData.value[key] !== undefined) {
        // Autres champs simples
        fd.append(key, formData.value[key]);
      }
    }

    // -------------------------
    // Ajouter les fichiers des documents des plans de maintenance
    // -------------------------
    console.log('📤 Ajout des fichiers des documents...');
    
    formData.value.compteurs.forEach((compteur, compteurIndex) => {
      compteur.planMaintenance.documents.forEach((doc, docIndex) => {
        if (doc.file instanceof File) {
          // ✅ Format correct pour correspondre au backend
          const fileKey = `compteur_${compteurIndex}_document_${docIndex}`;
          fd.append(fileKey, doc.file);
          
          console.log(`  ✓ Fichier ajouté: ${fileKey} = ${doc.file.name} (${doc.file.size} bytes)`);
        }
      });
    });

    // -------------------------
    // Debug : afficher le contenu du FormData
    // -------------------------
    console.log('\n📦 Contenu du FormData à envoyer:');
    for (let [key, value] of fd.entries()) {
      if (value instanceof File) {
        console.log(`  ${key}: [FILE] ${value.name} (${value.size} bytes)`);
      } else {
        console.log(`  ${key}:`, value);
      }
    }

    // -------------------------
    // Envoyer la requête
    // -------------------------
    console.log('\n🚀 Envoi de la requête...');
    
    await api.post('equipements/', fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    console.log('✅ Requête réussie !');
    successMessage.value = 'Équipement créé avec succès';
    
    setTimeout(() => router.back(), 1500);

  } catch (e) {
    console.error('❌ Erreur lors de la création:', e);
    console.error('Détails:', e.response?.data);
    
    errorMessage.value = 'Erreur lors de la création de l\'équipement';
    
    if (e.response?.data) {
      // Afficher les erreurs de validation si disponibles
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
  pmDocuments.value = [];
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

const addPMDocument = () => {
  const docs = currentCounter.value.planMaintenance.documents;
  // Vérifie si le dernier document est vide
  if (!docs.length || docs[docs.length - 1].titre) {
    docs.push({
      titre: '',
      file: null,
      type: null
    });
  }
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
    type: pm.type || null,
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

  // S'assurer que les consommables ont le bon format
  if (counterToSave.planMaintenance.consommables) {
    counterToSave.planMaintenance.consommables = counterToSave.planMaintenance.consommables
      .filter(c => c.consommable) // Filtrer les consommables non sélectionnés
      .map(c => ({
        consommable: c.consommable,
        quantite: c.quantite || 1
      }));
  }
  counterToSave.planMaintenance.documents = counterToSave.planMaintenance.documents.filter(doc => doc.titre || doc.file);


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

  console.log('✅ Compteur sauvegardé:', counterToSave);
};

const updateExistingPM = (counterToSave) => {
  const pmNom = counterToSave.planMaintenance.nom;
  if (!pmNom) return;

  const existingPMIndex = existingPMs.value.findIndex(pm => pm.nom === pmNom);

  if (existingPMIndex >= 0) {
    // Mettre à jour le PM existant
    existingPMs.value[existingPMIndex] = {
      nom: pmNom,
      type: counterToSave.planMaintenance.type || null,
      consommables: [...counterToSave.planMaintenance.consommables],
      documents: [...counterToSave.planMaintenance.documents]
    };
  } else {
    // Ajouter comme nouveau PM
    existingPMs.value.push({
      nom: pmNom,
      type: counterToSave.planMaintenance.type || null,
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