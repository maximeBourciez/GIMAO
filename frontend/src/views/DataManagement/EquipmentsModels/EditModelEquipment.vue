<template>
    <BaseForm v-model="modelEquipment" :loading="isLoading" :error-message="errorMessage"
        :success-message="successMessage" title="Modifier le modèle d'équipement" @submit="updateModelEquipment"
        @clear-error="errorMessage = ''" @clear-success="successMessage = ''">
        <template #default="{ formData }">
            <v-row v-if="formData">
                <v-col cols="12">
                    <v-text-field v-model="formData.nom" label="Nom du modèle" :rules="[rules.required]" required />
                </v-col>

                <v-col cols="12">
                    <v-select v-model="formData.fabricant" :items="fabricants" item-title="nom" item-value="id"
                        label="Fabricant" :rules="[rules.required]" return-object required />
                </v-col>
            </v-row>
        </template>
    </BaseForm>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useApi } from '@/composables/useApi';
import { useStore } from 'vuex';
import { API_BASE_URL } from '@/utils/constants';
import BaseForm from '@/components/common/BaseForm.vue';

// Données
const modelEquipment = ref({
    nom: '',
    fabricant: null
});
const originalData = ref(null);
const fabricants = ref([]);

const isLoading = ref(true);
const errorMessage = ref('');
const successMessage = ref('');

const route = useRoute();
const router = useRouter();
const store = useStore();
const api = useApi(API_BASE_URL);

// Règles de validation
const rules = {
    required: (value) => !!value || 'Ce champ est requis'
};

// Charger les données du modèle d'équipement
const loadModelEquipmentData = async () => {
    isLoading.value = true;
    errorMessage.value = '';

    try {
        const response = await api.get(`modele-equipements/${route.params.id}/`);
        console.log('Données chargées:', response);
        modelEquipment.value = response || {};
        originalData.value = JSON.parse(JSON.stringify(modelEquipment.value));
    } catch (error) {
        console.error('Error loading model equipment:', error);
        errorMessage.value = 'Erreur lors du chargement des données';
        modelEquipment.value = {};
    } finally {
        isLoading.value = false;
    }
};

// Mettre à jour le modèle d'équipement
const updateModelEquipment = async (values) => {
    isLoading.value = true;
    errorMessage.value = '';
    successMessage.value = '';

    const changes = detectChanges();
    console.log('Changements détectés:', changes);

    if (Object.keys(changes).length === 0) {
        errorMessage.value = 'Aucun changement détecté.';
        isLoading.value = false;
        return;
    }

    changes.user = store.getters.currentUser.id;

    try {
        const response = await api.put(`modele-equipements/${route.params.id}/`, changes);
        console.log('Modèle mis à jour:', response);
        successMessage.value = 'Modèle d\'équipement mis à jour avec succès';

        setTimeout(() => {
            router.push({
                name: "ModelEquipmentDetail",
                params: { id: response.id}
            })
        }, 2000);
    } catch (error) {
        console.error('Error updating model equipment:', error);
        errorMessage.value = 'Erreur lors de la mise à jour du modèle d\'équipement';
    } finally {
        isLoading.value = false;
    }
};

// Charger les fabricants pour le select
const loadFabricants = async () => {
    try {
        const response = await api.get('fabricants/');
        fabricants.value = response || [];
    } catch (error) {
        console.error('Error loading fabricants:', error);
        errorMessage.value = 'Erreur lors du chargement des fabricants';
    }
};

onMounted(() => {
    loadModelEquipmentData();
    loadFabricants();
});

const detectChanges = () => {
    const changes = {};

    // Vérifier le nom
    if (modelEquipment.value.nom !== originalData.value.nom) {
        changes.nom = {
            "ancienne": originalData.value.nom,
            "nouvelle": modelEquipment.value.nom
        }
    }

    // Vérifier le fabricant
    const currentFabricantId = modelEquipment.value.fabricant?.id;
    const originalFabricantId = originalData.value.fabricant?.id;

    if (currentFabricantId !== originalFabricantId) {
        changes.fabricant = {
            "ancienne": originalFabricantId,
            "nouvelle": currentFabricantId
        }
    }

    console.log('Changes detected in detectChanges function:', changes);
    return changes;
};
</script>