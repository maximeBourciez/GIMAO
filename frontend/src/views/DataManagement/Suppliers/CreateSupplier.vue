<template>
  <v-container>
    <FournisseurForm
      title="Créer un fournisseur"
      submit-button-text="Créer le fournisseur"
      @created="handleCreated"
      @close="handleClose"
    />
  </v-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import FournisseurForm from '@/components/Forms/FournisseurForm.vue'

const router = useRouter()

const handleCreated = (newFournisseur) => {
  router.push({
    name: 'SupplierDetail',
    params: { id: newFournisseur.id }
  })
}

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
