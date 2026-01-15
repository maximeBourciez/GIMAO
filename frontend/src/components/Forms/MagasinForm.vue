<template>
    <BaseForm
        v-model="formData"
        title="Ajouter un magasin"
        :validation-schema="validationSchema"
        :loading="loading"
        :error-message="errorMessage"
        :success-message="successMessage"
        :handleSubmit="save"
        :custom-cancel-action="close"
        elevation="0"
    >
        <v-row dense>
            <v-col cols="12">
                <FormField
                    v-model="formData.nom"
                    field-name="nom"
                    label="Nom du magasin"
                    placeholder="Saisir le nom du magasin"
                />
            </v-col>

            <v-col cols="12">
                <FormCheckbox
                    v-model="formData.estMobile"
                    field-name="estMobile"
                    label="Magasin mobile"
                />
            </v-col>

            <v-divider class="my-4"></v-divider>

            <v-col cols="12">
                <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                    Adresse (optionnelle)
                </v-card-subtitle>
            </v-col>

            <v-col cols="4">
                <FormField
                    v-model="formData.adresse.numero"
                    field-name="adresse.numero"
                    label="N°"
                    placeholder="123"
                />
            </v-col>
            <v-col cols="8">
                <FormField
                    v-model="formData.adresse.rue"
                    field-name="adresse.rue"
                    label="Rue"
                    placeholder="Rue de la République"
                />
            </v-col>

            <v-col cols="6">
                <FormField
                    v-model="formData.adresse.ville"
                    field-name="adresse.ville"
                    label="Ville"
                    placeholder="Paris"
                />
            </v-col>
            <v-col cols="6">
                <FormField
                    v-model="formData.adresse.code_postal"
                    field-name="adresse.code_postal"
                    label="Code postal"
                    placeholder="75000"
                />
            </v-col>

            <v-col cols="12">
                <FormField
                    v-model="formData.adresse.pays"
                    field-name="adresse.pays"
                    label="Pays"
                    placeholder="France"
                />
            </v-col>

            <v-col cols="12">
                <FormField
                    v-model="formData.adresse.complement"
                    field-name="adresse.complement"
                    label="Complément"
                    placeholder="Bâtiment A, Etage 3"
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
    estMobile: false,
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
    nom: ['required', { name: 'minLength', params: [2] }, { name: 'maxLength', params: [100] }],
    estMobile: [],
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
        const response = await api.post('magasins/', formData.value)
        console.log('Magasin créé avec succès:', response)
        
        const newMagasin = {
            id: response.id,
            nom: response.nom,
            estMobile: response.estMobile
        }
        
        successMessage.value = 'Magasin créé avec succès'
        emit('created', newMagasin)
        setTimeout(() => {
            emit('close')
        }, 500)
    } catch (error) {
        console.error('Erreur lors de la création du magasin:', error)
        errorMessage.value = error.message || 'Une erreur est survenue lors de la création du magasin'
    } finally {
        loading.value = false
    }
}
</script>
