<template>
    <div>
        <label v-if="label" class="field-label">
            {{ label }} <span v-if="isRequired" class="required-star">*</span>
        </label>
        <v-text-field v-bind="$attrs" :rules="fieldRules" variant="outlined" density="comfortable"
            hide-details="auto" />
    </div>
</template>

<script setup>
import { computed, inject } from 'vue';

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

// Récupérer les règles de validation
const fieldRules = computed(() => {
    if (!validation) return [];
    return validation.getFieldRules(props.fieldName, props.step);
});
</script>