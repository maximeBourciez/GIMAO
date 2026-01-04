<template>
    <v-card>
        <v-card-title>
            Ajouter un modèle d’équipement
        </v-card-title>

        <v-card-text>
            <v-row dense>
                <!-- Nom -->
                <v-col cols="12">
                    <v-text-field v-model="modele.nom" label="Nom du modèle *" outlined dense
                        :error="submitted && !modele.nom.trim()" :rules="[v => !!v || 'Le nom du modèle est requis']" />
                </v-col>

                <!-- Fabricant -->
                <v-col cols="12">
                    <v-select v-model="modele.fabricant" :items="fabricants" item-title="nom" return-object
                        label="Fabricant *" outlined dense clearable :rules="[v => !!v || 'Le fabricant est requis']">
                        <template #append-item>
                            <v-divider />
                            <v-list-item class="text-primary" @click="showFabricantModal = true">
                                <v-list-item-title>
                                    <v-icon left size="18">mdi-plus</v-icon>
                                    Ajouter un fabricant
                                </v-list-item-title>
                            </v-list-item>
                        </template>
                    </v-select>
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

        <!-- Modale fabricant -->
        <v-dialog v-model="showFabricantModal" max-width="600">
            <FabricantForm @created="onFabricantCreated" @close="showFabricantModal = false" />
        </v-dialog>
    </v-card>
</template>


<script setup>
import { ref } from 'vue'
import FabricantForm from '@/components/Forms/FabricantForm.vue'
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

// Props 
const props = defineProps({
    fabricants: {
        type: Array,
        required: true
    }
})


// Données
const emit = defineEmits(['created', 'close', 'fabricant-created'])

const submitted = ref(false)
const showFabricantModal = ref(false)

const modele = ref({
    nom: '',
    fabricant: null
})


// Validation du formulaire
const validateForm = () => {
    if(!modele.value.nom.trim()) {
        return false
    }
    if(!modele.value.fabricant) {
        return false
    }
    return true
}

// Soumission du formulaire
const submit = () => {
    if(!validateForm()) {
        submitted.value = true
        return
    }

    if (!modele.value.nom.trim()) return
    if (!modele.value.fabricant) return

    const api = useApi(API_BASE_URL);

    const payload = {
        nom: modele.value.nom,
        fabricant: modele.value.fabricant.id
    }

    console.log('payload : ', payload);

    api.post('modele-equipements/', payload)
        .then(response => {
            const modeleCreated = {
                id: response.id,
                nom: modele.value.nom,
                fabricant: modele.value.fabricant.id
            };
            console.log('Modele transmis : ', modeleCreated);
            emit('created', modeleCreated);
            emit('close');
        })
        .catch(error => {
            console.error(error);
        });
}

// Handler de la création de fabricant
const onFabricantCreated = (newFab) => {
    emit('fabricant-created', newFab)
    modele.value.fabricant = newFab
}



</script>
