<template>
    <v-card>
        <!-- Titre -->
        <v-card-title class="d-flex align-center">
            <span>Détails du compteur</span>
            <v-spacer />
            <v-btn icon @click="$emit('close')">
                <v-icon>mdi-close</v-icon>
            </v-btn>
        </v-card-title>

        <v-card-text v-if="!loading && counter">

            <!-- Informations générales -->
            <v-sheet class="pa-4 mb-4" elevation="1" rounded>
                <h4 class="mb-3">Informations générales</h4>

                <v-row dense>
                    <v-col cols="12" md="6">
                        <strong>Nom :</strong>
                        <div>{{ counter.nom }}</div>
                    </v-col>

                    <v-col cols="12" md="6">
                        <strong>Description :</strong>
                        <div>{{ counter.description || '—' }}</div>
                    </v-col>
                </v-row>

                <v-row dense>
                    <v-col cols="6">
                        <strong>Intervalle :</strong>
                        <div>{{ counter.intervalle }} {{ counter.unite }}</div>
                    </v-col>

                    <v-col cols="6">
                        <strong>Valeur actuelle :</strong>
                        <div>{{ counter.valeurCourante ?? '—' }}</div>
                    </v-col>
                </v-row>
            </v-sheet>

            <!-- Options -->
            <v-sheet class="pa-4 mb-4" elevation="1" rounded>
                <h4 class="mb-3">Options du compteur</h4>

                <v-row dense>
                    <v-col cols="6">
                        <v-chip :color="counter.estGlissant ? 'green' : 'grey'" label>
                            {{ counter.estGlissant ? 'Compteur glissant' : 'Non glissant' }}
                        </v-chip>
                    </v-col>

                    <v-col cols="6">
                        <v-chip :color="counter.estPrincipal ? 'primary' : 'grey'" label>
                            {{ counter.estPrincipal ? 'Compteur principal' : 'Secondaire' }}
                        </v-chip>
                    </v-col>
                </v-row>

                <v-divider class="my-3" />

                <strong>Maintenance nécessite :</strong>
                <v-row dense class="mt-2">
                    <v-col cols="6">
                        <v-icon left color="success" v-if="counter.habElec">mdi-check</v-icon>
                        <v-icon left color="grey" v-else>mdi-close</v-icon>
                        Habilitation électrique
                    </v-col>

                    <v-col cols="6">
                        <v-icon left color="success" v-if="counter.permisFeu">mdi-check</v-icon>
                        <v-icon left color="grey" v-else>mdi-close</v-icon>
                        Permis feu
                    </v-col>
                </v-row>
            </v-sheet>

            <!-- Plan de maintenance -->
            <v-sheet class="pa-4 mb-4" elevation="1" rounded>
                <h4 class="mb-3">Plan de maintenance</h4>

                <v-row dense>
                    <v-col cols="8">
                        <strong>Nom :</strong>
                        <div>{{ counter.planMaintenance?.nom || '—' }}</div>
                    </v-col>

                    <v-col cols="4">
                        <strong>Type :</strong>
                        <div>{{ getPMTypeLabel(counter.planMaintenance?.type) }}</div>
                    </v-col>
                </v-row>
            </v-sheet>

            <!-- Consommables -->
            <v-sheet class="pa-4 mb-4" elevation="1" rounded>
                <h4 class="mb-3">Consommables</h4>

                <div v-if="!counter.planMaintenance?.consommables?.length">
                    Aucun consommable
                </div>

                <v-row v-for="(c, index) in counter.planMaintenance.consommables" :key="index" dense>
                    <v-col cols="8">
                        {{ getConsumableLabel(c.consommable) }}
                    </v-col>
                    <v-col cols="4">
                        Quantité : {{ c.quantite }}
                    </v-col>
                </v-row>
            </v-sheet>

            <!-- Documents -->
            <v-sheet class="pa-4 mb-2" elevation="1" rounded>
                <h4 class="mb-3">Documents</h4>

                <div v-if="!counter.planMaintenance?.documents?.length">
                    Aucun document
                </div>

                <v-row v-for="(doc, index) in counter.planMaintenance.documents" :key="index" dense class="mb-2">
                    <v-col cols="4">
                        <strong>{{ doc.titre || 'Sans titre' }}</strong>
                    </v-col>

                    <v-col cols="5">
                        {{ getFileName(doc.path) || '—' }}
                    </v-col>

                    <v-col cols="3">
                        {{ getDocumentTypeLabel(doc.type) }}
                    </v-col>
                </v-row>
            </v-sheet>

        </v-card-text>

        <v-card-actions>
            <v-spacer />
            <v-btn color="primary" @click="$emit('edit')">
                Modifier
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApi } from '@/composables/useApi'
import { API_BASE_URL } from '@/utils/constants'

/* ========= ROUTER ========= */
const route = useRoute()
const router = useRouter()
const counterId = Number(route.params.id)

/* ========= STATE ========= */
const counter = ref(null)

const consumables = ref([])
const typesPM = ref([])
const typesDocuments = ref([])

const loading = ref(true)
const errorMessage = ref('')

/* ========= API ========= */
const api = useApi(API_BASE_URL)

/* ========= HELPERS ========= */
const getFileName = (path) => path?.split('/').pop() || '—'

const getPMTypeLabel = (id) =>
    typesPM.value.find(t => t.id === id)?.libelle || '—'

const getConsumableLabel = (id) =>
    consumables.value.find(c => c.id === id)?.designation || '—'

const getDocumentTypeLabel = (id) =>
    typesDocuments.value.find(t => t.id === id)?.nomTypeDocument || '—'

/* ========= FETCH ========= */
const fetchCounter = async () => {
    counter.value = await api.get(`compteurs/${counterId}`)
}

const fetchReferentials = async () => {
    const [cons, pmTypes, docTypes] = await Promise.all([
        api.get('consommables/'),
        api.get('types-plan-maintenance/'),
        api.get('types-documents/')
    ])

    consumables.value = cons
    typesPM.value = pmTypes
    typesDocuments.value = docTypes
}

const loadPage = async () => {
    loading.value = true
    errorMessage.value = ''

    try {
        if (!counterId) {
            throw new Error('Identifiant compteur invalide')
        }

        await Promise.all([
            fetchCounter(),
            fetchReferentials()
        ])
    } catch (e) {
        console.error(e)
        errorMessage.value = e.message || 'Erreur lors du chargement'
    } finally {
        loading.value = false
    }
}

onMounted(loadPage)
</script>
