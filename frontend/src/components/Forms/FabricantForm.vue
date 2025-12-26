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
                        <v-text-field 
                            v-model="fabricant.nom" 
                            label="Nom du fabricant *" 
                            outlined 
                            dense 
                            :error="submitted && !fabricant.nom.trim()" 
                            :error-messages="submitted && !fabricant.nom.trim() ? 'Le nom du fabricant est requis' : ''" 
                        />
                    </v-col>

                    <v-col cols="12" md="6">
                        <v-text-field 
                            v-model="fabricant.email" 
                            label="Email" 
                            outlined 
                            dense 
                            :error="submitted && fabricant.email && !isValidEmail(fabricant.email)"
                            :error-messages="submitted && fabricant.email && !isValidEmail(fabricant.email) ? 'Email invalide' : ''"
                        />
                    </v-col>
                </v-row>

                <v-row dense>
                    <v-col cols="6">
                        <v-text-field 
                            v-model="fabricant.numTelephone" 
                            label="Téléphone" 
                            outlined 
                            dense 
                            :error="submitted && fabricant.numTelephone && !isValidPhone(fabricant.numTelephone)"
                            :error-messages="submitted && fabricant.numTelephone && !isValidPhone(fabricant.numTelephone) ? 'Téléphone invalide' : ''"
                        />
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
                        <v-text-field 
                            v-model="adresse.numero" 
                            label="N°" 
                            outlined 
                            dense 
                            :error="submitted && adresse.numero && adresse.numero.trim().length < 1"
                            :error-messages="submitted && adresse.numero && adresse.numero.trim().length < 1 ? 'Le numéro doit contenir au moins 1 caractère' : ''"
                        />
                    </v-col>

                    <v-col cols="8">
                        <v-text-field 
                            v-model="adresse.rue" 
                            label="Rue" 
                            outlined 
                            dense 
                            :error="submitted && adresse.rue && adresse.rue.trim().length < 2"
                            :error-messages="submitted && adresse.rue && adresse.rue.trim().length < 2 ? 'La rue doit contenir au moins 2 caractères' : ''"
                        />
                    </v-col>
                </v-row>

                <v-row dense>
                    <v-col cols="6">
                        <v-text-field 
                            v-model="adresse.ville" 
                            label="Ville" 
                            outlined 
                            dense 
                            :error="submitted && adresse.ville && adresse.ville.trim().length < 2"
                            :error-messages="submitted && adresse.ville && adresse.ville.trim().length < 2 ? 'La ville doit contenir au moins 2 caractères' : ''"
                        />
                    </v-col>

                    <v-col cols="6">
                        <v-text-field 
                            v-model="adresse.code_postal" 
                            label="Code postal" 
                            outlined 
                            dense 
                            :error="submitted && adresse.code_postal && !isValidPostalCode(adresse.code_postal)"
                            :error-messages="submitted && adresse.code_postal && !isValidPostalCode(adresse.code_postal) ? 'Code postal invalide' : ''"
                        />
                    </v-col>
                </v-row>

                <v-row dense>
                    <v-col cols="12">
                        <v-text-field 
                            v-model="adresse.pays" 
                            label="Pays" 
                            outlined 
                            dense 
                            :error="submitted && adresse.pays && adresse.pays.trim().length < 2"
                            :error-messages="submitted && adresse.pays && adresse.pays.trim().length < 2 ? 'Le pays doit contenir au moins 2 caractères' : ''"
                        />
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

const emit = defineEmits(['close', 'created'])
const submitted = ref(false)

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

// Fonctions de validation
const isValidEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

const isValidPhone = (phone) => {
    return /^\+?[0-9\s\-()]{7,15}$/.test(phone)
}

const isValidPostalCode = (code) => {
    return /^[0-9]{4,6}$/.test(code.replace(/\s/g, ''))
}

const close = () => {
    emit('close')
}

const validateForm = () => {
    // Fabricant - nom obligatoire
    if (!fabricant.value.nom.trim()) {
        return false
    }
    
    // Email optionnel mais doit être valide si renseigné
    if (fabricant.value.email && !isValidEmail(fabricant.value.email)) {
        return false
    }
    
    // Téléphone optionnel mais doit être valide si renseigné
    if (fabricant.value.numTelephone && !isValidPhone(fabricant.value.numTelephone)) {
        return false
    }

    // Adresse - tous les champs sont optionnels mais doivent être valides si renseignés
    if( adresse.value.numero && isNaN(adresse.value.numero)) {
        return false
    }
    if (adresse.value.code_postal && !isValidPostalCode(adresse.value.code_postal)) {
        return false
    }
    
    if (adresse.value.pays && adresse.value.pays.trim().length < 2) {
        return false
    }
    
    if (adresse.value.ville && adresse.value.ville.trim().length < 2) {
        return false
    }
    
    if (adresse.value.rue && adresse.value.rue.trim().length < 2) {
        return false
    }
    
    return true
}

const save = async () => {
    submitted.value = true

    if (!validateForm()) return

    const api = useApi(API_BASE_URL);

    api.post('fabricants/', {
        ...fabricant.value,
        adresse: adresse.value
    })
        .then(response => {
            const newFabricant = {
                id: response.id,
                nom: response.nom  // Utilisez response.nom pour être cohérent
            };
            emit('created', newFabricant);
            emit('close');
        })
        .catch(error => {
            console.error('Erreur lors de la création du fabricant:', error);
        });
}
</script>