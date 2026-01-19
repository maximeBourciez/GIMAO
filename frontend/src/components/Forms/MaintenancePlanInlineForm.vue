<template>
    <v-form @submit.prevent="handleSave">
        <!-- Section: Configuration des seuils -->
        <div v-if="!hideSeuilSection">
            <h4 class="mb-3 text-body-1 font-weight-bold">
                <v-icon left color="primary" size="small">mdi-gauge</v-icon>
                Configuration du seuil
            </h4>
            <v-row dense>
                <v-col cols="12" md="6">
                    <FormSelect v-model="plan.compteurIndex" field-name="compteurIndex" label="Compteur associé"
                        :items="countersForSelect" item-title="label" item-value="value">
                        <template #item="{ props, item }">
                            <v-list-item v-bind="props">
                                <template #prepend>
                                    <v-icon :color="item.raw.isPrincipal ? 'primary' : 'grey'">
                                        mdi-{{ item.raw.isPrincipal ? 'star' : 'counter' }}
                                    </v-icon>
                                </template>
                                <v-list-item-title>
                                    {{ item.raw.label }}
                                    <span v-if="item.raw.isPrincipal"
                                        class="text-caption text-primary ml-1">(Principal)</span>
                                </v-list-item-title>
                                <v-list-item-subtitle>
                                    {{ item.raw.currentValue }} {{ item.raw.unit }}
                                </v-list-item-subtitle>
                            </v-list-item>
                        </template>
                    </FormSelect>
                </v-col>

                <v-col cols="12" md="6">
                    <FormField :model-value="selectedCounterValue" field-name="valeurCompteur"
                        label="Valeur du compteur" :readonly="true" :suffix="selectedCounterUnit" />
                </v-col>

                <v-col cols="12" md="4">
                    <FormField v-model.number="plan.seuil.derniereIntervention" field-name="derniereIntervention"
                        type="number" label="Dernière intervention" placeholder="0" min="0"
                        @update:model-value="updateProchaineMaintenance" />
                </v-col>

                <v-col cols="12" md="4">
                    <FormField v-model.number="plan.seuil.ecartInterventions" field-name="ecartInterventions"
                        type="number" label="Écart entre interventions" placeholder="0" min="0"
                        @update:model-value="updateProchaineMaintenance" />
                </v-col>

                <v-col cols="12" md="4">
                    <FormField v-model.number="plan.seuil.prochaineMaintenance" field-name="prochaineMaintenance"
                        type="number" label="Prochaine maintenance" :readonly="true" />
                </v-col>

                <v-col cols="12" md="4">
                    <FormCheckbox v-model="plan.seuil.estGlissant" field-name="estGlissant" label="Seuil glissant" />
                </v-col>
            </v-row>

            <v-divider class="my-4"></v-divider>
        </div>

        <!-- Sélection de PM existant ou création -->
        <div v-if="showPmSelection">
            <h4 class="mb-3 text-body-1 font-weight-bold">
                <v-icon left color="primary" size="small">mdi-clipboard-check</v-icon>
                Plan de maintenance
            </h4>
            <v-radio-group v-model="pmMode" inline hide-details class="mb-4">
                <v-radio label="Sélectionner un PM existant" value="existing"></v-radio>
                <v-radio label="Créer un nouveau PM" value="new"></v-radio>
            </v-radio-group>

            <v-divider class="my-4"></v-divider>
        </div>

        <!-- Sélection PM existant -->
        <div v-if="showPmSelection && pmMode === 'existing'">
            <v-row dense>
                <v-col cols="12">
                    <v-select v-model="selectedExistingPMId" :items="existingPMs" item-title="nom" item-value="id"
                        label="Sélectionner un plan de maintenance" variant="outlined" density="comfortable" clearable>
                        <template #item="{ props, item }">
                            <v-list-item v-bind="props">
                                <template #title>{{ item.raw.nom }}</template>
                                <template #subtitle>{{ getPMTypeLabel(item.raw.type_id) }}</template>
                            </v-list-item>
                        </template>
                    </v-select>
                </v-col>
            </v-row>

            <!-- Aperçu du PM sélectionné -->
            <v-alert v-if="selectedExistingPM" type="info" class="mt-4" variant="tonal">
                <div class="text-subtitle-2 font-weight-bold mb-2">
                    <v-icon left size="small">mdi-information</v-icon>
                    Aperçu du plan sélectionné
                </div>
                <v-row dense class="mb-2">
                    <v-col cols="12" md="6">
                        <div class="text-caption">Nom du plan</div>
                        <div class="font-weight-medium">{{ selectedExistingPM.nom }}</div>
                    </v-col>
                    <v-col cols="12" md="6">
                        <div class="text-caption">Type de maintenance</div>
                        <div class="font-weight-medium">{{ getPMTypeLabel(selectedExistingPM.type_id) }}</div>
                    </v-col>
                </v-row>
                <div v-if="selectedExistingPM.commentaire" class="mt-2">
                    <div class="text-caption">Commentaire</div>
                    <div>{{ selectedExistingPM.commentaire }}</div>
                </div>
                <div v-if="selectedExistingPM.necessiteHabilitationElectrique || selectedExistingPM.necessitePermisFeu"
                    class="mt-2">
                    <div class="text-caption mb-1">Habilitations requises</div>
                    <v-chip v-if="selectedExistingPM.necessiteHabilitationElectrique" size="small" color="orange"
                        class="mr-2">
                        <v-icon left size="small">mdi-flash</v-icon>
                        Habilitation électrique
                    </v-chip>
                    <v-chip v-if="selectedExistingPM.necessitePermisFeu" size="small" color="red">
                        <v-icon left size="small">mdi-fire</v-icon>
                        Permis feu
                    </v-chip>
                </div>
            </v-alert>
        </div>

        <!-- Section: Plan de maintenance (nouveau) -->
        <div v-if="!showPmSelection || pmMode === 'new'">
            <h4 class="mb-3 text-body-1 font-weight-bold">
                <v-icon left color="primary" size="small">mdi-clipboard-check</v-icon>
                Informations du plan de maintenance
            </h4>
            <v-row dense>
                <v-col cols="12" md="6">
                    <FormField v-model="plan.nom" field-name="nom" label="Nom du plan"
                        placeholder="Saisir le nom du plan" counter="100" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormSelect v-model="plan.type_id" field-name="type_id" label="Type de maintenance" :items="typesPM"
                        item-title="libelle" item-value="id" />
                </v-col>

                <v-col cols="12">
                    <FormField v-model="plan.description" field-name="description" label="Description" type="textarea"
                        rows="2" placeholder="Description du plan de maintenance" />
                </v-col>
            </v-row>

            <v-divider class="my-4"></v-divider>

            <!-- Section: Consommables -->
            <h4 class="mb-3 text-body-1 font-weight-bold">
                <v-icon left color="primary" size="small">mdi-package-variant</v-icon>
                Consommables nécessaires
            </h4>
            <v-row dense>
                <v-col cols="12">
                    <FormSelect v-model="plan.consommables" field-name="consommables"
                        label="Sélectionnez les consommables" :items="consumables" item-title="designation"
                        item-value="id" multiple chips />
                </v-col>
            </v-row>

            <v-divider class="my-4"></v-divider>

            <!-- Section: Documents -->
            <h4 class="mb-3 text-body-1 font-weight-bold">
                <v-icon left color="primary" size="small">mdi-file-document</v-icon>
                Documents associés
            </h4>

            <v-row v-for="(doc, index) in plan.documents" :key="index" dense class="mb-2 align-center">
                <v-col cols="12" md="5">
                    <v-text-field v-model="doc.nom" label="Nom du document" variant="outlined" density="comfortable"
                        hide-details></v-text-field>
                </v-col>
                <v-col cols="12" md="3">
                    <v-select v-model="doc.type_id" :items="typesDocuments" item-title="nomTypeDocument" item-value="id"
                        label="Type de document" variant="outlined" density="comfortable" hide-details></v-select>
                </v-col>
                <v-col cols="12" md="3">
                    <v-file-input v-model="doc.file" label="Fichier" variant="outlined" density="comfortable"
                        hide-details prepend-icon="" prepend-inner-icon="mdi-paperclip"
                        :show-size="true"></v-file-input>
                </v-col>
                <v-col cols="12" md="1" class="text-right">
                    <v-btn icon size="small" color="error" variant="text" @click="removeDocument(index)">
                        <v-icon>mdi-delete</v-icon>
                    </v-btn>
                </v-col>
            </v-row>

            <v-row dense>
                <v-col cols="12">
                    <v-btn variant="outlined" color="primary" size="small" @click="addDocument">
                        <v-icon left>mdi-plus</v-icon>
                        Ajouter un document
                    </v-btn>
                </v-col>
            </v-row>

            <v-divider class="my-4"></v-divider>

            <!-- Section: Habilitations -->
            <h4 class="mb-3 text-body-1 font-weight-bold">
                <v-icon left color="primary" size="small">mdi-shield-account</v-icon>
                Habilitations requises
            </h4>
            <v-row dense>
                <v-col cols="12" md="6">
                    <FormCheckbox v-model="plan.necessiteHabilitationElectrique"
                        field-name="necessiteHabilitationElectrique" label="Habilitation électrique requise"
                        color="orange" />
                </v-col>

                <v-col cols="12" md="6">
                    <FormCheckbox v-model="plan.necessitePermisFeu" field-name="necessitePermisFeu"
                        label="Permis feu requis" color="red" />
                </v-col>
            </v-row>
        </div>

        <v-alert v-if="localError" type="error" class="mt-4">{{ localError }}</v-alert>

        <v-card-actions v-if="showActions" class="px-0 pt-4">
            <v-spacer />
            <v-btn variant="text" @click="handleCancel">Annuler</v-btn>
            <v-btn type="submit" color="primary" :disabled="!isValid">
                {{ isEditMode ? 'Modifier le plan' : 'Ajouter le plan' }}
            </v-btn>
        </v-card-actions>
    </v-form>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { FormField, FormCheckbox, FormSelect } from '@/components/common'

const props = defineProps({
    modelValue: {
        type: Object,
        required: true
    },
    isEditMode: {
        type: Boolean,
        default: false
    },
    showActions: {
        type: Boolean,
        default: true
    },
    hideSeuilSection: {
        type: Boolean,
        default: false
    },
    showPmSelection: {
        type: Boolean,
        default: false
    },
    existingPMs: {
        type: Array,
        default: () => []
    },
    counters: {
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
    }
})

const emit = defineEmits(['update:modelValue', 'save', 'cancel'])

const localError = ref('')
const pmMode = ref('new')
const selectedExistingPMId = ref(null)

const plan = computed({
    get: () => props.modelValue,
    set: v => emit('update:modelValue', v)
})

// Transformer les compteurs pour le select
const countersForSelect = computed(() => {
    return props.counters.map((counter, index) => ({
        value: index,
        label: counter.nom,
        isPrincipal: counter.estPrincipal,
        currentValue: counter.valeurCourante,
        unit: counter.unite
    }))
})

// Valeur et unité du compteur sélectionné
const selectedCounterValue = computed(() => {
    if (plan.value.compteurIndex === null || plan.value.compteurIndex === undefined) return '—'
    const counter = props.counters[plan.value.compteurIndex]
    return counter?.valeurCourante ?? '—'
})

const selectedCounterUnit = computed(() => {
    if (plan.value.compteurIndex === null || plan.value.compteurIndex === undefined) return ''
    const counter = props.counters[plan.value.compteurIndex]
    return counter?.unite ?? ''
})

const selectedExistingPM = computed(() =>
    props.existingPMs.find(pm => pm.id === selectedExistingPMId.value)
)

const getPMTypeLabel = (typeId) => {
    const type = props.typesPM.find(t => t.id === typeId)
    return type ? type.libelle : "Non spécifié"
}

const isValid = computed(() => {
    // Vérifier d'abord que le seuil est valide
    const seuilValid = plan.value.seuil?.ecartInterventions > 0

    if (!seuilValid) return false

    if (props.showPmSelection && pmMode.value === 'existing') {
        return !!selectedExistingPMId.value
    }

    return plan.value.nom &&
        plan.value.nom.trim() !== '' &&
        plan.value.type_id !== null &&
        plan.value.compteurIndex !== null &&
        plan.value.compteurIndex !== undefined
})

// Calcul automatique de la prochaine maintenance
const updateProchaineMaintenance = () => {
    const derniere = plan.value.seuil.derniereIntervention || 0
    const intervalle = plan.value.seuil.ecartInterventions || 0
    plan.value.seuil.prochaineMaintenance = derniere + intervalle
}

// Gestion des documents
const addDocument = () => {
    if (!plan.value.documents) {
        plan.value.documents = []
    }
    plan.value.documents.push({
        nom: '',
        type_id: null,
        file: null
    })
}

const removeDocument = (index) => {
    plan.value.documents.splice(index, 1)
}

const handleSave = () => {
    if (!isValid.value) {
        localError.value = 'Veuillez remplir tous les champs obligatoires (nom, type et compteur)'
        return
    }
    localError.value = ''
    emit('save', {
        pmMode: pmMode.value,
        selectedExistingPMId: selectedExistingPMId.value
    })
}

const handleCancel = () => {
    localError.value = ''
    emit('cancel')
}
</script>
