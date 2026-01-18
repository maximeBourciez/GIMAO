<template>
    <v-form @submit.prevent="handleSave">
        <!-- Section: Informations générales -->
        <v-row dense>
            <v-col cols="12" md="6">
                <FormField v-model="plan.nom" field-name="nom" label="Nom du plan" 
                    placeholder="Saisir le nom du plan" counter="100" />
            </v-col>

            <v-col cols="12" md="6">
                <FormSelect v-model="plan.type_id" field-name="type_id" label="Type de maintenance"
                    :items="typesPM" item-title="libelle" item-value="id" />
            </v-col>

            <v-col cols="12">
                <FormField v-model="plan.description" field-name="description" label="Description" 
                    type="textarea" rows="2" placeholder="Description du plan de maintenance" />
            </v-col>
        </v-row>

        <v-divider class="my-4" />

        <!-- Section: Configuration des seuils -->
        <h4 class="mb-3 text-body-1 font-weight-bold">Configuration des seuils</h4>
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
                                <span v-if="item.raw.isPrincipal" class="text-caption text-primary ml-1">(Principal)</span>
                            </v-list-item-title>
                            <v-list-item-subtitle>
                                {{ item.raw.currentValue }} {{ item.raw.unit }}
                            </v-list-item-subtitle>
                        </v-list-item>
                    </template>
                </FormSelect>
            </v-col>

            <v-col cols="12" md="6" class="d-flex align-center">
                <FormCheckbox v-model="plan.seuil.estGlissant" field-name="estGlissant" 
                    label="Seuil glissant" />
            </v-col>
        </v-row>

        <!-- Section: Paramètres du seuil -->
        <v-row dense class="mt-2">
            <v-col cols="12" md="4">
                <FormField v-model.number="plan.seuil.derniereIntervention" 
                    field-name="derniereIntervention" type="number" 
                    label="Dernière intervention" placeholder="0" min="0" 
                    suffix="unité" @update:model-value="updateProchaineMaintenance" />
            </v-col>

            <v-col cols="12" md="4">
                <FormField v-model.number="plan.seuil.ecartInterventions" 
                    field-name="ecartInterventions" type="number" 
                    label="Intervalle" placeholder="0" min="0" 
                    suffix="unité" @update:model-value="updateProchaineMaintenance" />
            </v-col>

            <v-col cols="12" md="4">
                <FormField v-model.number="plan.seuil.prochaineMaintenance" 
                    field-name="prochaineMaintenance" type="number" 
                    label="Prochaine maintenance" :readonly="true" 
                    suffix="unité" />
            </v-col>
        </v-row>

        <v-divider class="my-4" />

        <!-- Section: Consommables -->
        <h4 class="mb-3 text-body-1 font-weight-bold">Consommables nécessaires</h4>
        <v-row dense>
            <v-col cols="12">
                <FormSelect v-model="plan.consommables" field-name="consommables" 
                    label="Sélectionnez les consommables" :items="consumables" 
                    item-title="designation" item-value="id" multiple chips />
            </v-col>
        </v-row>

        <v-divider class="my-4" />

        <!-- Section: Habilitations -->
        <h4 class="mb-3 text-body-1 font-weight-bold">Habilitations requises</h4>
        <v-row dense>
            <v-col cols="12" md="6">
                <FormCheckbox v-model="plan.necessiteHabilitationElectrique" 
                    field-name="necessiteHabilitationElectrique" 
                    label="Habilitation électrique requise" 
                    color="orange" />
            </v-col>

            <v-col cols="12" md="6">
                <FormCheckbox v-model="plan.necessitePermisFeu" 
                    field-name="necessitePermisFeu" 
                    label="Permis feu requis" 
                    color="red" />
            </v-col>
        </v-row>

        <v-alert v-if="localError" type="error" class="mt-4">{{ localError }}</v-alert>

        <v-card-actions class="px-0 pt-4">
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
    }
})

const emit = defineEmits(['update:modelValue', 'save', 'cancel'])

const localError = ref('')

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

const isValid = computed(() => {
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

const handleSave = () => {
    if (!isValid.value) {
        localError.value = 'Veuillez remplir tous les champs obligatoires (nom, type et compteur)'
        return
    }
    localError.value = ''
    emit('save')
}

const handleCancel = () => {
    localError.value = ''
    emit('cancel')
}
</script>
