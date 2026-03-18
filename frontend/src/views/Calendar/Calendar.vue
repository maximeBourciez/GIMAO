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
                <FullCalendar :options="calendarOptions" />
            </div>
        </v-card>
    </v-container>
</template>

<script>
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import frLocale from '@fullcalendar/core/locales/fr'

export default {
    components: { FullCalendar },

    data() {
        return {
            mode: "bt",

            eventsBT: [
                { 
                    title: "🔧 BT #101 - Pompe", 
                    start: "2026-03-18", 
                    color: "#1976D2",
                    extendedProps: { type: 'bt' }
                },
                { 
                    title: "⚡ BT #102 - Électricité", 
                    start: "2026-03-20 08:00", 
                    end: "2026-03-20 12:00", 
                    color: "#1976D2",
                    extendedProps: { type: 'bt' }
                },
                { 
                    title: "⚡ BT #102 - Électricité", 
                    start: "2026-03-20 10:00", 
                    end: "2026-03-20 12:00", 
                    color: "#1976D2",
                    extendedProps: { type: 'bt' }
                },
                { 
                    title: "⚡ BT #102 - Électricité", 
                    start: "2026-03-20 14:00", 
                    end: "2026-03-20 17:00", 
                    color: "#1976D2",
                    extendedProps: { type: 'bt' }
                },
                { 
                    title: "⚡ BT #102 - Électricité", 
                    start: "2026-03-20 09:00", 
                    end: "2026-03-20 17:00", 
                    color: "#1976D2",
                    extendedProps: { type: 'bt' }
                }
            ],

            eventsMaintenance: [
                { 
                    title: "🔧 Maintenance Compresseur", 
                    start: "2026-03-25", 
                    color: "#E53935",
                    extendedProps: { type: 'maintenance' }
                },
                { 
                    title: "❄️ Maintenance Climatisation", 
                    start: "2026-04-01", 
                    color: "#E53935",
                    extendedProps: { type: 'maintenance' }
                }
            ]
        }
    },

    computed: {
        calendarOptions() {
            return {
                plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
                initialView: 'dayGridMonth',
                locale: frLocale,
                firstDay: 1, // Lundi
                
                // Gestion des heures
                slotMinTime: "07:00:00",
                slotMaxTime: "20:00:00",
                slotDuration: '00:30:00',
                slotLabelInterval: '01:00',
                
                // Dimensions
                height: "auto",
                contentHeight: "auto",
                aspectRatio: 1.8,
                
                // Toolbar
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay'
                },

                // Limite à la période affichée
                validRange: {
                    start: new Date(new Date().getFullYear(), new Date().getMonth(), 1),
                    end: new Date(new Date().getFullYear(), new Date().getMonth() + 1, 1)
                },

                // Événements dynamiques
                events: this.mode === "bt" ? this.eventsBT : this.eventsMaintenance,

                // Configuration des événements
                editable: true,
                selectable: true,
                selectMirror: true,
                dayMaxEvents: 3,
                dayMaxEventRows: true,
                weekNumbers: false,
                
                // Format des événements
                eventDisplay: 'auto',
                eventTimeFormat: {
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: false
                },
                
                // Gestion des conflits
                eventOrder: 'start',
                eventOrderStrict: false,
                
                // Classes CSS personnalisées
                eventClassNames: (arg) => {
                    return ['custom-event', `event-type-${arg.event.extendedProps.type || 'default'}`];
                },
                
                // Gestion des dates vides
                dayCellClassNames: (arg) => {
                    return arg.isToday ? 'today-cell' : '';
                }
            }
        }
    }
}
</script>

<style scoped>
/* Utilisation des variables CSS Vuetify */
.calendar-container {
    background: rgb(var(--v-theme-background)) !important;
    min-height: 100vh;
}

.calendar-wrapper {
    background: rgb(var(--v-theme-surface));
    border-radius: 12px;
    overflow: hidden;
}

/* Styles de base du calendrier */
:deep(.fc) {
    --fc-border-color: rgba(var(--v-border-color), var(--v-border-opacity));
    --fc-page-bg-color: rgb(var(--v-theme-surface));
    --fc-neutral-bg-color: rgba(var(--v-theme-on-surface), 0.05);
    --fc-event-bg-color: var(--v-primary-base);
    --fc-event-border-color: var(--v-primary-base);
    --fc-event-text-color: #FFFFFF;
    --fc-today-bg-color: rgba(var(--v-theme-primary), 0.1);
    --fc-button-text-color: #FFFFFF;
    --fc-button-bg-color: rgb(var(--v-theme-primary));
    --fc-button-border-color: rgb(var(--v-theme-primary));
    --fc-button-hover-bg-color: rgb(var(--v-theme-primary-darken-1));
    --fc-button-hover-border-color: rgb(var(--v-theme-primary-darken-1));
    --fc-button-active-bg-color: rgb(var(--v-theme-primary-darken-2));
    --fc-button-active-border-color: rgb(var(--v-theme-primary-darken-2));
    
    font-family: 'Roboto', sans-serif;
    background: rgb(var(--v-theme-surface));
    border-radius: 12px;
    padding: 20px;
}

/* En-tête du calendrier */
:deep(.fc-toolbar-title) {
    color: rgb(var(--v-theme-on-surface)) !important;
    font-size: 1.5rem !important;
    font-weight: 500 !important;
    text-transform: capitalize;
}

/* En-tête des jours de la semaine */
:deep(.fc-col-header-cell) {
    background: rgb(var(--v-theme-primary)) !important;
    padding: 12px 0 !important;
}

:deep(.fc-col-header-cell-cushion) {
    color: rgb(var(--v-theme-on-primary)) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    text-decoration: none !important;
}

/* En-tête de la vue jour */
:deep(.fc-timegrid-axis) {
    background: rgb(var(--v-theme-primary)) !important;
    color: rgb(var(--v-theme-on-primary)) !important;
    font-weight: 600 !important;
}

:deep(.fc-timegrid-axis-cushion) {
    color: rgb(var(--v-theme-on-primary)) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* Jours dans la grille */
:deep(.fc-daygrid-day-number) {
    color: rgb(var(--v-theme-on-surface)) !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    padding: 8px !important;
    text-decoration: none !important;
}

:deep(.fc-day-other .fc-daygrid-day-number) {
    opacity: 0.6;
    color: rgba(var(--v-theme-on-surface), 0.6) !important;
}

/* Cellules de jour */
:deep(.fc-daygrid-day) {
    border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)) !important;
    transition: background-color 0.2s ease;
}

:deep(.fc-daygrid-day:hover) {
    background-color: rgba(var(--v-theme-primary), 0.05) !important;
}

/* Jour actuel */
:deep(.fc-day-today) {
    background-color: rgba(var(--v-theme-primary), 0.1) !important;
}

:deep(.fc-day-today .fc-daygrid-day-number) {
    color: rgb(var(--v-theme-primary)) !important;
    font-weight: 700 !important;
    background: rgba(var(--v-theme-primary), 0.1);
    border-radius: 50%;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 4px auto;
}

/* Week-end */
:deep(.fc-day-sat), :deep(.fc-day-sun) {
    background-color: rgba(var(--v-theme-on-surface), 0.02) !important;
}

/* Événements */
:deep(.fc-event) {
    border-radius: 6px !important;
    padding: 4px 8px !important;
    margin: 2px 4px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    border: none !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    color: var(--text) !important;
}

:deep(.fc-event:hover) {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
    filter: brightness(1.1) !important;
}

:deep(.fc-event-title) {
    font-weight: 500 !important;
    white-space: normal !important;
    line-height: 1.3 !important;
    color: var(--text) !important;
}

:deep(.fc-event-time) {
    font-weight: 400 !important;
    opacity: 0.9 !important;
    margin-right: 4px !important;
}

:deep(.fc-event-main) {
    padding: 2px !important;
}

/* Types d'événements */
:deep(.event-type-bt) {
    border-left: 3px solid #0D47A1 !important;
}

:deep(.event-type-maintenance) {
    border-left: 3px solid #B71C1C !important;
}

/* Vue semaine / jour */
:deep(.fc-timegrid-slot) {
    height: 3em !important;
    border-bottom: 1px solid rgba(var(--v-border-color), 0.3) !important;
}

:deep(.fc-timegrid-slot-label) {
    font-size: 0.85rem !important;
    color: rgb(var(--v-theme-on-surface)) !important;
    font-weight: 500 !important;
}

:deep(.fc-timegrid-slot-label-cushion) {
    color: rgb(var(--v-theme-on-surface)) !important;
    font-weight: 500 !important;
}

:deep(.fc-timegrid-axis) {
    background: rgb(var(--v-theme-primary)) !important;
}

:deep(.fc-timegrid-axis-cushion) {
    color: rgb(var(--v-theme-on-primary)) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

:deep(.fc-timegrid-now-indicator-line) {
    border-color: rgb(var(--v-theme-primary)) !important;
    border-width: 2px !important;
}

:deep(.fc-timegrid-now-indicator-arrow) {
    border-color: rgb(var(--v-theme-primary)) !important;
    color: rgb(var(--v-theme-primary)) !important;
}

/* Boutons de la toolbar */
:deep(.fc-button) {
    background: rgb(var(--v-theme-primary)) !important;
    border-color: rgb(var(--v-theme-primary)) !important;
    color: var(--text) !important;
    text-transform: none !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.2s ease !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

:deep(.fc-button:hover) {
    background: rgb(var(--v-theme-primary-darken-1)) !important;
    border-color: rgb(var(--v-theme-primary-darken-1)) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
}

:deep(.fc-button:disabled) {
    opacity: 0.6 !important;
    cursor: not-allowed !important;
}

:deep(.fc-button-primary:not(:disabled):active),
:deep(.fc-button-primary:not(:disabled).fc-button-active) {
    background: rgb(var(--v-theme-primary-darken-2)) !important;
    border-color: rgb(var(--v-theme-primary-darken-2)) !important;
}

/* Icônes dans les boutons */
:deep(.fc-icon) {
    font-size: 1.2em !important;
    color: #FFFFFF !important;
}

/* Texte des boutons de navigation */
:deep(.fc-button .fc-icon) {
    color: #FFFFFF !important;
}

:deep(.fc-button span) {
    color: #FFFFFF !important;
}

/* Popover pour les événements multiples */
:deep(.fc-more-popover) {
    background: rgb(var(--v-theme-surface)) !important;
    border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)) !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}

:deep(.fc-more-popover .fc-popover-header) {
    background: rgba(var(--v-theme-primary), 0.1) !important;
    padding: 8px 12px !important;
    border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)) !important;
}

:deep(.fc-more-popover .fc-popover-title) {
    color: rgb(var(--v-theme-on-surface)) !important;
    font-weight: 500 !important;
}

/* Vue par jour - en-tête */
:deep(.fc-timegrid-col) {
    background: rgb(var(--v-theme-surface)) !important;
}

:deep(.fc-timegrid-col .fc-col-header-cell) {
    background: rgb(var(--v-theme-primary)) !important;
}

/* Adaptations pour le dark mode */
:deep(.v-theme--dark) {
    --fc-border-color: rgba(255, 255, 255, 0.12);
    --fc-neutral-bg-color: rgba(255, 255, 255, 0.05);
}

:deep(.v-theme--dark .fc-day-today) {
    background-color: rgba(var(--v-theme-primary), 0.15) !important;
}

:deep(.v-theme--dark .fc-day-sat),
:deep(.v-theme--dark .fc-day-sun) {
    background-color: rgba(255, 255, 255, 0.03) !important;
}

:deep(.v-theme--dark .fc-event) {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
}

:deep(.v-theme--dark .fc-timegrid-slot-label) {
    color: rgba(255, 255, 255, 0.9) !important;
}

:deep(.v-theme--dark .fc-daygrid-day-number) {
    color: rgba(255, 255, 255, 0.9) !important;
}

/* Responsive */
@media (max-width: 768px) {
    :deep(.fc) {
        padding: 12px;
    }
    
    :deep(.fc-toolbar) {
        flex-direction: column;
        gap: 12px;
    }
    
    :deep(.fc-toolbar-title) {
        font-size: 1.2rem !important;
    }
    
    :deep(.fc-button) {
        padding: 6px 12px !important;
        font-size: 0.85rem !important;
    }
    
    :deep(.fc-col-header-cell-cushion) {
        font-size: 0.85rem !important;
    }
    
    :deep(.fc-event) {
        font-size: 0.75rem !important;
        padding: 2px 4px !important;
    }
}
</style>