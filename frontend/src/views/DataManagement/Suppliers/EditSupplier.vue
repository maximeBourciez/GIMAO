<template>
  <v-container>
    <v-alert v-if="loading" type="info" variant="tonal" class="mb-4">
      <v-progress-circular indeterminate size="20" class="mr-2"></v-progress-circular>
      Chargement des données...
    </v-alert>

    <v-alert v-else-if="errorLoading" type="error" variant="tonal" class="mb-4">
      {{ errorLoading }}
    </v-alert>

    <FournisseurForm
      v-if="!loading && supplierData"
      title="Modifier le fournisseur"
      submit-button-text="Enregistrer les modifications"
      :is-edit="true"
      :initial-data="supplierData"
      :connected-user-id="connectedUserId"
      @updated="handleUpdated"
      @close="handleClose"
    />
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { useApi } from '@/composables/useApi'
import { API_BASE_URL } from '@/utils/constants'
import FournisseurForm from '@/components/Forms/FournisseurForm.vue'

const route = useRoute()
const router = useRouter()
const store = useStore()
const api = useApi(API_BASE_URL)

const supplierId = route.params.id
const supplierData = ref(null)
const loading = ref(false)
const errorLoading = ref('')

const connectedUserId = computed(() => store.getters.currentUser?.id)

const loadSupplierData = async () => {
  isLoading.value = true;
  errorMessage.value = "";
  try {
    supplierData.value = await api.get(`fournisseurs/${supplierId}`);
    originalData.value = JSON.parse(JSON.stringify(supplierData.value));
} catch (error) {
    console.error("Error loading supplier data:", error);
    errorMessage.value = "Erreur lors du chargement des données du fournisseur";
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

  console.log("Detected changes:", changes);

  changes.user = store.getters.currentUser.id;

  console.log("Changes to be sent:", changes);

  if (Object.keys(changes).length === 0) {
    // Aucune modification détectée
    isSaving.value = false;
    console.log("No changes detected, skipping update.");
    return;
  }

  try {
    supplierData.value = await api.get(`fournisseurs/${supplierId}`)
  } catch (error) {
    console.error('Error loading supplier data:', error)
    errorLoading.value = 'Erreur lors du chargement des données du fournisseur'
  } finally {
    loading.value = false
  }
}

const handleUpdated = () => {
  router.push({
    name: 'SupplierDetail',
    params: { id: supplierId }
  })
}

const handleClose = () => {
  router.push({
    name: 'SupplierDetail',
    params: { id: supplierId }
  })
}

onMounted(() => {
  loadSupplierData()
})
</script>
