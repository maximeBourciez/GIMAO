<template>
    <v-card>
        <v-card-title class="text-h6">
            Ajouter un fabricant
        </v-card-title>

        <v-card-text>
            <!-- Infos fabricant -->
            <v-sheet class="pa-4 mb-4" elevation="1" rounded>
                <h4 class="mb-3">Fabricant</h4>

                <v-row dense>
                    <v-col cols="12" md="6">
                        <v-text-field v-model="fabricant.nom" label="Nom du fabricant *" outlined dense />
                    </v-col>

                    <v-col cols="12" md="6">
                        <v-text-field v-model="fabricant.email" label="Email" outlined dense />
                    </v-col>
                </v-row>

                <v-row dense>
                    <v-col cols="6">
                        <v-text-field v-model="fabricant.numTelephone" label="Téléphone" outlined dense />
                    </v-col>

                    <v-col cols="6" class="d-flex align-center">
                        <v-checkbox v-model="fabricant.serviceApresVente" label="Service après-vente" dense />
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

const props = defineProps({
    modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'created'])

const open = ref(props.modelValue)

const fabricant = ref({
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
    emit('update:modelValue', false)
}

const save = async () => {
    if (!fabricant.value.nom.trim()) return

    const payload = {
        ...fabricant.value,
        adresse: adresse.value
    }

    emit('created', payload)
    close()
}
</script>
