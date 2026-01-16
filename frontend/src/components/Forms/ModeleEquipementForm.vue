<template>
    <BaseForm
        v-model="formData"
        title="Ajouter un modèle d'équipement"
        :validation-schema="validationSchema"
        :loading="loading"
        :error-message="errorMessage"
        :success-message="successMessage"
        :handleSubmit="save"
        :custom-cancel-action="close"
        elevation="0"
    >
        <v-row dense>
                <!-- Nom -->
                <v-col cols="12">
                    <FormField
                        v-model="formData.nom"
                        field-name="nom"
                        label="Nom du modèle"
                        placeholder="Saisir le nom du modèle"
                    />
                </v-col>

                <!-- Fabricant -->
                <v-col cols="12">
                    <FormSelect
                        v-model="formData.fabricant"
                        field-name="fabricant"
                        label="Fabricant"
                        :items="fabricants"
                        item-title="nom"
                        return-object
                        clearable
                    >
                        <template #append-item>
                            <v-divider />
                            <v-list-item class="text-primary" @click="showFabricantModal = true">
                                <v-list-item-title>
                                    <v-icon left size="18">mdi-plus</v-icon>
                                    Ajouter un fabricant
                                </v-list-item-title>
                            </v-list-item>
                        </template>
                    </FormSelect>
                </v-col>
            </v-row>
    </BaseForm>

    <!-- Modale fabricant -->
    <v-dialog v-model="showFabricantModal" max-width="600" scrollable>
        <v-card>
            <v-card-text class="pa-6">
                <FabricantForm @created="onFabricantCreated" @close="showFabricantModal = false" />
            </v-card-text>
        </v-card>
    </v-dialog>
</template>


<script setup>
import { ref } from 'vue'
import { BaseForm, FormField, FormSelect } from '@/components/common'
import FabricantForm from '@/components/Forms/FabricantForm.vue'
import { useApi } from '@/composables/useApi'
import { API_BASE_URL } from '@/utils/constants'

const props = defineProps({
    fabricants: {
        type: Array,
        required: true
    }
})

const emit = defineEmits(['created', 'close', 'fabricant-created'])

const formData = ref({
    nom: '',
    fabricant: null
})

const validationSchema = {
    nom: ['required', { name: 'minLength', params: [2] }],
    fabricant: ['required']
}

const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const showFabricantModal = ref(false)

const close = () => {
    emit('close')
}

const save = async () => {
    loading.value = true
    errorMessage.value = ''
    successMessage.value = ''

    const api = useApi(API_BASE_URL)

    const payload = {
        nom: formData.value.nom,
        fabricant: formData.value.fabricant?.id || formData.value.fabricant
    }

    console.log('payload : ', payload)

    try {
        const response = await api.post('modele-equipements/', payload)
        const modeleCreated = {
            id: response.id,
            nom: formData.value.nom,
            fabricant: formData.value.fabricant?.id || formData.value.fabricant
        }
        console.log('Modele transmis : ', modeleCreated)
        successMessage.value = 'Modèle créé avec succès'
        emit('created', modeleCreated)
        setTimeout(() => {
            emit('close')
        }, 500)
    } catch (error) {
        console.error(error)
        errorMessage.value = error.message || 'Une erreur est survenue lors de la création du modèle'
    } finally {
        loading.value = false
    }
}

const onFabricantCreated = (newFab) => {
    emit('fabricant-created', newFab)
    formData.value.fabricant = newFab
}
</script>
