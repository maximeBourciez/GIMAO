<template>
  <v-container>
    <FabricantForm
      title="Créer un fabricant"
      submit-button-text="Créer le fabricant"
      @created="handleCreated"
      @close="handleClose"
    />
  </v-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import FabricantForm from '@/components/Forms/FabricantForm.vue'

const router = useRouter()

const handleCreated = (newFabricant) => {
  router.push({
    name: 'ManufacturerDetail',
    params: { id: newFabricant.id }
  })
}


const adresse = ref({});

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
  // Fabricant - nom obligatoire
  if (!fabricant.value.nom.trim()) {
    console.log("Nom invalide");
    return false;
  }

  // Email optionnel mais doit être valide si renseigné
  if (fabricant.value.email && !isValidEmail(fabricant.value.email)) {
    console.log("Email invalide");
    return false;
  }

  // Téléphone optionnel mais doit être valide si renseigné
  if (fabricant.value.numTelephone && !isValidPhone(fabricant.value.numTelephone)) {
    console.log("Téléphone invalide");
    return false;
  }

  // Adresse - tous les champs sont optionnels mais doivent être valides si renseignés
  if (adresse.value.code_postal && !isValidPostalCode(adresse.value.code_postal)) {
    console.log("Code postal invalide");
    return false;
  }

  if (adresse.value.pays && adresse.value.pays.trim().length < 2) {
    console.log("Pays invalide");
    return false;
  }

  if (adresse.value.ville && adresse.value.ville.trim().length < 2) {
    console.log("Ville invalide");
    return false;
  }

  if (!adresse.value.numero || !adresse.value.numero.trim()) {
    console.log("Numéro de rue requis");
    return false;
  }

  if (adresse.value.rue && adresse.value.rue.trim().length < 2) {
    console.log("Rue invalide");
    return false;
  }

  return true;
};

const save = async () => {
  submitted.value = true;
  if (!validateForm()) return;

  const payload = {
    ...fabricant.value,
    adresse: adresse.value,
  };

  try {
    let response;

    response = await api.post("fabricants/", payload);

    router.push({
      name: "ManufacturerDetail",
      params: { id: response.id },
    });
  } catch (error) {
    console.error("Erreur lors de l’enregistrement du fabricant:", error);
  }
};
</script>
