<template>
    <v-card>
        <v-card-title class="text-h6">
            {{ isEditMode ? 'Modifier le fournisseur' : 'Ajouter un fournisseur' }}
        </v-card-title>
        <v-card-text>
            <!-- Infos fournisseur -->
            <v-sheet class="pa-4 mb-4" elevation="1" rounded>
                <h4 class="mb-3">Fournisseur</h4>
                <v-row dense>
                    <v-col cols="12" md="6">
                        <v-text-field v-model="fournisseur.nom" label="Nom du fournisseur *" outlined dense
                            :error="submitted && !fournisseur.nom.trim()"
                            :error-messages="submitted && !fournisseur.nom.trim() ? 'Le nom du fournisseur est requis' : ''" />
                    </v-col>
                    <v-col cols="12" md="6">
                        <v-text-field v-model="fournisseur.email" label="Email" outlined dense
                            :error="submitted && fournisseur.email && !isValidEmail(fournisseur.email)"
                            :error-messages="submitted && fournisseur.email && !isValidEmail(fournisseur.email) ? 'Email invalide' : ''" />
                    </v-col>
                </v-row>
                <v-row dense>
                    <v-col cols="6">
                        <v-text-field v-model="fournisseur.numTelephone" label="Téléphone" outlined dense
                            :error="submitted && fournisseur.numTelephone && !isValidPhone(fournisseur.numTelephone)"
                            :error-messages="submitted && fournisseur.numTelephone && !isValidPhone(fournisseur.numTelephone) ? 'Téléphone invalide' : ''" />
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
                        <v-text-field v-model="adresse.rue" label="Rue" outlined dense
                            :error="submitted && adresse.rue && adresse.rue.trim().length < 2"
                            :error-messages="submitted && adresse.rue && adresse.rue.trim().length < 2 ? 'La rue doit contenir au moins 2 caractères' : ''" />
                    </v-col>
                </v-row>
                <v-row dense>
                    <v-col cols="6">
                        <v-text-field v-model="adresse.ville" label="Ville" outlined dense
                            :error="submitted && adresse.ville && adresse.ville.trim().length < 2"
                            :error-messages="submitted && adresse.ville && adresse.ville.trim().length < 2 ? 'La ville doit contenir au moins 2 caractères' : ''" />
                    </v-col>
                    <v-col cols="6">
                        <v-text-field v-model="adresse.code_postal" label="Code postal" outlined dense
                            :error="submitted && adresse.code_postal && !isValidPostalCode(adresse.code_postal)"
                            :error-messages="submitted && adresse.code_postal && !isValidPostalCode(adresse.code_postal) ? 'Code postal invalide' : ''" />
                    </v-col>
                </v-row>
                <v-row dense>
                    <v-col cols="12">
                        <v-text-field v-model="adresse.pays" label="Pays" outlined dense
                            :error="submitted && adresse.pays && adresse.pays.trim().length < 2"
                            :error-messages="submitted && adresse.pays && adresse.pays.trim().length < 2 ? 'Le pays doit contenir au moins 2 caractères' : ''" />
                    </v-col>
                </v-row>
                <v-text-field v-model="adresse.complement" label="Complément" outlined dense />
            </v-sheet>
        </v-card-text>
        <v-card-actions>
            <v-spacer />
            <v-btn text @click="close">Annuler</v-btn>
            <v-btn color="primary" @click="save">
                {{ isEditMode ? 'Enregistrer les modifications' : 'Créer le fournisseur' }}
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const api = useApi(API_BASE_URL);

const props = defineProps({
    supplier: {
        type: Object,
        default: null
    }
})

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

const supplierId = computed(() => props.supplier?.id)
const isEditMode = computed(() => !!supplierId.value)





const emit = defineEmits(['created', 'close'])
const submitted = ref(false)



// Fonctions de validation
const isValidEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

const isValidPhone = (phone) => {
    return /^\+?[0-9\s\-()]{7,15}$/.test(phone)
}

const isValidPostalCode = (code) => {
    // Accepte les codes français (5 chiffres) ou autres formats
    return /^[0-9]{4,6}$/.test(code.replace(/\s/g, ''))
}

const close = () => {
    emit('close')
}

const validateForm = () => {
    // Fournisseur - nom obligatoire
    if (!fournisseur.value.nom.trim()) {
        return false
    }

    // Email optionnel mais doit être valide si renseigné
    if (fournisseur.value.email && !isValidEmail(fournisseur.value.email)) {
        return false
    }

    // Téléphone optionnel mais doit être valide si renseigné
    if (fournisseur.value.numTelephone && !isValidPhone(fournisseur.value.numTelephone)) {
        return false
    }

    // Adresse - tous les champs sont optionnels mais doivent être valides si renseignés
    if (adresse.value.code_postal && !isValidPostalCode(adresse.value.code_postal)) {
        return false
    }

    if (adresse.value.pays && adresse.value.pays.trim().length < 2) {
        return false
    }

    if (adresse.value.ville && adresse.value.ville.trim().length < 2) {
        return false
    }

    if (adresse.value.numero && isNaN(adresse.value.numero)) {
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

    const payload = {
        ...fournisseur.value,
        adresse: adresse.value
    }

    try {
        let response

        if (isEditMode.value) {
            response = await api.put(`fournisseurs/${supplierId.value}/`, payload)
        } else {
            response = await api.post('fournisseurs/', payload)
        }

        emit('created', response)
        emit('close')

    } catch (error) {
        console.error('Erreur lors de l’enregistrement du fournisseur:', error)
    }
}

</script>