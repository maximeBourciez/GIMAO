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

              <v-col cols="12" md="6">
                <v-select v-model="formData.fabricant" :items="fabricants" item-title="nom" item-value="id"
                  label="Fabricant" outlined dense></v-select>
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
                    <v-btn icon color="red" @click="formData.compteurs = formData.compteurs.filter(c => c !== item)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                    <v-btn icon color="blue" @click="console.log('Modifier le compteur', item)">
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

    <v-dialog v-model="showCounterDialog" max-width="500px">
      <v-card>
        <v-card-title>Ajouter un compteur</v-card-title>

        <v-card-text>
          <v-text-field v-model="newCounter.nom" label="Nom du compteur" outlined dense></v-text-field>

          <v-text-field v-model="newCounter.intervalle" type="number" label="Intervalle" outlined dense></v-text-field>

          <v-text-field v-model="newCounter.unite" label="Unité" outlined dense></v-text-field>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn text @click="showCounterDialog = false">Annuler</v-btn>
          <v-btn color="primary" @click="saveNewCounter">Ajouter</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { VTreeview } from 'vuetify/labs/VTreeview';
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


const formData = ref({
  reference: '',
  designation: '',
  dateCreation: new Date().toISOString(),
  dateMiseEnService: new Date().toISOString().substr(0, 10),
  prixAchat: null,
  lienImageEquipement: null,
  createurEquipement: 1,
  lieu: null,
  modeleEquipement: null,
  fournisseur: null,
  fabricant: null,
  consommables: [],
  compteurs: [
    { nom: 'Vidange', intervalle: '10000', unite: 'Km' }
  ]
});

const locations = ref([]);
const equipmentModels = ref([]);
const fournisseurs = ref([]);
const fabricants = ref([]);
const consumables = ref([]);
const selectedConsumables = ref([]);
const openNodes = ref(new Set());
const showCounterDialog = ref(false);

const newCounter = ref({
  nom: '',
  intervalle: '',
  unite: ''
});

const validation = useFormValidation(formData, {
  numSerie: [v => !!v || 'Le numéro de série est requis'],
  reference: [v => !!v || 'La référence est requise'],
  designation: [v => !!v || 'La désignation est requise'],
  dateMiseEnService: [v => !!v || 'La date de mise en service est requise'],
  modeleEquipement: [v => !!v || 'Le modèle d\'équipement est requis'],
});

const validateForm = () => {
  return validation.checkRequiredFields(['numSerie', 'reference', 'designation', 'dateMiseEnService', 'modeleEquipement']);
};

const selectLocation = (item) => {
  if (formData.value.lieu && formData.value.lieu.id === item.id) {
    formData.value.lieu = null;
  } else {
    formData.value.lieu = item;
  }
};

const toggleNode = (item) => {
  if (openNodes.value.has(item.id)) {
    openNodes.value.delete(item.id);
  } else {
    openNodes.value.add(item.id);
  }
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

    await Promise.all([
      locationsApi.get('lieux-hierarchy/'),
      modelsApi.get('modele-equipements/'),
      fabricantApi.get('fabricants/'),
      fournisseurApi.get('fournisseurs/'),
      consumablesApi.get('consommables/')
    ]);

    locations.value = locationsApi.data.value;
    equipmentModels.value = modelsApi.data.value;
    fournisseurs.value = fournisseurApi.data.value;
    fabricants.value = fabricantApi.data.value;
    consumables.value = consumablesApi.data.value;

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
    formData.value.dateCreation = new Date().toISOString();

    const form_data = new FormData();
    for (const key in formData.value) {
      if (formData.value[key] !== null && key !== 'lienImageEquipement') {
        if (key === 'lieu') {
          form_data.append(key, formData.value.lieu.id.toString());
        } else {
          form_data.append(key, formData.value[key]);
        }
      }
    }

    if (formData.value.lienImageEquipement instanceof File) {
      form_data.append('lienImageEquipement', formData.value.lienImageEquipement);
    }

    const response = await api.post('equipements/', form_data, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    if (response) {
      const equipement_id = response.reference;

      const information_statut_data = {
        statutEquipement: 'En fonctionnement',
        dateChangement: new Date().toISOString(),
        equipement: equipement_id,
        informationStatutParent: null,
        ModificateurStatut: 1
      };

      const statut_response = await api.post('information-statuts/', information_statut_data, {
        headers: { 'Content-Type': 'application/json' }
      });

      if (statut_response) {
        for (const consumable_id of selectedConsumables.value) {
          await api.post('constituer/', {
            equipement: equipement_id,
            consommable: consumable_id
          });
        }
      }

      successMessage.value = 'Équipement créé avec succès !';

      setTimeout(() => {
        router.go(-1);
      }, 1500);
    }
  } catch (error) {
    console.error('Erreur lors de la création de l\'équipement:', error);
    errorMessage.value = 'Erreur lors de la création de l\'équipement. Veuillez réessayer.';
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
  newCounter.value = { nom: '', intervalle: '', unite: '' };
  showCounterDialog.value = true;
};

const saveNewCounter = () => {
  if (!newCounter.value.nom || !newCounter.value.intervalle || !newCounter.value.unite) {
    return; // tu peux mettre un message d'erreur si tu veux
  }

  formData.value.compteurs.push({ ...newCounter.value });

  showCounterDialog.value = false;
};

onMounted(() => {
  fetchData();
});

components: {
  VTreeview
}

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
</style>