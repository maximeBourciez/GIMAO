<template>
    <BaseForm
        v-model="formData"
        title="Ajouter un fournisseur"
        :validation-schema="validationSchema"
        :loading="loading"
        :error-message="errorMessage"
        :success-message="successMessage"
        :handleSubmit="save"
        :custom-cancel-action="close"
        elevation="0"
    >
        <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
            Informations du fournisseur
        </v-card-subtitle>

        <v-row dense>
            <v-col cols="12" md="6">
                <FormField
                    v-model="formData.nom"
                    field-name="nom"
                    label="Nom du fournisseur"
                />
            </v-col>
            <v-col cols="12" md="6">
                <FormField
                    v-model="formData.email"
                    field-name="email"
                    label="Email"
                    type="email"
                />
            </v-col>
        </v-row>

        <v-row dense>
            <v-col cols="6">
                <FormField
                    v-model="formData.numTelephone"
                    field-name="numTelephone"
                    label="Téléphone"
                />
            </v-col>
            <v-col cols="6" class="d-flex align-center">
                <FormCheckbox
                    v-model="formData.serviceApresVente"
                    field-name="serviceApresVente"
                    label="Service après-vente"
                />
            </v-col>
        </v-row>

        <v-divider class="my-6"></v-divider>

        <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
            Adresse
        </v-card-subtitle>

        <v-row dense>
            <v-col cols="4">
                <FormField
                    v-model="formData.adresse.numero"
                    field-name="adresse.numero"
                    label="N°"
                />
            </v-col>
            <v-col cols="8">
                <FormField
                    v-model="formData.adresse.rue"
                    field-name="adresse.rue"
                    label="Rue"
                />
            </v-col>
        </v-row>

        <v-row dense>
            <v-col cols="6">
                <FormField
                    v-model="formData.adresse.ville"
                    field-name="adresse.ville"
                    label="Ville"
                />
            </v-col>
            <v-col cols="6">
                <FormField
                    v-model="formData.adresse.code_postal"
                    field-name="adresse.code_postal"
                    label="Code postal"
                />
            </v-col>
        </v-row>

        <v-row dense>
            <v-col cols="12">
                <FormField
                    v-model="formData.adresse.pays"
                    field-name="adresse.pays"
                    label="Pays"
                />
            </v-col>
        </v-row>

        <v-row dense>
            <v-col cols="12">
                <FormField
                    v-model="formData.adresse.complement"
                    field-name="adresse.complement"
                    label="Complément"
                />
            </v-col>
        </v-row>
    </BaseForm>
</template>

<script setup>
import { ref } from 'vue'
import { BaseForm, FormField, FormCheckbox } from '@/components/common'
import { useApi } from '@/composables/useApi'
import { API_BASE_URL } from '@/utils/constants'

const emit = defineEmits(['created', 'close'])

const formData = ref({
    nom: '',
    email: null,
    numTelephone: null,
    serviceApresVente: false,
    adresse: {
        numero: '',
        rue: '',
        ville: '',
        code_postal: '',
        pays: '',
        complement: null
    }
})

const validationSchema = {
    nom: ['required', { name: 'minLength', params: [2] }],
    email: ['email'],
    numTelephone: ['phone'],
    'adresse.numero': [{ name: 'minLength', params: [1] }],
    'adresse.rue': [{ name: 'minLength', params: [2] }],
    'adresse.ville': [{ name: 'minLength', params: [2] }],
    'adresse.code_postal': [{ name: 'pattern', params: [/^[0-9]{4,6}$/], message: 'Le code postal doit contenir entre 4 et 6 chiffres' }],
    'adresse.pays': [{ name: 'minLength', params: [2] }]
}

const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const close = () => {
    emit('close')
}

const save = async () => {
    loading.value = true
    errorMessage.value = ''
    successMessage.value = ''

    const api = useApi(API_BASE_URL)
    
    try {
        const response = await api.post('fournisseurs/', formData.value)
        console.log('Fournisseur créé avec succès:', response)
        const newFournisseur = {
            id: response.id,
            nom: response.nom
        }
        successMessage.value = 'Fournisseur créé avec succès'
        emit('created', newFournisseur)
        setTimeout(() => {
            emit('close')
        }, 500)
    } catch (error) {
        console.error('Erreur lors de la création du fournisseur:', error)
        errorMessage.value = error.message || 'Une erreur est survenue lors de la création du fournisseur'
    } finally {
        loading.value = false
    }
}
</script>
