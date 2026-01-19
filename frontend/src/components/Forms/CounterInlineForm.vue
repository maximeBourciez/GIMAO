<template>
    <v-form @submit.prevent="handleSave">
        <v-row dense>
            <v-col cols="12" md="6">
                <FormField v-model="counter.nom" field-name="nom" label="Nom du compteur"
                    placeholder="Saisir le nom du compteur" counter="100" />
            </v-col>

            <v-col cols="12" md="6">
                <FormField v-model="counter.valeurCourante" field-name="valeurCourante" type="number"
                    label="Valeur actuelle" placeholder="0" min="0" />
            </v-col>

            <v-col cols="12" md="6">
                <FormSelect v-model="counter.unite" field-name="unite" label="Unité" 
                    :items="COUNTER_UNITS" item-title="title" item-value="value" />
            </v-col>

            <v-col cols="12" md="6">
                <FormCheckbox v-model="counter.estPrincipal" field-name="estPrincipal" label="Compteur principal" />
            </v-col>
        </v-row>

        <v-alert v-if="localError" type="error" class="mt-4">{{ localError }}</v-alert>

        <v-card-actions class="px-0 pt-4">
            <v-spacer />
            <v-btn variant="text" @click="handleCancel">Annuler</v-btn>
            <v-btn type="submit" color="primary" :disabled="!isValid">
                {{ isEditMode ? 'Modifier le compteur' : 'Ajouter le compteur' }}
            </v-btn>
        </v-card-actions>
    </v-form>
</template>

<script setup>
import { computed, ref } from 'vue'
import { FormField, FormCheckbox, FormSelect } from '@/components/common'
import { COUNTER_UNITS } from '@/utils/constants'

const props = defineProps({
    modelValue: {
        type: Object,
        required: true
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

const counter = computed({
    get: () => props.modelValue,
    set: v => emit('update:modelValue', v)
})

const isValid = computed(() => {
    return counter.value.nom && counter.value.nom.trim() !== '' && counter.value.unite
})

const handleSave = () => {
    if (!isValid.value) {
        localError.value = 'Veuillez remplir tous les champs obligatoires'
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
