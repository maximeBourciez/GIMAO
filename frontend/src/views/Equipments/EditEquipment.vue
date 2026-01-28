<template>
  <v-app>
    <v-main>
      <v-container>
        <BaseForm v-model="formData" :title="`Modifier l'Équipement #${equipmentId}`" :loading="loading"
          :error-message="errorMessage" :success-message="successMessage"
          :loading-message="loadingData ? 'Chargement des données...' : ''" :custom-validation="validateForm"
          submit-button-text="Enregistrer les modifications" :handleSubmit="handleSubmit">
          <template #default>
            <EquipmentFormFields v-model="formData" :equipment-models="equipmentModels" :fournisseurs="fournisseurs"
              :fabricants="fabricants" :familles="familles" :locations="locations" :consumables="consumables"
              :equipment-statuses="equipmentStatuses" :show-counters="false" @file-upload="handleFileUpload"
              @location-created="handleLocationCreated" />
          </template>
        </BaseForm>
      </v-container>
    </v-main>

    <v-dialog v-model="showFabricantDialog" max-width="80%">
      <FabricantForm @created="handleFabricantCreated" @close="showFabricantDialog = false" />
    </v-dialog>

    <v-dialog v-model="showFournisseurDialog" max-width="80%">
      <FournisseurForm @created="handleFournisseurCreated" @close="showFournisseurDialog = false" />
    </v-dialog>

    <v-dialog v-model="showModeleDialog" max-width="80%">
      <ModeleEquipementForm :fabricants="fabricants" @created="handleModeleCreated" @close="showModeleDialog = false"
        @fabricant-created="handleFabricantCreated" />
    </v-dialog>

    <v-dialog v-model="showFamilleDialog" max-width="50%">
      <FamilleEquipementForm :families="familles" @created="handleFamilleCreated" @close="showFamilleDialog = false" />
    </v-dialog>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { BaseForm } from '@/components/common';
import { useEquipmentForm } from '@/composables/useEquipmentForm';
import EquipmentFormFields from '@/components/Forms/EquipmentFormFields.vue';
import FabricantForm from '@/components/Forms/FabricantForm.vue';
import FournisseurForm from '@/components/Forms/FournisseurForm.vue';
import ModeleEquipementForm from '@/components/Forms/ModeleEquipementForm.vue';
import FamilleEquipementForm from '@/components/Forms/FamilleEquipementForm.vue';

const route = useRoute();

const {
  formData,
  initialData,
  loading,
  loadingData,
  errorMessage,
  successMessage,
  locations,
  equipmentModels,
  fournisseurs,
  fabricants,
  consumables,
  familles,
  equipmentStatuses,
  showFabricantDialog,
  showFournisseurDialog,
  showModeleDialog,
  showFamilleDialog,
  validateForm,
  handleFileUpload,
  fetchData,
  fetchEquipment,
  detectChanges,
  handleFabricantCreated,
  handleFournisseurCreated,
  handleModeleCreated,
  handleFamilleCreated,
  handleLocationCreated,
  api,
  router
} = useEquipmentForm(true);


const equipmentId = computed(() => route.params.id || null);


const handleSubmit = async () => {
  if (!validateForm()) return;

  // Détecter les changements
  const { hasChanges, changes } = detectChanges();

  if (!hasChanges) {
    errorMessage.value = 'Aucune modification détectée';
    return;
  }

  loading.value = true;
  errorMessage.value = '';
  try {
    const fd = new FormData();

    if (formData.value.lienImageEquipement instanceof File) {
      fd.append('lienImageEquipement', formData.value.lienImageEquipement);
      delete equipementData.lienImageEquipement;
    }

    fd.append('changes', JSON.stringify(changes));

    await api.put(`equipements/${equipmentId.value}/`, fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });

    successMessage.value = 'Équipement modifié avec succès';
    setTimeout(() => router.back(), 1500);

  } catch (e) {
    console.error('Erreur lors de la modification:', e);
    errorMessage.value = 'Erreur lors de la modification de l\'équipement';

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

onMounted(async () => {
  try {
    await fetchData();
    await fetchEquipment(equipmentId.value);
    // Pas besoin de fetchDocs car pas de compteurs en mode édition
  } catch (error) {
    console.error('Erreur dans onMounted:', error);
    errorMessage.value = error.message || 'Erreur lors du chargement';
  }
});


</script>
