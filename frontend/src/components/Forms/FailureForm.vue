<template>
    <BaseForm
        v-model="formData"
        :title="title"
        :validation-schema="validationSchema"
        :loading="loading"
        :error-message="errorMessage"
        :success-message="successMessage"
        :handleSubmit="save"
        :custom-cancel-action="close"
        :submit-button-text="submitButtonText"
        elevation="0"
    >
        <v-row dense>
            <v-col cols="12">
                <FormField
                    v-model="formData.nom"
                    field-name="nom"
                    label="Nom de la demande d'intervention"
                    placeholder="Saisir le nom de la demande"
                />
            </v-col>

            <v-col cols="12" v-if="!isEdit">
                <FormSelect
                    v-model="formData.equipement_id"
                    field-name="equipement_id"
                    label="Équipement"
                    :items="equipments"
                    item-title="designation"
                    item-value="id"
                    placeholder="Sélectionner un équipement"
                />
            </v-col>

            <v-col cols="12">
                <FormTextarea
                    v-model="formData.commentaire"
                    field-name="commentaire"
                    label="Commentaires"
                    placeholder="Ajouter des détails ou une description..."
                    rows="5"
                    counter="300"
                />
            </v-col>

            <!-- Documents (uniquement en création) -->
            <v-col cols="12" v-if="!isEdit">
                <v-divider class="my-4"></v-divider>
                <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                    Documents (optionnels)
                </v-card-subtitle>

                <DocumentForm v-model="formData.documents" :type-documents="typesDocuments" />
            </v-col>
        </v-row>
    </BaseForm>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { BaseForm, FormField, FormSelect, FormTextarea } from '@/components/common'
import DocumentForm from '@/components/Forms/DocumentForm.vue'
import { useApi } from '@/composables/useApi'
import { API_BASE_URL } from '@/utils/constants'

const props = defineProps({
    title: {
        type: String,
        default: 'Ajouter une demande d\'intervention'
    },
    submitButtonText: {
        type: String,
        default: 'Créer'
    },
    isEdit: {
        type: Boolean,
        default: false
    },
    initialData: {
        type: Object,
        default: () => ({})
    },
    equipments: {
        type: Array,
        default: () => []
    },
    typesDocuments: {
        type: Array,
        default: () => []
    },
    connectedUserId: {
        type: Number,
        default: null
    }
})

const emit = defineEmits(['created', 'updated', 'close'])

const formData = ref({
    nom: '',
    equipement_id: null,
    commentaire: '',
    documents: []
})

const validationSchema = computed(() => {
    const schema = {
        nom: ['required', { name: 'minLength', params: [2] }, { name: 'maxLength', params: [255] }],
    }

    if (!props.isEdit) {
        schema.equipement_id = ['required']
    }

    return schema
})

const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Initialiser les données
watch(() => props.initialData, (newData) => {
    if (newData && Object.keys(newData).length > 0) {
        formData.value = {
            nom: newData.nom || '',
            equipement_id: newData.equipement_id || null,
            commentaire: newData.commentaire || '',
            documents: newData.documents || []
        }
    }
}, { immediate: true, deep: true })

const close = () => {
    emit('close')
}

const save = async () => {
    loading.value = true
    errorMessage.value = ''
    successMessage.value = ''

    const api = useApi(API_BASE_URL)

    try {
        if (props.isEdit) {
            // Mode édition
            const payload = {
                nom: formData.value.nom,
                commentaire: formData.value.commentaire || ''
            }

            const response = await api.patch(`demandes-intervention/${props.initialData.id}/`, payload)
            console.log('Demande d\'intervention modifiée avec succès:', response)

            successMessage.value = 'Demande d\'intervention modifiée avec succès'
            emit('updated', response)
        } else {
            // Mode création
            if (!props.connectedUserId) {
                errorMessage.value = "Erreur: Utilisateur non connecté"
                loading.value = false
                return
            }

            // Utilisation de FormData pour envoyer les fichiers
            const formDataToSend = new FormData()
            formDataToSend.append('nom', formData.value.nom)
            formDataToSend.append('commentaire', formData.value.commentaire || '')
            formDataToSend.append('equipement_id', formData.value.equipement_id)
            formDataToSend.append('utilisateur_id', props.connectedUserId)

            // Préparation des documents (métadonnées en JSON, fichiers séparés)
            const validDocs = formData.value.documents
                .filter(doc => {
                    const hasFile = doc.cheminAcces || doc.file
                    const hasType = doc.typeDocument_id
                    const hasName = doc.nomDocument
                    return hasFile && hasType && hasName
                })

            if (validDocs.length > 0) {
                const docMetadata = validDocs.map((doc, index) => ({
                    nomDocument: doc.nomDocument,
                    typeDocument_id: doc.typeDocument_id
                }))
                formDataToSend.append('documents', JSON.stringify(docMetadata))

                // Ajouter chaque fichier avec la convention document_{index}
                validDocs.forEach((doc, index) => {
                    const file = doc.cheminAcces?.[0] || doc.cheminAcces || doc.file?.[0] || doc.file
                    if (file) {
                        formDataToSend.append(`document_${index}`, file)
                    }
                })
            }

            const response = await api.post('demandes-intervention/', formDataToSend, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            console.log('Demande d\'intervention créée avec succès:', response)

            successMessage.value = 'Demande d\'intervention créée avec succès'
            emit('created', response)
        }

        setTimeout(() => {
            emit('close')
        }, 1500)
    } catch (error) {
        console.error('Erreur lors de l\'enregistrement:', error)
        errorMessage.value = error.message || 'Une erreur est survenue lors de l\'enregistrement de la demande d\'intervention'
    } finally {
        loading.value = false
    }
}
</script>
