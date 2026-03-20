<template>
    <v-container fluid class="calendar-container pa-4">
        <v-card class="pa-4 elevation-2 rounded-lg">
            <v-tabs
                v-model="mode"
                class="mb-4"
                color="primary"
                grow
            >
                <v-tab value="bt" class="text-none font-weight-medium">
                    <v-icon start>mdi-wrench</v-icon>
                    Bons de Travail
                </v-tab>
                <v-tab value="maintenance" class="text-none font-weight-medium">
                    <v-icon start>mdi-calendar-refresh</v-icon>
                    Maintenance Préventive
                </v-tab>
            </v-tabs>

            <div class="calendar-wrapper">
                <vue-cal
                    ref="vuecal"
                    :events="currentEvents"
                    :time-from="7 * 60"
                    :time-to="20 * 60"
                    :time-step="30"
                    active-view="month"
                    :disable-views="[]"
                    locale="fr"
                    :first-day-of-week="2"
                    :on-event-click="onEventClick"
                    :max-events-per-cell="3"
                    events-on-month-view="short"
                    :today-button="true"
                    :click-to-navigate="false"
                    show-week-numbers
                    :time-cell-height="48"
                    class="vuecal--custom"
                />
            </div>
        </v-card>
    </v-container>
</template>

<script>
import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'

export default {
    name: 'CalendarView',

    components: { VueCal },

    data() {
        return {
            mode: 'bt',

            eventsBT: [
                {
                    title: 'BT #101 - Pompe centrifuge',
                    start: '2026-03-18 00:00',
                    end: '2026-03-18 23:59',
                    class: 'event-bt',
                    id: 101,
                },
                {
                    title: 'BT #102 - Electricité tableau',
                    start: '2026-03-20 08:00',
                    end: '2026-03-20 12:00',
                    class: 'event-bt',
                    id: 102,
                },
                {
                    title: 'BT #103 - Fuite hydraulique',
                    start: '2026-03-20 14:00',
                    end: '2026-03-20 17:00',
                    class: 'event-bt',
                    id: 103,
                },
                {
                    title: 'BT #104 - Remplacement vanne DN100',
                    start: '2026-03-23 07:00',
                    end: '2026-03-25 17:00',
                    class: 'event-bt',
                    id: 104,
                },
                {
                    title: 'BT #105 - Inspection générale',
                    start: '2026-03-26 08:00',
                    end: '2026-03-27 16:00',
                    class: 'event-bt',
                    id: 105,
                },
            ],

            eventsMaintenance: [
                {
                    title: 'MP-201 - Compresseur air',
                    start: '2026-03-25 08:00',
                    end: '2026-03-25 17:00',
                    class: 'event-mp',
                    id: 201,
                },
                {
                    title: 'MP-202 - Climatisation bâtiment A',
                    start: '2026-04-01 08:00',
                    end: '2026-04-01 12:00',
                    class: 'event-mp',
                    id: 202,
                },
                {
                    title: 'MP-203 - Graissage mensuel',
                    start: '2026-03-17 08:00',
                    end: '2026-03-19 17:00',
                    class: 'event-mp',
                    id: 203,
                },
            ],
        }
    },

    computed: {
        currentEvents() {
            return this.mode === 'bt' ? this.eventsBT : this.eventsMaintenance
        },
    },

    methods: {
        onEventClick(event, e) {
            e.stopPropagation()
            // Remplacer par : this.$router.push(`/work-orders/${event.id}`)
            console.log('Navigation vers :', event.id, event.title)
        },
    },
}
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
    --vc-primary:          rgb(var(--v-theme-primary));
    --vc-surface:          rgb(var(--v-theme-surface));
    --vc-on-surface:       rgb(var(--v-theme-on-surface));
    --vc-border:           rgba(var(--v-border-color), var(--v-border-opacity));

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
    background: rgb(var(--v-theme-primary));
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