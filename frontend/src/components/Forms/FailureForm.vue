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

            <v-col cols="12">
                <FormSelect
                    v-model="formData.equipement_id"
                    field-name="equipement_id"
                    label="Équipement"
                    :items="equipments"
                    item-title="designation"
                    item-value="id"
                    placeholder="Sélectionner un équipement"
                    :disabled="isEdit"
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

            <!-- Documents -->
            <v-col cols="12">
                <v-divider class="my-4"></v-divider>
                <div class="pb-2" style="font-size: 20px;">
                    Documents (optionnels)
                </div>

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
const originalFormData = ref(null)

// Initialiser les données
watch(() => props.initialData, (newData) => {
    if (newData && Object.keys(newData).length > 0) {
        formData.value = {
            nom: newData.nom || '',
            equipement_id: newData.equipement_id || null,
            commentaire: newData.commentaire || '',
            documents: newData.documents || []
        }
        // Sauvegarder l'état original pour comparaison
        if (props.isEdit) {
            originalFormData.value = JSON.parse(JSON.stringify(formData.value))
        }
    }
}, { immediate: true, deep: true })

const close = () => {
    emit('close')
}

// Fonction pour créer de nouveaux documents et les lier à la DI
const createAndLinkDocuments = async (demandeId, documents, originalDocuments = []) => {
    const docs = Array.isArray(documents) ? documents : []
    const errors = []
    const api = useApi(API_BASE_URL)

    for (const doc of docs) {
        if (!doc) continue
        
        // Ignorer les lignes vides
        if (!doc.file && !doc.typeDocument_id && !(doc.nomDocument || '').trim()) continue
        
        // Gérer les documents existants (mise à jour seulement si modifié)
        if (doc.document_id) {
            // Trouver le document original
            const original = originalDocuments.find(o => o.document_id === doc.document_id)
            
            // Vérifier si au moins un champ a changé
            const hasChanges = 
                (original && doc.nomDocument !== original.nomDocument) ||
                (original && doc.typeDocument_id !== original.typeDocument_id) ||
                doc.file // Nouveau fichier = toujours un changement
            
            if (!hasChanges) {
                // Aucun changement, on passe au suivant
                continue
            }
            
            try {
                // Toujours utiliser FormData pour la compatibilité avec le backend
                const form = new FormData()
                form.append('nomDocument', doc.nomDocument || '')
                form.append('typeDocument_id', String(doc.typeDocument_id))
                if (doc.file) {
                    form.append('cheminAcces', doc.file)
                }
                await api.patch(`documents/${doc.document_id}/`, form)
            } catch (e) {
                console.error('Erreur lors de la mise à jour du document:', e)
                errors.push(doc.nomDocument || 'Document existant')
            }
            continue
        }
        
        // Vérifier les champs requis pour les nouveaux documents
        if (!doc.file || !doc.typeDocument_id) {
            errors.push(doc.nomDocument || 'Document')
            continue
        }

        try {
            const form = new FormData()
            form.append('nomDocument', (doc.nomDocument || doc.file.name || '').toString())
            form.append('typeDocument_id', String(doc.typeDocument_id))
            form.append('cheminAcces', doc.file)

            const created = await api.post('documents/', form)
            const newId = Number(created?.id)
            if (!Number.isInteger(newId) || newId <= 0) {
                errors.push(doc.nomDocument || doc.file?.name || 'Document')
                continue
            }

            try {
                await api.post(`demandes-intervention/${demandeId}/ajouter_document/`, {
                    document_id: newId
                })
            } catch (e) {
                try {
                    await api.remove(`documents/${newId}/`)
                } catch (_) {}
                errors.push(doc.nomDocument || doc.file?.name || 'Document')
            }
        } catch (e) {
            errors.push(doc.nomDocument || doc.file?.name || 'Document')
        }
    }

    return errors
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
            console.log('Documents à traiter:', formData.value.documents)

            // Gestion des documents (création + liaison + mise à jour)
            const createErrors = await createAndLinkDocuments(
                props.initialData.id, 
                formData.value.documents,
                props.initialData.documents || [] // Documents originaux pour comparaison
            )
            console.log('Erreurs création documents:', createErrors)
            
            if (createErrors.length) {
                errorMessage.value = `Certains documents n'ont pas pu être traités: ${createErrors.join(', ')}`
                loading.value = false
                return
            }

            successMessage.value = 'Demande d\'intervention modifiée avec succès'
            emit('updated', response)
        } else {
            // Mode création
            if (!props.connectedUserId) {
                errorMessage.value = "Erreur: Utilisateur non connecté"
                loading.value = false
                return
            }

            // Création de la DI
            const payload = {
                nom: formData.value.nom,
                commentaire: formData.value.commentaire || '',
                equipement_id: formData.value.equipement_id,
                utilisateur_id: props.connectedUserId
            }

            const response = await api.post('demandes-intervention/', payload)
            console.log('Demande d\'intervention créée avec succès:', response)

            // Gestion des documents (création + liaison)
            const createErrors = await createAndLinkDocuments(response.id, formData.value.documents)
            
            if (createErrors.length) {
                errorMessage.value = `DI créée mais certains documents n'ont pas pu être ajoutés: ${createErrors.join(', ')}`
                loading.value = false
                return
            }

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