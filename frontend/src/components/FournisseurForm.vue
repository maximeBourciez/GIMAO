<template>
    <v-card>
        <v-card-title class="text-h6">
            Ajouter un fournisseur
        </v-card-title>

        <v-card-text>
            <!-- Infos fournisseur -->
            <v-sheet class="pa-4 mb-4" elevation="1" rounded>
                <h4 class="mb-3">Fournisseur</h4>

                <v-row dense>
                    <v-col cols="12" md="6">
                        <v-text-field v-model="fournisseur.nom" label="Nom du fournisseur *" outlined dense />
                    </v-col>

                    <v-col cols="12" md="6">
                        <v-text-field v-model="fournisseur.email" label="Email" outlined dense />
                    </v-col>
                </v-row>

                <v-row dense>
                    <v-col cols="6">
                        <v-text-field v-model="fournisseur.numTelephone" label="Téléphone" outlined dense />
                    </v-col>

                    <v-col cols="6" class="d-flex align-center">
                        <v-checkbox v-model="fournisseur.serviceApresVente" label="Service après-vente" dense />
                    </v-col>
                </v-row>
            </v-sheet>

            <!-- Adresse -->
            <v-sheet class="pa-4" elevation="1" rounded>
                <h4 class="mb-3">Adresse</h4>

                <v-row dense>
                    <v-col cols="4">
                        <v-text-field v-model="adresse.numero" label="N°" outlined dense />
                    </v-col>

                    <v-col cols="8">
                        <v-text-field v-model="adresse.rue" label="Rue" outlined dense />
                    </v-col>
                </v-row>

                <v-row dense>
                    <v-col cols="6">
                        <v-text-field v-model="adresse.ville" label="Ville" outlined dense />
                    </v-col>

                    <v-col cols="6">
                        <v-text-field v-model="adresse.code_postal" label="Code postal" outlined dense />
                    </v-col>
                </v-row>

                <v-row dense>
                    <v-col cols="12">
                        <v-text-field v-model="adresse.pays" label="Pays" outlined dense />
                    </v-col>
                </v-row>

                <v-text-field v-model="adresse.complement" label="Complément" outlined dense />
            </v-sheet>
        </v-card-text>

        <v-card-actions>
            <v-spacer />
            <v-btn text @click="close">Annuler</v-btn>
            <v-btn color="primary" @click="save">
                Créer
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script setup>
import { ref } from 'vue'
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const props = defineProps({
    modelValue: Boolean
})

const emit = defineEmits(['created', 'close'])

const fournisseur = ref({
    nom: '',
    email: null,
    numTelephone: null,
    serviceApresVente: false
})

const adresse = ref({
    numero: '',
    rue: '',
    ville: '',
    code_postal: '',
    pays: '',
    complement: null
})

const close = () => {
    emit('close')
}

const save = async () => {
    if (!fournisseur.value.nom.trim()) return

    const api = useApi(API_BASE_URL);

    api.post('fournisseurs/', {
        ...fournisseur.value,
        adresse: adresse.value
    })
    .then(response => {
        console.log('Fournisseur créé avec succès:', response);
        const newFournisseur = {
            id: response.id,
            nom: fournisseur.value.nom
        };
        emit('created', newFournisseur);
        emit('close');
    })
    .catch(error => {
        console.error(error);
    });
}
</script>
