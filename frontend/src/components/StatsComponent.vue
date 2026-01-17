<template>
    <v-container fluid class="d-flex justify-center">
        <v-container fluid>

            <!-- ================= RESPONSABLE ================= -->
            <v-row v-if="role === 'Responsable GMAO'" dense>
                <v-col v-for="(stat, index) in responsableStats" :key="index" cols="12" md="4">
                    <v-card elevation="2" class="pa-4">
                        <v-row align="center" justify="space-between">
                            <v-col cols="8">
                                <span class="font-weight-bold">
                                    {{ stat.label }}
                                </span>
                            </v-col>

                            <v-col cols="4" class="text-right">
                                <span class="text-h4 font-weight-bold">
                                    {{ stat.value }}
                                </span>
                            </v-col>
                        </v-row>
                    </v-card>
                </v-col>
            </v-row>

            <!-- ============ TECHNICIEN ================= -->
            <v-row v-else-if="role === 'Technicien'" dense>
                <v-col v-for="(stat, index) in technicienStats" :key="'tech-' + index" cols="12" md="4">
                    <v-card elevation="2" class="pa-4">
                        <v-row align="center" justify="space-between">
                            <v-col cols="8">
                                <span class="font-weight-bold">
                                    {{ stat.label }}
                                </span>
                            </v-col>

                            <v-col cols="4" class="text-right">
                                <span class="text-h4 font-weight-bold">
                                    {{ stat.value }}
                                </span>
                            </v-col>
                        </v-row>
                    </v-card>
                </v-col>
            </v-row>

            <!-- ============ OPERATEUR ================= -->
            <v-row v-else-if="role === 'Opérateur'" dense>
                <v-col v-for="(stat, index) in operateurStats" :key="'op-' + index" cols="12" md="4">
                    <v-card elevation="2" class="pa-4">
                        <v-row align="center" justify="space-between">
                            <v-col cols="8">
                                <span class="font-weight-bold">
                                    {{ stat.label }}
                                </span>
                            </v-col>

                            <v-col cols="4" class="text-right">
                                <span class="text-h4 font-weight-bold">
                                    {{ stat.value }}
                                </span>
                            </v-col>
                        </v-row>
                    </v-card>
                </v-col>
            </v-row>

        </v-container>
    </v-container>
</template>



<script setup>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import { useApi } from '@/composables/useApi.js';
import { API_BASE_URL } from '../utils/constants';

const props = defineProps({
    role: {
        type: String,
        default: ''
    }
})


const store = useStore();
const api = useApi(API_BASE_URL);

// données dynamiques
const technicienStats = ref([]);
const operateurStats = ref([]);
const responsableStats = ref([]);

// Loading / error
const loading = ref(false);
const error = ref(null);

const buildUrl = () => {
    const params = new URLSearchParams();
    params.append('role', props.role);

    // si rôle technicien ou opérateur, on ajoute userId
    if (props.role === 'Technicien' || props.role === 'Opérateur') {
        const userId = store.getters.currentUser.id;
        params.append('userId', userId);
    }

    return `stats/?${params.toString()}`;
}

const fetchStats = async () => {
    console.log('Fetching stats for role:', props.role);
    loading.value = true;
    error.value = null;

    try {
        const url = buildUrl();
        console.log('Fetching stats from URL:', url);
        const response = await api.get(url);

        // exemple de réponse attendue :
        const stats = response.stats;

        if (props.role === 'Responsable GMAO') {
            responsableStats.value = stats;
        } else if (props.role === 'Technicien') {
            technicienStats.value = stats;
        } else if (props.role === 'Opérateur') {
            operateurStats.value = stats;
        }

    } catch (err) {
        error.value = err;
        console.error(err);
    } finally {
        loading.value = false;
    }

    console.log('Fetched stats:', {
        responsableStats: responsableStats.value,
        technicienStats: technicienStats.value,
        operateurStats: operateurStats.value,
    });
}

onMounted(() => {
    fetchStats();
})
</script>
