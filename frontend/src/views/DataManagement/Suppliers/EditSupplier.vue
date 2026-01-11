<template>
    <v-container>


        <v-row v-if="isLoading" justify="center">
            <v-col cols="12" class="text-center">
                <v-progress-circular indeterminate color="primary" size="64" />
            </v-col>
        </v-row>

        <v-row v-else-if="errorMessage">
            <v-col cols="12">
                <v-alert type="error" dismissible @click:close="errorMessage = ''">
                    {{ errorMessage }}
                </v-alert>
            </v-col>
        </v-row>

        <v-row v-else-if="supplierData">
            <v-col cols="12">
                <BaseForm title="Modifier le fournisseur" :loading="isSaving" :error-message="saveErrorMessage"
                    submit-button-text="Enregistrer les modifications" @submit="handleSubmit" @cancel="goBack"
                    @clear-error="saveErrorMessage = ''" actions-container-class="d-flex justify-end gap-2 mt-2">
                    <template #default>
                        <!-- Infos fournisseur -->
                        <v-sheet class="pa-4 mb-4" elevation="1" rounded>
                            <h4 class="mb-3">Fournisseur</h4>
                            <v-row dense>
                                <v-col cols="12" md="6">
                                    <v-text-field v-model="supplierData.nom" label="Nom du fournisseur *" outlined dense
                                        :rules="[v => !!v && !!v.trim() || 'Le nom du fournisseur est requis']" />
                                </v-col>
                                <v-col cols="12" md="6">
                                    <v-text-field v-model="supplierData.email" label="Email *" outlined dense
                                        :rules="[v => !v || isValidEmail(v) || 'Email invalide']" />
                                </v-col>
                            </v-row>
                            <v-row dense>
                                <v-col cols="6">
                                    <v-text-field v-model="supplierData.numTelephone" label="Téléphone *" outlined dense
                                        :rules="[v => !v || isValidPhone(v) || 'Téléphone invalide']" />
                                </v-col>
                                <v-col cols="6" class="d-flex align-center">
                                    <v-checkbox v-model="supplierData.serviceApresVente" label="Service après-vente"
                                        dense />
                                </v-col>
                            </v-row>
                        </v-sheet>

                        <!-- Adresse -->
                        <v-sheet class="pa-4" elevation="1" rounded>
                            <h4 class="mb-3">Adresse</h4>
                            <v-row dense>
                                <v-col cols="4">
                                    <v-text-field v-model="supplierData.adresse.numero" label="N° *" outlined dense />
                                </v-col>
                                <v-col cols="8">
                                    <v-text-field v-model="supplierData.adresse.rue" label="Rue *" outlined dense
                                        :rules="[v => !v || v.trim().length >= 2 || 'La rue doit contenir au moins 2 caractères']" />
                                </v-col>
                            </v-row>
                            <v-row dense>
                                <v-col cols="6">
                                    <v-text-field v-model="supplierData.adresse.code_postal" label="Code postal *"
                                        outlined dense
                                        :rules="[v => !v || isValidPostalCode(v) || 'Code postal invalide']" />
                                </v-col>
                                <v-col cols="6">
                                    <v-text-field v-model="supplierData.adresse.ville" label="Ville *" outlined dense
                                        :rules="[v => !v || v.trim().length >= 2 || 'La ville doit contenir au moins 2 caractères']" />
                                </v-col>

                            </v-row>
                            <v-row dense>
                                <v-col cols="12">
                                    <v-text-field v-model="supplierData.adresse.pays" label="Pays *" outlined dense
                                        :rules="[v => !v || v.trim().length >= 2 || 'Le pays doit contenir au moins 2 caractères']" />
                                </v-col>
                            </v-row>
                            <v-row dense>
                                <v-col cols="12">
                                    <v-text-field v-model="supplierData.adresse.complement" label="Complément" outlined
                                        dense />
                                </v-col>
                            </v-row>
                        </v-sheet>
                    </template>
                </BaseForm>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';
import BaseForm from '@/components/common/BaseForm.vue';

const route = useRoute();
const router = useRouter();
const api = useApi(API_BASE_URL);

const supplierId = route.params.id;
const supplierData = ref(null);
const isLoading = ref(true);
const isSaving = ref(false);
const errorMessage = ref('');
const saveErrorMessage = ref('');

onMounted(async () => {
    await loadSupplierData();
});

const loadSupplierData = async () => {
    isLoading.value = true;
    errorMessage.value = '';
    try {
        supplierData.value = await api.get(`fournisseurs/${supplierId}`);
    } catch (error) {
        console.error('Error loading supplier data:', error);
        errorMessage.value = 'Erreur lors du chargement des données du fournisseur';
        loader.value = false;
    } finally {
        isLoading.value = false;
    }
};

// Fonctions de validation
const isValidEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

const isValidPhone = (phone) => {
    return /^\+?[0-9\s\-()]{7,15}$/.test(phone);
};

const isValidPostalCode = (code) => {
    return /^[0-9]{4,6}$/.test(code.replace(/\s/g, ''));
};

const handleSubmit = async () => {
    isSaving.value = true;
    saveErrorMessage.value = '';

    console.log('Submitting supplier data:', supplierData.value);

    try {
        await api.put(`fournisseurs/${supplierId}/`, supplierData.value);

        // Rediriger vers la page de détail après la modification
        router.push({
            name: 'SupplierDetail',
            params: { id: supplierId }
        });
    } catch (error) {
        console.error('Error updating supplier:', error);
        saveErrorMessage.value = 'Erreur lors de la modification du fournisseur';
    } finally {
        isSaving.value = false;
    }
};

const goBack = () => {
    router.back();
};
</script>