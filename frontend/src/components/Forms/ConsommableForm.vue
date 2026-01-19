<template>
    <BaseForm
        v-model="formData"
        title="Ajouter un consommable"
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
                    v-model="formData.designation"
                    field-name="designation"
                    label="Désignation"
                    placeholder="Saisir la désignation du consommable"
                />
            </v-col>

            <v-col cols="12">
                <FormSelect
                    v-model="formData.magasin"
                    field-name="magasin"
                    label="Magasin"
                    :items="magasins"
                    item-title="nom"
                    item-value="id"
                    clearable
                >
                    <template #append-item>
                        <v-divider />
                        <v-list-item class="text-primary" @click="showMagasinModal = true">
                            <v-list-item-title>
                                <v-icon left size="18">mdi-plus</v-icon>
                                Ajouter un magasin
                            </v-list-item-title>
                        </v-list-item>
                    </template>
                </FormSelect>
            </v-col>

            <v-col cols="12">
                <FormField
                    v-model="formData.seuilStockFaible"
                    field-name="seuilStockFaible"
                    label="Seuil de stock faible (optionnel)"
                    placeholder="0"
                    type="number"
                />
            </v-col>

            <v-col cols="12">
                <FormFileInput
                    label="Image du consommable (optionnel)"
                    placeholder="Sélectionner une image"
                    accept="image/*"
                    prepend-inner-icon="mdi-camera"
                    @update:model-value="handleFileUpload"
                />
            </v-col>
        </v-row>
    </BaseForm>

    <!-- Modale magasin -->
    <v-dialog v-model="showMagasinModal" max-width="600" scrollable>
        <v-card>
            <v-card-text class="pa-6">
                <MagasinForm @created="onMagasinCreated" @close="showMagasinModal = false" />
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { BaseForm, FormField, FormSelect, FormFileInput } from '@/components/common'
import MagasinForm from '@/components/Forms/MagasinForm.vue'
import { useApi } from '@/composables/useApi'
import { API_BASE_URL } from '@/utils/constants'

const props = defineProps({
    magasins: {
        type: Array,
        default: () => []
    }
})

const emit = defineEmits(['created', 'close', 'magasin-created'])

const formData = ref({
    designation: '',
    magasin: null,
    seuilStockFaible: null,
    lienImageConsommable: null
})

const validationSchema = {
    designation: ['required', { name: 'minLength', params: [2] }, { name: 'maxLength', params: [50] }],
    magasin: ['required'],
    seuilStockFaible: ['numeric', 'positive']
}

const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const showMagasinModal = ref(false)

const close = () => {
    emit('close')
}

const handleFileUpload = (file) => {
    formData.value.lienImageConsommable = file
}

const save = async () => {
    loading.value = true
    errorMessage.value = ''
    successMessage.value = ''

    const api = useApi(API_BASE_URL)

    const formDataToSend = new FormData()
    formDataToSend.append('designation', formData.value.designation)
    formDataToSend.append('magasin', formData.value.magasin)
    
    if (formData.value.seuilStockFaible !== null && formData.value.seuilStockFaible !== '') {
        formDataToSend.append('seuilStockFaible', formData.value.seuilStockFaible)
    }
    
    if (formData.value.lienImageConsommable instanceof File) {
        formDataToSend.append('lienImageConsommable', formData.value.lienImageConsommable)
    }

    try {
        const response = await api.post('consommables/', formDataToSend, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
        
        console.log('Consommable créé avec succès:', response)
        
        const newConsommable = {
            id: response.id,
            designation: response.designation,
            magasin: response.magasin,
            seuilStockFaible: response.seuilStockFaible
        }
        
        successMessage.value = 'Consommable créé avec succès'
        emit('created', newConsommable)
        setTimeout(() => {
            emit('close')
        }, 500)
    } catch (error) {
        console.error('Erreur lors de la création du consommable:', error)
        errorMessage.value = error.message || 'Une erreur est survenue lors de la création du consommable'
    } finally {
        loading.value = false
    }
}

const onMagasinCreated = (newMagasin) => {
    emit('magasin-created', newMagasin)
    props.magasins.push(newMagasin)
    formData.value.magasin = newMagasin.id
}
</script>
