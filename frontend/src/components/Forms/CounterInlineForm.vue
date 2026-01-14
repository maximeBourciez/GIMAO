<template>
    <BaseForm v-model="counter" :title="isEditMode ? 'Modifier le compteur' : 'Ajouter un compteur'"
        :validation-schema="validationSchema" :handleSubmit="handleSave" :error-message="localError"
        :show-cancel-button="!isFirstCounter" :custom-cancel-action="true" @cancel="handleCancel"
        :submit-button-text="isEditMode ? 'Modifier le compteur' : 'Ajouter le compteur'" elevation="0">

        <template #default>
            <!-- Informations générales -->
            <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                Informations générales
            </v-card-subtitle>

            <v-row dense>
                <v-col cols="12" md="6">
                    <FormField v-model="counter.nom" field-name="nom" label="Nom du compteur"
                        placeholder="Saisir le nom du compteur" counter="100" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormField v-model="counter.description" field-name="description" label="Description"
                        placeholder="Saisir une description (optionnel)" counter="255" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormField v-model="counter.intervalle" field-name="intervalle" type="number" label="Intervalle"
                        placeholder="0" min="1" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormField v-model="counter.unite" field-name="unite" label="Unité"
                        placeholder="Ex: heures, km, cycles..." counter="50" />
                </v-col>
            </v-row>

            <v-divider class="my-6"></v-divider>

            <!-- Options du compteur -->
            <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                Options du compteur
            </v-card-subtitle>

            <v-row dense>
                <v-col cols="12" md="6">
                    <FormField v-model="counter.valeurCourante" field-name="valeurCourante" type="number"
                        label="Valeur actuelle" placeholder="0" min="0" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormField v-model="counter.derniereIntervention" field-name="derniereIntervention" type="number"
                        label="Dernière intervention" placeholder="0" min="0" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormCheckbox v-model="counter.estGlissant" field-name="estGlissant" label="Compteur glissant" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormCheckbox v-model="counter.estPrincipal" field-name="estPrincipal" label="Compteur principal" />
                </v-col>
            </v-row>

            <v-row dense class="mt-2">
                <v-col cols="12">
                    <p class="text-subtitle-2 font-weight-medium mb-3">La maintenance nécessite :</p>
                </v-col>

                <v-col cols="12" md="6">
                    <FormCheckbox v-model="counter.habElec" field-name="habElec" label="Habilitation électrique" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormCheckbox v-model="counter.permisFeu" field-name="permisFeu" label="Permis feu" />
                </v-col>
            </v-row>

            <v-divider class="my-6"></v-divider>

            <!-- Plan de maintenance -->
            <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                Plan de maintenance associé
            </v-card-subtitle>

            <v-row dense v-if="existingPMs.length > 0">
                <v-col cols="12">
                    <FormSelect v-model="counter.planMaintenance.nom" field-name="planMaintenanceExistant"
                        label="Sélectionner un plan existant" :items="existingPMs" item-title="nom" item-value="nom"
                        clearable @update:model-value="applyExistingPM" />
                </v-col>
            </v-row>

            <v-row dense>
                <v-col cols="12" md="8">
                    <FormField v-model="counter.planMaintenance.nom" field-name="planMaintenanceNom"
                        label="Nom du plan de maintenance" placeholder="Saisir le nom du plan" counter="100" />
                </v-col>
                <v-col cols="12" md="4">
                    <FormSelect v-model="counter.planMaintenance.type" field-name="planMaintenanceType" label="Type"
                        :items="typesPM" item-title="libelle" item-value="id" clearable />
                </v-col>
            </v-row>

            <v-divider class="my-6"></v-divider>

            <!-- Consommables -->
            <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                Consommables
            </v-card-subtitle>

            <v-row v-for="(c, index) in counter.planMaintenance.consommables" :key="index" dense class="mb-2">
                <v-col cols="12" md="7">
                    <FormSelect v-model="c.consommable" :field-name="`consommable_${index}`" label="Consommable"
                        :items="consumables" item-title="designation" item-value="id" clearable />
                </v-col>

                <v-col cols="10" md="4">
                    <FormField v-model.number="c.quantite" :field-name="`quantite_${index}`" type="number"
                        label="Quantité" placeholder="1" min="1" />
                </v-col>

                <v-col cols="2" md="1" class="d-flex align-center justify-center">
                    <v-btn icon="mdi-delete" size="small" color="error" variant="text"
                        @click="removePMConsumable(index)" />
                </v-col>
            </v-row>

            <v-row dense>
                <v-col cols="12">
                    <v-btn color="primary" variant="text" prepend-icon="mdi-plus" @click="addPMConsumable">
                        Ajouter un consommable
                    </v-btn>
                </v-col>
            </v-row>

            <v-divider class="my-6"></v-divider>

            <!-- Documents -->
            <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                Documents
            </v-card-subtitle>

            <v-row v-for="(doc, index) in counter.planMaintenance.documents" :key="index" dense class="mb-2">
                <v-col cols="12" md="4">
                    <FormField v-model="doc.titre" :field-name="`documentTitre_${index}`" label="Titre"
                        placeholder="Titre du document" counter="100" />
                </v-col>

                <v-col cols="12" md="4">
                    <FormFileInput v-model="doc.file" label="Document" prepend-icon=""
                        prepend-inner-icon="mdi-file-document">
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
                    </FormFileInput>
                </v-col>

                <v-col cols="10" md="3">
                    <FormSelect v-model="doc.type" :field-name="`documentType_${index}`" label="Type"
                        :items="typesDocuments" item-title="nomTypeDocument" item-value="id" clearable />
                </v-col>

                <v-col cols="2" md="1" class="d-flex align-center justify-center">
                    <v-btn icon="mdi-delete" size="small" color="error" variant="text"
                        @click="removePMDocument(index)" />
                </v-col>
            </v-row>

            <v-row dense>
                <v-col cols="12">
                    <v-btn color="primary" variant="text" prepend-icon="mdi-plus" @click="addPMDocument">
                        Ajouter un document
                    </v-btn>
                </v-col>
            </v-row>
        </template>
    </BaseForm>
</template>

<script setup>
import { computed, ref } from 'vue'
import { BaseForm, FormField, FormSelect, FormCheckbox, FormFileInput } from '@/components/common'

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
    // La validation est gérée par BaseForm
    emit('save')
}

const handleCancel = () => {
    localError.value = ''
    emit('cancel')
}

const getFileName = (path) => {
    return path?.split('/').pop() || ''
}
</script>
