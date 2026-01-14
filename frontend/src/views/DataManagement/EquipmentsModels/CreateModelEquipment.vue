<template>
  <BaseForm
    title="Créer un modèle d'équipement"
    :model-value="model"
    :loading="false"
    :error-message="errorMessage"
    :success-message="successMessage"
    submit-button-text="Créer le modèle"
    @submit="saveModelEquipment"
    @clear-error=""
    @clear-success=""
  >
    <template #default="{ formData }">
      <v-row v-if="formData">
        <v-col cols="12">
          <v-text-field
            v-model="formData.nom"
            label="Nom du modèle"
            :rules="[(value) => !!value || 'Ce champ est requis']"
            required
          />
        </v-col>
        <v-col cols="12">
          <v-select
            v-model="formData.fabricant"
            :items="fabricants"
            item-title="nom"
            item-value="id"
            label="Fabricant"
            :rules="[(value) => !!value || 'Ce champ est requis']"
            return-object
            required
          />
        </v-col>
      </v-row>
    </template>
  </BaseForm>
</template>

<script setup>
import { useApi } from "@/composables/useApi";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { API_BASE_URL } from "@/utils/constants";
import BaseForm from "@/components/common/BaseForm.vue";

// Données
const model = ref({});
const fabricants = ref([]);
const api = useApi(API_BASE_URL);
const router = useRouter();
const successMessage = ref("");
const errorMessage = ref("");

const loadFabricants = async () => {
  try {
    fabricants.value = await api.get("fabricants/");
  } catch (error) {
    console.error("Error loading manufacturers:", error);
    errorMessage.value = "Erreur lors du chargement des fabricants.";
  }
};

onMounted(() => {
  loadFabricants();
});

const saveModelEquipment = async (formData) => {
  try {
    const response = await api.post(`modele-equipements/`, formData);
    console.log("Model equipment updated:", response);

    successMessage.value = "Modèle d'équipement créé avec succès.";

    setTimeout(() => {
      router.push({
        name: "ModelEquipmentDetail",
        params: { id: response.id },
      });
    }, 2000);
  } catch (error) {
    console.error("Error creating model equipment:", error);
    errorMessage.value = "Erreur lors de la création du modèle d'équipement.";
  }
};
</script>
