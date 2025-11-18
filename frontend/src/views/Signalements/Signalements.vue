<template>
  <BaseForm v-model="formData" title="Signaler une défaillance" :loading="loading" :error-message="errorMessage"
    :success-message="successMessage" :fields="formFields" submit-text="Valider" cancel-text="Annuler"
    @submit="handleSubmit" @cancel="handleCancel">
    <template #additional-fields>
      <v-col cols="12" md="6">
        <v-textarea v-model="formData.commentaire" label="Commentaires" rows="10" outlined dense></v-textarea>
      </v-col>
    </template>
  </BaseForm>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import BaseForm from '@/components/common/BaseForm.vue';

const router = useRouter();

const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const formData = ref({
  lieu: null,
  salle: null,
  equipement: null,
  commentaire: ''
});

const lieux = ref(["Lieu 1", "Lieu 2", "Lieu 3"]);
const salles = ref(["Salle 1", "Salle 2", "Salle 3"]);
const equipements = ref(["Equipement 1", "Equipement 2", "Equipement 3"]);

const formFields = computed(() => [
  {
    name: 'lieu',
    label: 'Lieu',
    type: 'select',
    items: lieux.value,
    required: true,
    cols: 12,
    md: 6
  },
  {
    name: 'salle',
    label: 'Salle',
    type: 'select',
    items: salles.value,
    required: true,
    cols: 12,
    md: 6
  },
  {
    name: 'equipement',
    label: 'Équipement',
    type: 'select',
    items: equipements.value,
    required: true,
    cols: 12,
    md: 6
  }
]);

const handleSubmit = async () => {
  loading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    // TODO: Remplacer par l'appel API réel
    // await api.post('signalements/', formData.value);

    // Simulation de succès
    await new Promise(resolve => setTimeout(resolve, 500));

    successMessage.value = 'Défaillance signalée avec succès !';

    // Réinitialiser le formulaire après succès
    setTimeout(() => {
      formData.value = {
        lieu: null,
        salle: null,
        equipement: null,
        commentaire: ''
      };
      successMessage.value = '';
    }, 2000);

  } catch (error) {
    console.error('Erreur lors du signalement:', error);
    errorMessage.value = 'Une erreur est survenue lors du signalement de la défaillance.';
  } finally {
    loading.value = false;
  }
};

const handleCancel = () => {
  formData.value = {
    lieu: null,
    salle: null,
    equipement: null,
    commentaire: ''
  };
  errorMessage.value = '';
  successMessage.value = '';
};
</script>
