<template>
    <v-card>
        <v-card-title>
            Ajouter une famille d’équipement
        </v-card-title>

        <v-card-text>
            <v-row dense>
                <v-col cols="12">
                    <v-text-field v-model="family.nom" label="Nom de la famille *" outlined dense
                        :error="submitted && !family.nom.trim()" :error-messages="submitted && !family.nom.trim() ? 'Le nom de la famille est requis' : ''" />
                </v-col>

                <v-col cols="12">
                    <v-select v-model="family.parent" :items="families" item-title="nom" item-value="id"
                        label="Famille parente (optionnel)" outlined dense clearable />
                </v-col>
            </v-row>
        </v-card-text>

        <v-card-actions>
            <v-spacer />
            <v-btn text @click="$emit('close')">Annuler</v-btn>
            <v-btn color="primary" @click="submit">
                Enregistrer
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script setup>
import { ref } from 'vue'
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const props = defineProps({
    families: {
        type: Array,
        default: () => []
    }
})

const emit = defineEmits(['created', 'close'])

const submitted = ref(false)

const family = ref({
    nom: '',
    parent: null
})

const submit = () => {
    submitted.value = true
    if (!family.value.nom.trim()) return

    const api = useApi(API_BASE_URL);

    api.post('famille-equipements/', family.value)
        .then(response => {
            console.log('Famille créée avec succès:', response);
            const newFamily = {
                id: response.id,
                nom: family.value.nom,
                parent: family.value.parent
            };
            emit('created', newFamily);
            emit('close');
        })
        .catch(error => {
            console.error(error);
        });
}

</script>
