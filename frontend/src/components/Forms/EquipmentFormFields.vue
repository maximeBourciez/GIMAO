<template>
    <v-row>
        <!-- Informations générales -->
        <v-col cols="12" md="6">
            <FormField v-model="modelValue.numSerie" field-name="numSerie" :step="step" label="Numéro de série"
                placeholder="Saisir le numéro de série" counter="100" />
        </v-col>

        <v-col cols="12" md="6">
            <FormField v-model="modelValue.reference" field-name="reference" :step="step" label="Référence"
                placeholder="Saisir la référence" counter="100" />
        </v-col>

        <v-col cols="12" md="6">
            <FormField v-model="modelValue.designation" field-name="designation" :step="step" label="Désignation"
                placeholder="Saisir la désignation" counter="100" />
        </v-col>

        <v-col cols="12" md="6">
            <FormField v-model="modelValue.dateMiseEnService" field-name="dateMiseEnService" :step="step"
                label="Date de mise en service" type="date" />
        </v-col>

        <v-col cols="12" md="6">
            <FormField v-model="modelValue.prixAchat" field-name="prixAchat" :step="step" label="Prix d'achat"
                type="number" placeholder="0.00" suffix="€" step="0.01" min="0" />
        </v-col>

        <v-col cols="12" md="6">
            <FormFileInput
                label="Image de l'équipement"
                placeholder="Sélectionner une image"
                accept="image/*"
                prepend-inner-icon="mdi-camera"
                @update:model-value="handleFileUpload"
            />
        </v-col>

        <!-- Modèle, Fournisseur, Fabricant, Famille -->
        <v-col cols="12" md="6">
            <FormSelect v-model="modelValue.modeleEquipement" field-name="modeleEquipement" :step="step" label="Modèle"
                :items="equipmentModels" item-title="nom" item-value="id" clearable />
        </v-col>

        <v-col cols="12" md="6">
            <FormSelect v-model="modelValue.fournisseur" field-name="fournisseur" :step="step" label="Fournisseur"
                :items="fournisseurs" item-title="nom" item-value="id" clearable />
        </v-col>

        <v-col cols="12" md="6">
            <FormSelect v-model="modelValue.fabricant" field-name="fabricant" :step="step" label="Fabricant"
                :items="fabricants" item-title="nom" item-value="id" clearable />
        </v-col>

        <v-col cols="12" md="6">
            <FormSelect v-model="modelValue.famille" field-name="famille" :step="step" label="Famille" :items="familles"
                item-title="nom" item-value="id" clearable />
        </v-col>

        <!-- Localisation -->
        <v-col v-if="showLocation" cols="12" :md="showStatus ? 6 : 12">
            <LocationTreeView :items="locations" v-model:selected="modelValue.lieu" @created="handleLocationCreated" />
        </v-col>

        <!-- Statut -->
        <v-col v-if="showStatus" cols="12" md="6">
            <FormSelect v-model="modelValue.statut" field-name="statut" :step="step" label="Statut"
                :items="equipmentStatuses" item-title="label" item-value="value" />
        </v-col>

        <!-- Consommables -->
        <v-col v-if="showConsommables" cols="12">
            <v-divider class="my-4" />
            <h3 class="mb-3">Consommables</h3>
            <v-select v-model="modelValue.consommables" :items="consumables" item-title="designation" item-value="id"
                multiple chips label="Consommables" />
        </v-col>

        <!-- Compteurs -->
        <v-col v-if="showCounters" cols="12">
            <v-divider class="my-4" />
            <h3 class="mb-3">Compteurs</h3>
            <v-data-table :items="modelValue.compteurs" :headers="TABLE_HEADERS.COUNTERS" class="elevation-1">
                <template #item.nom="{ item }">
                    {{ item.nom }}
                </template>
                <template #item.intervalle="{ item }">
                    {{ item.intervalle }}
                </template>
                <template #item.unite="{ item }">
                    {{ item.unite }}
                </template>
                <template #item.options="{ item }">
                    <div>
                        {{ item.estGlissant && item.estPrincipal ? 'Glissant et Principal' :
                            item.estGlissant ? 'Glissant' :
                                item.estPrincipal ? 'Principal' :
                        'Aucune' }}
                    </div>
                </template>
                <template #item.planMaintenance="{ item }">
                    <div>
                        <v-icon left small>mdi-wrench</v-icon>
                        {{ item.planMaintenance?.nom?.slice(0, 20) || 'Aucun plan associé' }}
                    </div>
                </template>
                <template #item.actions="{ item }">
                    <v-row>
                        <v-btn icon color="blue" @click="$emit('edit-counter', item)" size="30" class="mr-2">
                            <v-icon size="14">mdi-pencil</v-icon>
                        </v-btn>
                        <v-btn icon color="red" @click="$emit('delete-counter', item)" size="30">
                            <v-icon size="14">mdi-delete</v-icon>
                        </v-btn>
                    </v-row>
                </template>
            </v-data-table>
        </v-col>
    </v-row>
</template>

<script setup>
import { FormField, FormSelect, FormFileInput } from '@/components/common';
import LocationTreeView from '@/components/LocationTreeView.vue';
import { TABLE_HEADERS } from '@/utils/constants';

const props = defineProps({
    modelValue: {
        type: Object,
        required: true
    },
    equipmentModels: {
        type: Array,
        default: () => []
    },
    fournisseurs: {
        type: Array,
        default: () => []
    },
    fabricants: {
        type: Array,
        default: () => []
    },
    familles: {
        type: Array,
        default: () => []
    },
    locations: {
        type: Array,
        default: () => []
    },
    consumables: {
        type: Array,
        default: () => []
    },
    equipmentStatuses: {
        type: Array,
        default: () => []
    },
    step: {
        type: Number,
        default: undefined
    },
    showLocation: {
        type: Boolean,
        default: true
    },
    showStatus: {
        type: Boolean,
        default: true
    },
    showConsommables: {
        type: Boolean,
        default: true
    },
    showCounters: {
        type: Boolean,
        default: true
    }
});

const emit = defineEmits(['update:modelValue', 'file-upload', 'location-created', 'edit-counter', 'delete-counter']);

const handleFileUpload = (file) => {
    emit('file-upload', file);
};

const handleLocationCreated = (newLocation) => {
    emit('location-created', newLocation);
};
</script>

<style scoped>
</style>
