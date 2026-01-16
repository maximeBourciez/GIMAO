<template>
  <BaseForm
    title="Créer un Fournisseur"
    :model-value="formData"
    :loading="false"
    :error-message="errorMessage"
    :success-message="successMessage"
    submit-button-text="Créer le fournisseur"
    @submit="save"
    @clear-error=""
    @clear-success=""
  >
    <template #default="{ formData }">
      <!-- Infos fournisseur -->
      <v-sheet class="pa-4 mb-4" elevation="1" rounded>
        <h4 class="mb-3">Fournisseur</h4>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.nom"
              label="Nom du fournisseur *"
              outlined
              dense
              :error="submitted && !formData.nom.trim()"
              :error-messages="
                submitted && !formData.nom.trim()
                  ? 'Le nom du fournisseur est requis'
                  : ''
              "
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.email"
              label="Email"
              outlined
              dense
              :error="submitted && formData.email && !isValidEmail(formData.email)"
              :error-messages="
                submitted && formData.email && !isValidEmail(formData.email)
                  ? 'Email invalide'
                  : ''
              "
            />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="6">
            <v-text-field
              v-model="formData.numTelephone"
              label="Téléphone"
              outlined
              dense
              :error="
                submitted && formData.numTelephone && !isValidPhone(formData.numTelephone)
              "
              :error-messages="
                submitted && formData.numTelephone && !isValidPhone(formData.numTelephone)
                  ? 'Téléphone invalide'
                  : ''
              "
            />
          </v-col>
          <v-col cols="6" class="d-flex align-center">
            <v-checkbox
              v-model="formData.serviceApresVente"
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
            <v-text-field v-model="formData.adresse.numero" label="N°" outlined dense />
          </v-col>
          <v-col cols="8">
            <v-text-field
              v-model="formData.adresse.rue"
              label="Rue"
              outlined
              dense
              :error="
                submitted &&
                formData.adresse.rue &&
                formData.adresse.rue.trim().length < 2
              "
              :error-messages="
                submitted &&
                formData.adresse.rue &&
                formData.adresse.rue.trim().length < 2
                  ? 'La rue doit contenir au moins 2 caractères'
                  : ''
              "
            />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="6">
            <v-text-field
              v-model="formData.adresse.ville"
              label="Ville"
              outlined
              dense
              :error="
                submitted &&
                formData.adresse.ville &&
                formData.adresse.ville.trim().length < 2
              "
              :error-messages="
                submitted &&
                formData.adresse.ville &&
                formData.adresse.ville.trim().length < 2
                  ? 'La ville doit contenir au moins 2 caractères'
                  : ''
              "
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="formData.adresse.code_postal"
              label="Code postal"
              outlined
              dense
              :error="
                submitted &&
                formData.adresse.code_postal &&
                !isValidPostalCode(formData.adresse.code_postal)
              "
              :error-messages="
                submitted &&
                formData.adresse.code_postal &&
                !isValidPostalCode(formData.adresse.code_postal)
                  ? 'Code postal invalide'
                  : ''
              "
            />
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="12">
            <v-text-field
              v-model="formData.adresse.pays"
              label="Pays"
              outlined
              dense
              :error="
                submitted &&
                formData.adresse.pays &&
                formData.adresse.pays.trim().length < 2
              "
              :error-messages="
                submitted &&
                formData.adresse.pays &&
                formData.adresse.pays.trim().length < 2
                  ? 'Le pays doit contenir au moins 2 caractères'
                  : ''
              "
            />
          </v-col>
        </v-row>
        <v-text-field
          v-model="formData.adresse.complement"
          label="Complément"
          outlined
          dense
        />
      </v-sheet>
    </template>
  </BaseForm>
</template>

<script setup>
import { ref, computed } from "vue";
import { useApi } from "@/composables/useApi";
import { API_BASE_URL } from "@/utils/constants";
import { useRouter } from "vue-router";
import BaseForm from "@/components/common/BaseForm.vue";

const api = useApi(API_BASE_URL);
const router = useRouter();
const successMessage = ref("");
const errorMessage = ref("");

const props = defineProps({
  supplier: {
    type: Object,
    default: null,
  },
});

const formData = ref({
  nom: "",
  email: "",
  numTelephone: "",
  serviceApresVente: false,
  adresse: {
    numero: "",
    rue: "",
    ville: "",
    code_postal: "",
    pays: "",
    complement: "",
  },
});

const supplierId = computed(() => props.supplier?.id);
const isEditMode = computed(() => !!supplierId.value);

const emit = defineEmits(["created", "close"]);
const submitted = ref(false);

// Fonctions de validation
const isValidEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
};

const isValidPhone = (phone) => {
  return /^\+?[0-9\s\-()]{7,15}$/.test(phone);
};

const isValidPostalCode = (code) => {
  // Accepte les codes français (5 chiffres) ou autres formats
  return /^[0-9]{4,6}$/.test(code.replace(/\s/g, ""));
};

const close = () => {
  emit("close");
};

const validateForm = () => {
  // Fournisseur - nom obligatoire
  if (!formData.value.nom.trim()) {
    return false;
  }

  // Email optionnel mais doit être valide si renseigné
  if (formData.value.email && !isValidEmail(formData.value.email)) {
    return false;
  }

  // Téléphone optionnel mais doit être valide si renseigné
  if (formData.value.numTelephone && !isValidPhone(formData.value.numTelephone)) {
    return false;
  }

  // Adresse - tous les champs sont optionnels mais doivent être valides si renseignés
  if (
    formData.value.adresse.code_postal &&
    !isValidPostalCode(formData.value.adresse.code_postal)
  ) {
    return false;
  }

  if (formData.value.adresse.pays && formData.value.adresse.pays.trim().length < 2) {
    return false;
  }

  if (formData.value.adresse.ville && formData.value.adresse.ville.trim().length < 2) {
    return false;
  }

  if (formData.value.adresse.numero && isNaN(formData.value.adresse.numero)) {
    return false;
  }

  if (formData.value.adresse.rue && formData.value.adresse.rue.trim().length < 2) {
    return false;
  }

  return true;
};

const save = async () => {
  submitted.value = true;
  if (!validateForm()) return;

  try {
    let response;

    response = await api.post("fournisseurs/", formData.value);

    successMessage.value = "Fournisseur créé avec succès";

    setTimeout(() => {
        router.push({
            name: "SupplierDetail",
            params: { id: response.id },
        })
    }, 2000);
  } catch (error) {
    console.error("Erreur lors de l’enregistrement du fournisseur:", error);
    errorMessage.value = "Erreur lors de la création du fournisseur";
  }
};
</script>
