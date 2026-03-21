<template>
    <v-container fluid class="calendar-container pa-4">
        <v-card class="pa-4 elevation-2 rounded-lg">

            <!-- Loader -->
            <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-2" />

            <!-- Tabs -->
            <v-tabs v-model="mode" class="mb-4" color="primary" grow @update:modelValue="handleNewMode">
                <v-tab value="bt" class="text-none font-weight-medium">
                    <v-icon start>mdi-wrench</v-icon>
                    Bons de Travail
                </v-tab>

                <v-tab value="maintenance" class="text-none font-weight-medium">
                    <v-icon start>mdi-calendar-refresh</v-icon>
                    Maintenance Préventive
                </v-tab>
            </v-tabs>

            <!-- Calendrier -->
            <div class="calendar-wrapper">
                <vue-cal ref="vuecal" :events="currentEvents" :time-from="7 * 60" :time-to="20 * 60" :time-step="30"
                    active-view="month" locale="fr" :first-day-of-week="2" :on-event-click="onEventClick"
                    :max-events-per-cell="3" events-on-month-view="short" :today-button="true"
                    :click-to-navigate="false" show-week-numbers :time-cell-height="48" class="vuecal--custom"
                    @view-change="({ view }) => currentView = view">
                    <template #event="{ event }" >
                        <!-- Vue mois : compact -->
                        <template v-if="currentView === 'month'"  :style="{ backgroundColor: event.backgroundColor, color: event.color, borderLeftColor: event.backgroundColor }">
                            <div class="event-content d-flex align-center gap-1">
                                <span class="event-title">{{ event.title }}</span>
                            </div>
                        </template>

                        <!-- Vue semaine / jour : détaillé -->
                        <template v-else>
                            <div class="event-content d-flex flex-column" :style="{ backgroundColor: event.backgroundColor, color: event.color }">
                                <span class="event-title font-weight-medium">{{ event.title }}</span>

                                <span v-if="event.start && event.end" class="event-time">
                                    {{ new Date(event.start).toLocaleTimeString([], {
                                        day: '2-digit', month: '2-digit',
                                        hour: '2-digit', minute: '2-digit'
                                    }) }}
                                    -
                                    {{ new Date(event.end).toLocaleTimeString([], {
                                        day: '2-digit', month: '2-digit', hour:
                                            '2-digit', minute: '2-digit'
                                    }) }}
                                </span>

                                <span v-if="event.equipement" class="event-equipement">
                                    <v-icon size="12">mdi-cog</v-icon>
                                    {{ event.equipement.nom }}
                                </span>

                                <span v-if="event.techniciens?.length" class="event-techniciens">
                                    <span v-if="currentView === 'week'">
                                        <v-icon size="12">mdi-account</v-icon>
                                        {{ event.techniciens.length > 1
                                            ? event.techniciens.length + ' techniciens'
                                            : event.techniciens[0].nom }}
                                    </span>

                                    <span v-else class="d-flex align-center gap-1">
                                        <v-icon size="12">mdi-account</v-icon>
                                        <span v-for="(t, i) in event.techniciens" :key="t.id">
                                            {{ t.nom }}<span v-if="i < event.techniciens.length - 1">, </span>
                                        </span>
                                    </span>
                                </span>
                            </div>
                        </template>
                    </template>
                </vue-cal>
            </div>

            <!-- Message si aucun event -->
            <v-alert v-if="!loading && currentEvents.length === 0" type="info" variant="tonal" class="mt-4">
                Aucun événement à afficher
            </v-alert>
        </v-card>
    </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import VueCal from 'vue-cal'
import { API_BASE_URL } from '@/utils/constants'
import { useApi } from '@/composables/useApi'
import { useRouter } from 'vue-router'
import 'vue-cal/dist/vuecal.css'

const api = useApi(API_BASE_URL);
const router = useRouter();

const currentView = ref('month')

const technicienColors = new Map()
const COLORS = [
    '#E53935', '#8E24AA', '#1E88E5', '#00897B',
    '#F4511E', '#6D4C41', '#039BE5', '#43A047',
    '#FB8C00', '#3949AB', '#00ACC1', '#7CB342',
]

const getColorForTechnicien = (id) => {
    if (!technicienColors.has(id)) {
        technicienColors.set(id, COLORS[technicienColors.size % COLORS.length])
    }
    return technicienColors.get(id)
}

/**
 * Mode actif
 */
const mode = ref('bt')

/**
 * Donnees
 */
const eventsBT = ref([])
const eventsMaintenance = ref([])

/**
 * Cache (evite re-fetch)
 */
const loadedBT = ref(false)
const loadedMaintenance = ref(false)

/**
 * Loading
 */
const loading = ref(false)

const fetchBT = async () => {
    loading.value = true
    try {
        const res = await api.get('bons-travail/calendar/')
        const data = res.data ?? res  // selon ce que retourne useApi

        eventsBT.value = (data || []).map(e => {
            const start = e.start || e.date_prevue
            const end = e.end && e.end !== e.start
                ? e.end
                : new Date(new Date(start).getTime() + 60 * 60 * 1000).toISOString()
            const firstTechId = e.techniciens?.[0]?.id ?? null
            const color = firstTechId ? getColorForTechnicien(firstTechId) : '#E53935'

            return {
                id: e.id,
                title: e.nom || 'BT',
                start: toVueCalDate(start),
                end: toVueCalDate(end),
                equipement: e.equipement ? {
                    id: e.equipement.id,
                    nom: e.equipement.nom
                } : null,
                techniciens: (e.techniciens || []).map(t => ({
                    id: t.id,
                    nom: t.nom
                })),
                class: 'event-bt',
                route: { name: 'InterventionDetail', params: { id: e.id } },
                backgroundColor: color,
                color: '#fff',
            }
        })

        loadedBT.value = true
    } catch (e) {
        console.error('Erreur BT', e)
        eventsBT.value = []
    } finally {
        loading.value = false
    }
}

/**
 * API Maintenance
 */
const fetchMaintenance = async () => {
    loading.value = true
    try {
        const res = await api.get('maintenance/calendar/')
        const data = res.data

        eventsMaintenance.value = (data || []).map(e => ({
            id: e.id,
            title: e.title || 'Maintenance',
            start: e.start || e.date_prevue,
            end: e.end || e.date_prevue,
            class: 'event-mp'
        }))

        loadedMaintenance.value = true
    } catch (e) {
        console.error('Erreur Maintenance', e)
        eventsMaintenance.value = []
    } finally {
        loading.value = false
    }
}

/**
 * Chargement intelligent
 */
const loadDataIfNeeded = async () => {
    if (mode.value === 'bt' && !loadedBT.value) {
        console.log("BT")
        await fetchBT()
    }

    if (mode.value === 'maintenance' && !loadedMaintenance.value) {
        console.log("Maintenance")
        await fetchMaintenance()
    }
}

/**
 * Changement d’onglet
 */
const handleNewMode = async () => {
    await loadDataIfNeeded()
}

/**
 * Events affiches
 */
const currentEvents = computed(() => {
    return mode.value === 'bt'
        ? eventsBT.value
        : eventsMaintenance.value
})

/**
 * Click event
 */
const onEventClick = (event, e) => {
    e.stopPropagation()
    if (event.route) {
        console.log('Navigating to:', event.route)
        router.push({ name: 'InterventionDetail', params: { id: event.id } })
    }
}

const toVueCalDate = (iso) => iso ? iso.replace('T', ' ').substring(0, 16) : null


/**
 * Initialisation
 */
onMounted(() => {
    loadDataIfNeeded();
})
</script>

<style scoped>
.calendar-container {
    background: rgb(var(--v-theme-background)) !important;
    min-height: 100vh;
}

.calendar-wrapper {
    background: rgb(var(--v-theme-surface));
    border-radius: 12px;
    overflow: hidden;
}

/* ─── Variables de base ─────────────────────────────────────── */
:deep(.vuecal--custom) {
    /* Couleurs remapées sur les tokens Vuetify */
    --vc-primary: rgb(var(--v-theme-primary));
    --vc-surface: rgb(var(--v-theme-surface));
    --vc-on-surface: rgb(var(--v-theme-on-surface));
    --vc-border: rgba(var(--v-border-color), var(--v-border-opacity));

    font-family: 'Roboto', sans-serif;
    background: var(--vc-surface);
    border: none;
    height: auto;
    min-height: 600px;
}

/* ─── En-têtes jours ────────────────────────────────────────── */
:deep(.vuecal--custom .vuecal__heading) {
    background: var(--vc-primary);
    color: rgb(var(--v-theme-on-primary));
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 12px 0;
    border: none;
}

/* ─── Titre mois / période ──────────────────────────────────── */
:deep(.vuecal--custom .vuecal__title) {
    color: var(--vc-on-surface);
    font-size: 1.4rem;
    font-weight: 500;
    text-transform: capitalize;
    background: none;
    border: none;
}

:deep(.vuecal--custom .vuecal__title-bar) {
    background: var(--vc-surface);
    border-bottom: 1px solid var(--vc-border);
    padding: 12px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* ─── Boutons navigation ────────────────────────────────────── */
:deep(.vuecal--custom .vuecal__arrow),
:deep(.vuecal--custom .vuecal__today-btn),
:deep(.vuecal--custom .vuecal__view-btn) {
    background: var(--vc-primary);
    color: rgb(var(--v-theme-on-primary));
    border: none;
    border-radius: 8px;
    padding: 6px 14px;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: filter 0.15s ease, transform 0.15s ease;
}

:deep(.vuecal--custom .vuecal__arrow:hover),
:deep(.vuecal--custom .vuecal__today-btn:hover),
:deep(.vuecal--custom .vuecal__view-btn:hover) {
    filter: brightness(1.12);
    transform: translateY(-1px);
}

:deep(.vuecal--custom .vuecal__view-btn--active) {
    filter: brightness(0.85);
}

/* ─── Cellules de jours ─────────────────────────────────────── */
:deep(.vuecal--custom .vuecal__cell) {
    border: 1px solid var(--vc-border);
    background: var(--vc-surface);
    transition: background-color 0.15s ease;
    min-height: 80px;
}

:deep(.vuecal--custom .vuecal__cell:hover) {
    background: rgba(var(--v-theme-primary), 0.04);
}

/* Week-end */
:deep(.vuecal--custom .vuecal__cell--weekend) {
    background: rgba(var(--v-theme-on-surface), 0.02);
}

/* Jour actuel */
:deep(.vuecal--custom .vuecal__cell--today) {
    background: rgba(var(--v-theme-primary), 0.08) !important;
}

:deep(.vuecal--custom .vuecal__cell-date .today) {
    background: var(--vc-primary);
    color: rgb(var(--v-theme-on-primary));
    border-radius: 50%;
    width: 28px;
    height: 28px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
}

/* Jours hors mois courant */
:deep(.vuecal--custom .vuecal__cell--out-of-scope) {
    opacity: 0.45;
}

/* Numéros de jours */
:deep(.vuecal--custom .vuecal__cell-date) {
    color: var(--vc-on-surface);
    font-weight: 500;
    font-size: 0.9rem;
    padding: 6px 8px;
}

/* ─── Événements ────────────────────────────────────────────── */
:deep(.vuecal--custom .vuecal__event) {
    border-radius: 6px;
    padding: 3px 8px;
    margin: 2px 3px;
    font-size: 0.8rem;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: transform 0.15s ease, filter 0.15s ease;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    line-height: 1.4;
}

:deep(.vuecal--custom .vuecal__event:hover) {
    transform: translateY(-1px);
    filter: brightness(1.08);
}

/* Classe Bons de Travail */
:deep(.vuecal--custom .vuecal__event.event-bt) {
    color: rgb(var(--v-theme-on-primary));
    border-left: 3px solid rgba(0, 0, 0, 0.25);
}

/* Classe Maintenance Préventive */
:deep(.vuecal--custom .vuecal__event.event-mp) {
    background: #E53935;
    color: #ffffff;
    border-left: 3px solid #B71C1C;
}

:deep(.vuecal--custom .vuecal__event-title) {
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

:deep(.vuecal--custom .vuecal__event-time) {
    font-size: 0.75rem;
    opacity: 0.85;
    margin-right: 4px;
}

/* ─── Slots horaires (vue semaine/jour) ─────────────────────── */
:deep(.vuecal--custom .vuecal__time-cell) {
    color: var(--vc-on-surface);
    font-size: 0.8rem;
    font-weight: 500;
    border-right: 1px solid var(--vc-border);
}

:deep(.vuecal--custom .vuecal__time-cell-line) {
    border-color: var(--vc-border);
}

/* Indicateur "maintenant" */
:deep(.vuecal--custom .vuecal__now-line) {
    border-color: var(--vc-primary);
    border-width: 2px;
}

/* ─── Responsive ─────────────────────────────────────────────── */
@media (max-width: 768px) {
    :deep(.vuecal--custom .vuecal__title-bar) {
        flex-wrap: wrap;
        gap: 8px;
        padding: 8px 10px;
    }

    :deep(.vuecal--custom .vuecal__title) {
        font-size: 1.1rem;
    }

    :deep(.vuecal--custom .vuecal__arrow),
    :deep(.vuecal--custom .vuecal__today-btn),
    :deep(.vuecal--custom .vuecal__view-btn) {
        padding: 4px 10px;
        font-size: 0.8rem;
    }

    :deep(.vuecal--custom .vuecal__event) {
        font-size: 0.72rem;
        padding: 2px 4px;
    }

    :deep(.vuecal--custom .vuecal__cell) {
        min-height: 56px;
    }
}
</style>
