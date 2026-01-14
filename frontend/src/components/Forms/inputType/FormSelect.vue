<template>
    <v-select v-bind="$attrs" :label="computedLabel" :rules="fieldRules" variant="outlined" density="comfortable"
        hide-details="auto">
        <!-- Passer tous les slots au v-select parent -->
        <template v-for="(_, slot) in $slots" v-slot:[slot]="scope">
            <slot :name="slot" v-bind="scope || {}" />
        </template>
    </v-select>
</template>

<script setup>
import { computed, inject } from 'vue';

defineOptions({
    inheritAttrs: false
});

const props = defineProps({
    label: {
        type: String,
        default: ''
    },
    fieldName: {
        type: String,
        required: true
    },
    step: {
        type: Number,
        default: null
    }
});

// Injecter validation et isFieldRequired depuis le parent (BaseForm)
const validation = inject('validation', null);
const isFieldRequired = inject('isFieldRequired', null);

// Vérifier si le champ est requis
const isRequired = computed(() => {
    if (!isFieldRequired) return false;
    return isFieldRequired(props.fieldName, props.step);
});

// Label avec étoile si requis
const computedLabel = computed(() => {
    if (!props.label) return '';
    return isRequired.value ? `${props.label} *` : props.label;
});

// Récupérer les règles de validation
const fieldRules = computed(() => {
    if (!validation) return [];
    return validation.getFieldRules(props.fieldName, props.step);
});
</script>
