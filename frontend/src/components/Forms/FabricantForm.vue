<template>
    <BaseForm v-model="formData" title="Ajouter un fabricant" :validation-schema="validationSchema"
        :handleSubmit="save" :error-message="errorMessage" :success-message="successMessage" :loading="loading"
        submit-button-text="Créer" :custom-cancel-action="true" @cancel="close" elevation="0">
        <template #default>
            <!-- Infos fabricant -->
            <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                Informations du fabricant
            </v-card-subtitle>

            <v-row dense>
                <v-col cols="12" md="6">
                    <FormField v-model="formData.nom" field-name="nom" label="Nom du fabricant"
                        placeholder="Saisir le nom" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormField v-model="formData.email" field-name="email" label="Email" type="email"
                        placeholder="exemple@email.com" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormField v-model="formData.numTelephone" field-name="numTelephone" label="Téléphone"
                        placeholder="06 12 34 56 78" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormCheckbox v-model="formData.serviceApresVente" field-name="serviceApresVente"
                        label="Service après-vente" />
                </v-col>
            </v-row>

            <v-divider class="my-6"></v-divider>

            <!-- Adresse -->
            <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                Adresse
            </v-card-subtitle>

            <v-row dense>
                <v-col cols="12" md="4">
                    <FormField v-model="formData.adresse.numero" field-name="adresse.numero" label="N°"
                        placeholder="123" />
                </v-col>

                <v-col cols="12" md="8">
                    <FormField v-model="formData.adresse.rue" field-name="adresse.rue" label="Rue"
                        placeholder="Rue de la République" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormField v-model="formData.adresse.ville" field-name="adresse.ville" label="Ville"
                        placeholder="Paris" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormField v-model="formData.adresse.code_postal" field-name="adresse.code_postal"
                        label="Code postal" placeholder="75001" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormField v-model="formData.adresse.pays" field-name="adresse.pays" label="Pays"
                        placeholder="France" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormField v-model="formData.adresse.complement" field-name="adresse.complement"
                        label="Complément" placeholder="Bâtiment A, 2ème étage" />
                </v-col>
            </v-row>
        </template>
    </BaseForm>
</template>

<script setup>
import { ref } from 'vue'
import { BaseForm, FormField, FormCheckbox } from '@/components/common'
import { useApi } from '@/composables/useApi'
import { API_BASE_URL } from '@/utils/constants'

const emit = defineEmits(['close', 'created'])

const formData = ref({
    nom: '',
    email: '',
    numTelephone: '',
    serviceApresVente: false,
    adresse: {
        numero: '',
        rue: '',
        ville: '',
        code_postal: '',
        pays: '',
        complement: ''
    }
})

const validationSchema = {
    nom: ['required', { name: 'minLength', params: [2] }],
    email: ['email'],
    numTelephone: ['phone'],
    'adresse.numero': [{ name: 'minLength', params: [1] }],
    'adresse.rue': [{ name: 'minLength', params: [2] }],
    'adresse.ville': [{ name: 'minLength', params: [2] }],
    'adresse.code_postal': [{ name: 'pattern', params: [/^[0-9]{4,6}$/], message: 'Code postal invalide (4-6 chiffres)' }],
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

    try {
        const api = useApi(API_BASE_URL)
        const response = await api.post('fabricants/', formData.value)

        const newFabricant = {
            id: response.id,
            nom: response.nom
        }

        successMessage.value = 'Fabricant créé avec succès'
        emit('created', newFabricant)
        
        setTimeout(() => {
            emit('close')
        }, 1000)
    } catch (error) {
        console.error('Erreur lors de la création du fabricant:', error)
        errorMessage.value = 'Erreur lors de la création du fabricant'
    } finally {
        loading.value = false
    }
}
</script>