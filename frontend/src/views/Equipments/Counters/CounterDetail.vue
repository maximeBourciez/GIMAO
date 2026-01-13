<template>
    <v-card>
        <!-- Titre -->
        <v-card-title class="d-flex align-center">
            <span>Détails du compteur</span>
        </v-card-title>

        <v-card-text v-if="!loading && counter">

            <!-- Informations générales -->
            <v-sheet class="pa-4 mb-4" elevation="1" rounded>
                <h4 class="mb-3">Informations générales</h4>

                <v-row dense>
                    <v-col cols="12" md="4">
                        <strong>Nom :</strong>
                        <div>{{ counter.nom }}</div>
                    </v-col>

                    <v-col cols="12" md="4">
                        <strong>Description :</strong>
                        <div>{{ counter.description || '—' }}</div>
                    </v-col>

                    <v-col cols="12" md="4">
                        <strong>Dernière intervention</strong>
                        <div>{{ counter.derniereIntervention }}</div>
                    </v-col>
                </v-row>

                <v-row dense>
                    <v-col cols="4">
                        <strong>Intervalle entre les interventions:</strong>
                        <div>{{ counter.intervalle }}</div>
                    </v-col>

                    <v-col cols="4">
                        <strong>Unité :</strong>
                        <div>{{ counter.unite }}</div>
                    </v-col>

                    <v-col cols="4">
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

                <strong>Une maintenance nécessite :</strong>
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

                <v-divider class="mt-3"></v-divider>

                <!-- Consommables -->
                <h4 class="my-3">Consommables</h4>

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

                <v-divider class="mt-3"></v-divider>

                <!-- Documents -->
                <h4 class="my-3">Documents</h4>

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
            <v-btn color="primary" @click="showEditForm">
                Modifier
            </v-btn>
        </v-card-actions>
    </v-card>

    <v-dialog v-model="showCounterDialog" max-width="1000px" @click:outside="closeCounterDialog">
        <v-card>
            <v-card-title>Modifier le compteur</v-card-title>
            <v-card-text>
                <CounterInlineForm v-model="counter" :existingPMs="existingPMs" :typesPM="typesPM"
                    :consumables="consumables" :typesDocuments="typesDocuments" @save="saveCurrentCounter"
                    @cancel="closeCounterDialog" />
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApi } from '@/composables/useApi'
import { API_BASE_URL, MEDIA_BASE_URL } from '@/utils/constants'
import CounterInlineForm from '@/components/Forms/CounterInlineForm.vue'

const route = useRoute();
const router = useRouter();
const counterId = Number(route.params.id);

const counter = ref(null)
const originalCounter = ref(null)

const consumables = ref([])
const typesPM = ref([])
const typesDocuments = ref([])
const existingPMs = ref([])

const loading = ref(true)
const errorMessage = ref('')
const successMessage = ref('')

const api = useApi(API_BASE_URL)

const getFileName = (path) => path?.split('/').pop() || '—'

const getPMTypeLabel = (id) => {
    return typesPM.value.find(t => t.id === id)?.libelle || '—'
}

const getConsumableLabel = (id) => {
    return consumables.value.find(c => c.id === id)?.designation || '—'
}
const getDocumentTypeLabel = (id) => {
    return typesDocuments.value.find(t => t.id === id)?.nomTypeDocument || '—'
}

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

const fetchPMFiles = async () => {
    try {
        const fetchPromises = [];

        counter.value.planMaintenance?.documents.forEach(doc => {
            if (doc.path) {
                const promise = fetch(MEDIA_BASE_URL + doc.path)
                    .then(res => res.blob())
                    .then(blob => {
                        const filename = doc.titre || 'document';
                        const file = new File([blob], filename, { type: blob.type });
                        doc.file = file;
                        return file;
                    })
                    .catch(err => {
                        console.error(`Erreur pour ${doc.path}:`, err);
                    });

                fetchPromises.push(promise);
            }
        });

        await Promise.all(fetchPromises);

    } catch (error) {
        console.error('Erreur lors du chargement des documents:', error);
    }
};

const loadPage = async () => {
    loading.value = true
    errorMessage.value = ''

    try {
        if (!counterId) {
            throw new Error('Identifiant compteur invalide')
        }

        await Promise.all([
            fetchCounter(),
            fetchReferentials(),
        ])
    } catch (e) {
        console.error(e)
        errorMessage.value = e.message || 'Erreur lors du chargement'
    } finally {
        loading.value = false
    }
}


onMounted(async () => {
    await loadPage();
    fetchPMFiles();
});

const showCounterDialog = ref(false)

const showEditForm = () => {
    originalCounter.value = replicateCounter();
    showCounterDialog.value = true
}

const closeCounterDialog = () => {
    showCounterDialog.value = false
}

const saveCurrentCounter = async () => {
    closeCounterDialog();

    const { hasChanges, changes } = detectChanges();

    if (!hasChanges) {
        errorMessage.value = 'Aucune modification détectée';
        return;
    }

    loading.value = true;
    errorMessage.value = '';

    try {
        const fd = new FormData();

        const counterCopy = JSON.parse(JSON.stringify(counter.value));

        counterCopy.planMaintenance.documents.forEach((doc, index) => {
            doc.index = index;
        });

        fd.append('compteur', JSON.stringify(counterCopy));
        fd.append('changes', JSON.stringify(changes));

        const pmDocsChanged = changes['planMaintenance.documents'].modifications;
        pmDocsChanged.forEach((doc, index) => {
            if (doc.nouvelle) {
                fd.append(`file_planMaintenance.documents_${doc.nouvelle.id}`, doc.nouvelle.file);
            }
        })

        const pmDocsAdded = changes['planMaintenance.documents'].ajouts;
        pmDocsAdded.forEach((doc, index) => {
            if (doc.file) {
                fd.append(`file_planMaintenance.documents_${index}`, doc.file);
            }
        });

        await api.put(`compteurs/${counter.value.id}/`, fd, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });

        successMessage.value = 'Compteur modifié avec succès';
        setTimeout(() => router.back(), 1500);

    } catch (e) {
        console.error('Erreur lors de la modification du compteur:', e);
        errorMessage.value = 'Erreur lors de la modification du compteur';

        if (e.response?.data) {
            const errors = Object.entries(e.response.data)
                .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
                .join('\n');
            errorMessage.value += `\n${errors}`;
        }

    } finally {
        loading.value = false;
    }
};

function detectChanges() {
    let changes = {};
    let hasChanges = false;

    const fieldsToCheck = ['nom', 'description', 'intervalle', 'unite', 'valeurCourante', 'estGlissant', 'estPrincipal', 'habElec', 'permisFeu'];

    for (let key of fieldsToCheck) {
        if (counter.value[key] !== originalCounter.value[key]) {
            changes[key] = { ancienne: originalCounter.value[key], nouvelle: counter.value[key] };
            hasChanges = true;
        }
    }

    // Plan de maintenance
    if (counter.value.planMaintenance && originalCounter.value.planMaintenance) {
        const PMFieldsToCheck = ['nom', 'type'];
        for (let key of PMFieldsToCheck) {
            if (counter.value.planMaintenance[key] !== originalCounter.value.planMaintenance[key]) {
                changes[`planMaintenance.${key}`] = { ancienne: originalCounter.value.planMaintenance[key], nouvelle: counter.value.planMaintenance[key] };
                hasChanges = true;
            }
        }

        // Consommables
        const currentConsommables = JSON.stringify(counter.value.planMaintenance.consommables || []);
        const originalConsommables = JSON.stringify(originalCounter.value.planMaintenance.consommables || []);
        if (currentConsommables !== originalConsommables) {
            changes['planMaintenance.consommables'] = { ancienne: originalCounter.value.planMaintenance.consommables || [], nouvelle: counter.value.planMaintenance.consommables || [] };
            hasChanges = true;
        }

        const currentDocs = counter.value.planMaintenance.documents || [];
        const originalDocs = originalCounter.value.planMaintenance.documents || [];

        if (!changes['planMaintenance.documents']) {
            changes['planMaintenance.documents'] = {
                ajouts: [],
                modifications: [],
                suppressions: []
            };
        }

        const deletedDocsIds = originalDocs
            .filter(orig => !currentDocs.find(curr => curr.id === orig.id))
            .map(d => d.id);

        if (deletedDocsIds.length > 0) {
            changes['planMaintenance.documents'].suppressions.push(...deletedDocsIds);
            hasChanges = true;
        }

        for (let i = 0; i < currentDocs.length; i++) {
            const docStr = JSON.stringify({ titre: currentDocs[i].titre, type: currentDocs[i].type });
            const originalDocStr = JSON.stringify({ titre: originalDocs[i]?.titre, type: originalDocs[i]?.type });

            if (!currentDocs[i].id && originalDocs[i] === undefined) {
                changes['planMaintenance.documents'].ajouts.push(currentDocs[i]);
                hasChanges = true;
            }
            else if (docStr !== originalDocStr) {
                changes['planMaintenance.documents'].modifications.push({ ancienne: originalDocs[i], nouvelle: currentDocs[i] });
                hasChanges = true;
            }

            else if (currentDocs[i].file && originalDocs[i].file) {
                if (currentDocs[i].file.name !== originalDocs[i].file.name ||
                    currentDocs[i].file.size !== originalDocs[i].file.size ||
                    currentDocs[i].file.type !== originalDocs[i].file.type) {
                    changes['planMaintenance.documents'].modifications.push({ ancienne: originalDocs[i], nouvelle: currentDocs[i] });
                    hasChanges = true;
                }
            }
            else if ((!originalDocs[i].file && originalDocs[i].file === undefined) && currentDocs[i].file) {
                changes['planMaintenance.documents'].ajouts.push(currentDocs[i]);
                hasChanges = true;
            }
        }

    }

    return { hasChanges, changes };
}


const replicateCounter = () => {
    const ogCounter = {
        ...counter.value,
        planMaintenance: {
            ...counter.value.planMaintenance,
            consommables: counter.value.planMaintenance.consommables
                .filter(c => c.consommable)
                .map(c => ({ ...c })),
            documents: counter.value.planMaintenance.documents
                .filter(d => d.titre || d.file)
                .map(d => ({
                    titre: d.titre,
                    type: d.type,
                    file: d.file
                }))
        }
    };

    return ogCounter;
}
</script>
