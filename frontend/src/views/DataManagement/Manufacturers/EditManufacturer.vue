<template>
  <BaseForm
    title="Modifier le fabricant"
    :loading="isSaving"
    :error-message="saveErrorMessage"
    :success-message="successMessage"
    submit-button-text="Enregistrer les modifications"
    @submit="handleSubmit"
    @cancel="goBack"
    @clear-error="saveErrorMessage = ''"
    actions-container-class="d-flex justify-end gap-2 mt-2"
  >
    <template #default>
      <!-- Infos fabricant -->
      <v-sheet class="pa-4 mb-4" elevation="1" rounded>
        <h4 class="mb-3">Fabricant</h4>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="manufacturerData.nom"
              label="Nom du fabricant *"
              outlined
              dense
              :rules="[(v) => (!!v && !!v.trim()) || 'Le nom du fabricant est requis']"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="manufacturerData.email"
              label="Email *"
              outlined
              dense
              :rules="[(v) => !v || isValidEmail(v) || 'Email invalide']"
            />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="6">
            <v-text-field
              v-model="manufacturerData.numTelephone"
              label="Téléphone *"
              outlined
              dense
              :rules="[(v) => !v || isValidPhone(v) || 'Téléphone invalide']"
            />
          </v-col>
          <v-col cols="6" class="d-flex align-center">
            <v-checkbox
              v-model="manufacturerData.serviceApresVente"
              label="Service après-vente"
              dense
            />
          </v-col>
        </v-row>
      </v-sheet>

      <!-- Adresse -->
      <v-sheet class="pa-4" elevation="1" rounded>
        <h4 class="mb-3">Adresse</h4>
        <v-row dense>
          <v-col cols="4">
            <v-text-field
              v-model="manufacturerData.adresse.numero"
              label="N° *"
              outlined
              dense
            />
          </v-col>
          <v-col cols="8">
            <v-text-field
              v-model="manufacturerData.adresse.rue"
              label="Rue *"
              outlined
              dense
              :rules="[
                (v) =>
                  !v ||
                  v.trim().length >= 2 ||
                  'La rue doit contenir au moins 2 caractères',
              ]"
            />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="6">
            <v-text-field
              v-model="manufacturerData.adresse.code_postal"
              label="Code postal *"
              outlined
              dense
              :rules="[(v) => !v || isValidPostalCode(v) || 'Code postal invalide']"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="manufacturerData.adresse.ville"
              label="Ville *"
              outlined
              dense
              :rules="[
                (v) =>
                  !v ||
                  v.trim().length >= 2 ||
                  'La ville doit contenir au moins 2 caractères',
              ]"
            />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="12">
            <v-text-field
              v-model="manufacturerData.adresse.pays"
              label="Pays *"
              outlined
              dense
              :rules="[
                (v) =>
                  !v ||
                  v.trim().length >= 2 ||
                  'Le pays doit contenir au moins 2 caractères',
              ]"
            />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="12">
            <v-text-field
              v-model="manufacturerData.adresse.complement"
              label="Complément"
              outlined
              dense
            />
          </v-col>
        </v-row>
      </v-sheet>
    </template>
  </BaseForm>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { useApi } from "@/composables/useApi";
import { API_BASE_URL } from "@/utils/constants";
import BaseForm from "@/components/common/BaseForm.vue";

const route = useRoute();
const router = useRouter();
const store = useStore();
const api = useApi(API_BASE_URL);

const manufacturerId = route.params.id;
const manufacturerData = ref({
  nom: "",
  email: "",
  numTelephone: "",
  serviceApresVente: false,
  adresse: {
    numero: "",
    rue: "",
    code_postal: "",
    ville: "",
    pays: "",
    complement: "",
  },
});
const originalData = ref(null);
const isLoading = ref(true);
const isSaving = ref(false);
const errorMessage = ref("");
const saveErrorMessage = ref("");
const successMessage = ref("");

onMounted(async () => {
  await loadManufacturerData();
});

const loadManufacturerData = async () => {
  isLoading.value = true;
  errorMessage.value = "";
  try {
    manufacturerData.value = await api.get(`fabricants/${manufacturerId}`);
    originalData.value = JSON.parse(JSON.stringify(manufacturerData.value));
  } catch (error) {
    console.error("Error loading manufacturer data:", error);
    errorMessage.value = "Erreur lors du chargement des données du fabricant";
    loader.value = false;
  } finally {
    isLoading.value = false;
  }
};

// Fonctions de validation
const isValidEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
};

const isValidPhone = (phone) => {
  return /^\+?[0-9\s\-()]{7,15}$/.test(phone);
};

const isValidPostalCode = (code) => {
  return /^[0-9]{4,6}$/.test(code.replace(/\s/g, ""));
};

const handleSubmit = async () => {
  isSaving.value = true;
  saveErrorMessage.value = "";

  const changes = detectChanges();

  changes.user = store.getters.currentUser.id;

  if (Object.keys(changes).length === 0) {
    // Aucune modification détectée
    isSaving.value = false;
    console.log("No changes detected, skipping update.");
    return;
  }

  try {
    await api.put(`fabricants/${manufacturerId}/`, changes);

    successMessage.value = "Fabricant modifié avec succès.";

    // Rediriger vers la page de détail après la modification
    setTimeout(() => {
      router.push({
        name: "ManufacturerDetail",
        params: { id: manufacturerId },
      });
    }, 2000);
  } catch (error) {
    console.error("Error updating manufacturer:", error);
    saveErrorMessage.value = "Erreur lors de la modification du fabricant";
  } finally {
    isSaving.value = false;
  }
};

const detectChanges = () => {
  const changes = {};
  changes.adresse = {};

  // Champs simples
  ["nom", "email", "numTelephone", "serviceApresVente"].forEach((field) => {
    if (manufacturerData.value[field] !== originalData.value[field]) {
      changes[field] = {
        ancienne: originalData.value[field],
        nouvelle: manufacturerData.value[field],
      };
    }
  });

  // Adresse
  const champsAdresse = ["numero", "rue", "ville", "code_postal", "pays", "complement"];
  champsAdresse.forEach((field) => {
    if (manufacturerData.value.adresse[field] !== originalData.value.adresse[field]) {
      changes.adresse[field] = {
        ancienne: originalData.value.adresse[field],
        nouvelle: manufacturerData.value.adresse[field],
      };
    }
  });

  return changes;
};

const goBack = () => {
  router.back();
};
</script>
