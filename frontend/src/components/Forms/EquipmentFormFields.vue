<template>
    <v-row>
        <template v-if="showGeneral">
            <!-- Informations générales -->
            <v-col cols="12">
                <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                    Informations générales
                </v-card-subtitle>
            </v-col>

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
                    placeholder="0.00" suffix="€" />
            </v-col>

            <v-col cols="12" md="6">
                <FormFileInput label="Image de l'équipement" placeholder="Sélectionner une image" accept="image/*"
                    prepend-inner-icon="mdi-camera" @update:model-value="handleFileUpload" />
            </v-col>
        </template>

        <template v-if="showModelInfo">
            <v-col cols="12">
                <v-divider class="my-4"></v-divider>
                <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                    Modèle et références
                </v-card-subtitle>
            </v-col>

            <v-col cols="12" md="6">
                <FormSelect v-model="modelValue.modeleEquipement" field-name="modeleEquipement" :step="step"
                    label="Modèle" :items="equipmentModels" item-title="nom" item-value="id" clearable />
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
                <FormSelect v-model="modelValue.famille" field-name="famille" :step="step" label="Famille"
                    :items="familles" item-title="nom" item-value="id" clearable />
            </v-col>
        </template>

        <!-- Localisation et Statut -->
        <template v-if="showLocation || showStatus">
            <v-col cols="12">
                <v-divider class="my-4"></v-divider>
                <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                    Localisation et statut
                </v-card-subtitle>
            </v-col>

            <v-col v-if="showLocation" cols="12" :md="showStatus ? 6 : 12">
                <LocationTreeView :items="locations" v-model:selected="modelValue.lieu"
                    @created="handleLocationCreated" />
            </v-col>

            <v-col v-if="showStatus" cols="12" md="6">
                <FormSelect v-model="modelValue.statut" field-name="statut" :step="step" label="Statut"
                    :items="equipmentStatuses" item-title="label" item-value="value" />
            </v-col>
        </template>

        <!-- Consommables -->
        <template v-if="showConsommables">
            <v-col cols="12">
                <v-divider class="my-4"></v-divider>
                <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                    Consommables associés
                </v-card-subtitle>
            </v-col>

            <v-col cols="12">
                <FormSelect v-model="modelValue.consommables" label="Consommables" :items="consumables"
                    item-title="designation" item-value="id" multiple chips clearable />
            </v-col>
        </template>

        <!-- Compteurs -->
        <template v-if="showCounters">
            <v-col cols="12">
                <v-divider class="my-4"></v-divider>
                <v-card-subtitle class="text-h6 font-weight-bold px-0 pb-2">
                    Compteurs
                </v-card-subtitle>
            </v-col>

            <v-col cols="12">
                <v-data-table :items="modelValue.compteurs" :headers="TABLE_HEADERS.COUNTERS" class="elevation-1"
                    density="comfortable">
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
                        <div class="d-flex align-center">
                            <v-icon size="small" class="mr-1">mdi-wrench</v-icon>
                            <span class="text-truncate" style="max-width: 200px;">
                                {{ item.planMaintenance?.nom || 'Aucun plan associé' }}
                            </span>
                        </div>
                    </template>
                    <template #item.actions="{ item }">
                        <div class="d-flex gap-1">
                            <v-btn icon="mdi-pencil" size="small" color="primary" variant="text"
                                @click="$emit('edit-counter', item)" />
                            <v-btn icon="mdi-delete" size="small" color="error" variant="text"
                                @click="$emit('delete-counter', item)" />
                        </div>
                    </template>
                </v-data-table>
            </v-col>
        </template>
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
    },
    showGeneral: {
        type: Boolean,
        default: true
    },
    showModelInfo: {
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

<style scoped></style>
