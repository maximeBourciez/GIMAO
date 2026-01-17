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
defineProps({
    role: {
        type: String,
        default: ''
    }
})

/**
 * Données brutes temporaires
 */

// Technicien
const technicienStats = [
    { label: 'Vos BT', value: 12 },
    { label: 'Vos BT en cours', value: 5 },
    { label: 'Vos BT terminés', value: 7 }
]

// Opérateur
const operateurStats = [
    { label: 'Vos BT', value: 9 },
    { label: 'Vos DI en attente', value: 3 },
    { label: 'Vos DI acceptées', value: 6 }
]

// Responsable
const responsableStats = [
    { label: 'Nombre de DI', value: 24 },
    { label: 'DI en attente', value: 6 },
    { label: 'DI acceptés', value: 18 },
    { label: 'Nombre de BT', value: 42 },
    { label: 'BT en retard', value: 4 },
    { label: 'BT en cours', value: 11 }
]
</script>