<template>
    <v-sheet class="pa-4 mb-4" elevation="2" rounded>
        <!-- Message d'erreur -->
        <FormAlert v-if="localError" :message="localError" type="error" dismissible @close="localError = ''"
            class="mb-4" />

        <h3 class="mb-4">
            {{ isEditMode ? 'Modifier le compteur' : 'Ajouter un compteur' }}
        </h3>

        <!-- Informations générales -->
        <v-sheet class="pa-4 mb-4" elevation="1" rounded>
            <h4 class="mb-3">Informations générales</h4>

            <v-row dense>
                <v-col cols="12" md="6">
                    <FormField v-model="counter.nom" field-name="nom" label="Nom du compteur"
                        placeholder="Saisir le nom du compteur" counter="100" required />
                </v-col>

                <v-col cols="12" md="6">
                    <FormField v-model="counter.description" field-name="description" label="Description"
                        placeholder="Saisir une description (optionnel)" counter="255" />
                </v-col>
            </v-row>

            <v-row dense>
                <v-col cols="6">
                    <FormField v-model="counter.intervalle" field-name="intervalle" type="number" label="Intervalle"
                        placeholder="0" min="1" required />
                </v-col>

                <v-col cols="6">
                    <FormField v-model="counter.unite" field-name="unite" label="Unité"
                        placeholder="Ex: heures, km, cycles..." counter="50" required />
                </v-col>
            </v-row>
        </v-sheet>

        <!-- Options -->
        <v-sheet class="pa-4 mb-4" elevation="1" rounded>
            <h4 class="mb-3">Options du compteur</h4>

            <v-row dense>
                <v-col cols="6">
                    <FormField v-model="counter.valeurCourante" field-name="valeurCourante" type="number"
                        label="Valeur actuelle" placeholder="0" min="0" />
                </v-col>

                <v-col cols="6">
                    <FormField v-model="counter.derniereIntervention" field-name="derniereIntervention" type="number"
                        label="Dernière intervention" placeholder="0" min="0" />
                </v-col>
            </v-row>

            <v-row dense justify="space-around">
                <v-checkbox v-model="counter.estGlissant" label="Compteur glissant" density="comfortable" />
                <v-checkbox v-model="counter.estPrincipal" label="Compteur principal" density="comfortable" />
            </v-row>

            <v-row dense>
                <v-col>
                    <p class="mb-2 text-subtitle-2">La maintenance nécessite :</p>
                    <v-row justify="space-around" dense>
                        <v-checkbox v-model="counter.habElec" label="Habilitation électrique" density="comfortable" />
                        <v-checkbox v-model="counter.permisFeu" label="Permis feu" density="comfortable" />
                    </v-row>
                </v-col>
            </v-row>
        </v-sheet>

        <!-- Plan de maintenance -->
        <v-sheet class="pa-4 mb-4" elevation="1" rounded>
            <h4 class="mb-3">Plan de maintenance associé</h4>
            <v-row v-if="existingPMs.length > 0">
                <v-col cols="12">
                    <FormSelect v-model="counter.planMaintenance.nom" field-name="planMaintenanceExistant"
                        label="Sélectionner un plan existant" :items="existingPMs" item-title="nom" item-value="nom"
                        clearable @update:model-value="applyExistingPM" />
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="8">
                    <FormField v-model="counter.planMaintenance.nom" field-name="planMaintenanceNom"
                        label="Nom du plan de maintenance" placeholder="Saisir le nom du plan" counter="100" />
                </v-col>
                <v-col cols="4">
                    <FormSelect v-model="counter.planMaintenance.type" field-name="planMaintenanceType" label="Type"
                        :items="typesPM" item-title="libelle" item-value="id" clearable />
                </v-col>
            </v-row>
        </v-sheet>

        <!-- Consommables -->
        <v-sheet class="pa-4 mb-4" elevation="1" rounded>
            <h4 class="mb-3">Consommables</h4>

            <v-row v-for="(c, index) in counter.planMaintenance.consommables" :key="index" dense class="mb-3">
                <v-col cols="6">
                    <FormSelect v-model="c.consommable" :field-name="`consommable_${index}`" label="Consommable"
                        :items="consumables" item-title="designation" item-value="id" clearable />
                </v-col>

                <v-col cols="3">
                    <FormField v-model.number="c.quantite" :field-name="`quantite_${index}`" type="number"
                        label="Quantité" placeholder="1" min="1" />
                </v-col>

                <v-col cols="3" class="d-flex align-center">
                    <v-btn icon="mdi-delete" size="small" color="error" @click="removePMConsumable(index)" />
                </v-col>
            </v-row>

            <v-btn color="primary" variant="outlined" prepend-icon="mdi-plus" @click="addPMConsumable">
                Ajouter un consommable
            </v-btn>
        </v-sheet>

        <!-- Documents -->
        <v-sheet class="pa-4 mb-4" elevation="1" rounded>
            <h4 class="mb-3">Documents</h4>

            <v-row v-for="(doc, index) in counter.planMaintenance.documents" :key="index" dense class="mb-3">
                <v-col cols="4">
                    <FormField v-model="doc.titre" :field-name="`documentTitre_${index}`" label="Titre"
                        placeholder="Titre du document" counter="100" />
                </v-col>

                <v-col cols="5">
                    <label class="field-label">Document</label>
                    <v-file-input v-model="doc.file" density="comfortable" variant="outlined" show-size clearable
                        prepend-icon="" prepend-inner-icon="mdi-file-document" hide-details="auto">
                        <template #selection>
                            <span v-if="doc.file">
                                {{ doc.file.name }}
                            </span>
                            <span v-else-if="doc.path">
                                {{ getFileName(doc.path) }}
                            </span>
                            <span v-else class="text-grey">
                                Aucun fichier sélectionné
                            </span>
                        </template>
                    </v-file-input>
                </v-col>

                <v-col cols="2">
                    <FormSelect v-model="doc.type" :field-name="`documentType_${index}`" label="Type"
                        :items="typesDocuments" item-title="nomTypeDocument" item-value="id" clearable />
                </v-col>

                <v-col cols="1" class="d-flex align-center">
                    <v-btn icon="mdi-delete" size="small" color="error" @click="removePMDocument(index)" />
                </v-col>
            </v-row>

            <v-btn color="primary" variant="outlined" prepend-icon="mdi-plus" @click="addPMDocument">
                Ajouter un document
            </v-btn>
        </v-sheet>

        <!-- Actions du formulaire -->
        <v-row class="mt-4" justify="end">
            <v-btn v-if="!isFirstCounter" variant="text" @click="handleCancel">
                Annuler
            </v-btn>
            <v-btn color="primary" class="ml-2" @click="handleSave">
                {{ isEditMode ? 'Modifier le compteur' : 'Ajouter le compteur' }}
            </v-btn>
        </v-row>
    </v-sheet>
</template>

<script setup>
import { computed, ref } from 'vue'
import { FormField, FormSelect, FormAlert } from '@/components/common'
import { useFormValidation } from '@/composables/useFormValidation'

const props = defineProps({
    modelValue: {
        type: Object,
        required: true
    },
    existingPMs: {
        type: Array,
        default: () => []
    },
    typesPM: {
        type: Array,
        default: () => []
    },
    consumables: {
        type: Array,
        default: () => []
    },
    typesDocuments: {
        type: Array,
        default: () => []
    },
    isEditMode: {
        type: Boolean,
        default: false
    },
    isFirstCounter: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:modelValue', 'save', 'cancel'])

const localError = ref('')

// Schéma de validation
const validationSchema = {
    nom: ['required', { name: 'maxLength', params: [100] }],
    description: [{ name: 'maxLength', params: [255] }],
    intervalle: ['required', 'numeric', 'positive', { name: 'min', params: [1] }],
    unite: ['required', { name: 'maxLength', params: [50] }],
    valeurCourante: ['numeric', 'positive'],
    derniereIntervention: ['numeric', 'positive']
}

const validation = useFormValidation(validationSchema)

const counter = computed({
    get: () => props.modelValue,
    set: v => emit('update:modelValue', v)
})

const addPMConsumable = () => {
    counter.value.planMaintenance.consommables.push({ consommable: null, quantite: 1 })
}

const removePMConsumable = (i) => {
    counter.value.planMaintenance.consommables.splice(i, 1)
}

const addPMDocument = () => {
    counter.value.planMaintenance.documents.push({ titre: '', file: null, type: null })
}

const removePMDocument = (i) => {
    counter.value.planMaintenance.documents.splice(i, 1)
}

const applyExistingPM = (nom) => {
    const pm = props.existingPMs.find(p => p.nom === nom)
    if (!pm) return

    counter.value.planMaintenance = {
        nom: pm.nom,
        type: pm.type ?? null,
        consommables: pm.consommables ? JSON.parse(JSON.stringify(pm.consommables)) : [],
        documents: pm.documents ? [...pm.documents] : []
    }
}

const handleSave = () => {
    localError.value = ''

    // Validation avec le composable
    if (!validation.validateAll(counter.value)) {
        const errors = Object.values(validation.errors.value).flat()
        localError.value = errors[0] || 'Veuillez vérifier les champs requis'
        return
    }

    // Si tout est valide, émettre l'événement save
    emit('save')
}

const handleCancel = () => {
    localError.value = ''
    validation.clearErrors()
    emit('cancel')
}

const getFileName = (path) => {
    return path?.split('/').pop() || ''
}
</script>

<style scoped>
.field-label {
    display: block;
    margin-bottom: 4px;
    font-size: 0.875rem;
    font-weight: 500;
    color: rgba(0, 0, 0, 0.87);
}
</style>
