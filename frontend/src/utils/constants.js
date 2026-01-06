// ============================================
// CONSTANTES GÉNÉRALES
// ============================================

export const API_BASE_URL = "http://localhost:8000/api/";
export const BASE_URL = "http://localhost:8000";
export const MEDIA_BASE_URL = BASE_URL + '/media/'
export const DEFAULT_ITEMS_PER_PAGE = 10;

// ============================================
// STATUTS D'ÉQUIPEMENT
// ============================================

export const EQUIPMENT_STATUS = {
    EN_FONCTIONNEMENT: "En fonctionnement",
    A_LARRET: "À l'arrêt",
    DEGRADE: "Dégradé",
    HORS_SERVICE: "Hors service",
};


export const EQUIPMENT_STATUS_COLORS = {
    EN_FONCTIONNEMENT: "green",
    A_LARRET: "red",
    DEGRADE: "orange",
    HORS_SERVICE: "grey",
};


// ============================================
// NIVEAUX DE DÉFAILLANCE
// ============================================

export const FAILURE_LEVELS = {
    MINOR: "Mineur",
    MAJOR: "Majeur",
    CRITICAL: "Critique",
};

export const FAILURE_LEVEL_COLORS = {
    [FAILURE_LEVELS.MINOR]: "green",
    [FAILURE_LEVELS.MAJOR]: "orange",
    [FAILURE_LEVELS.CRITICAL]: "red",
};

// ============================================
// STATUTS D'INTERVENTION (BT)
// ============================================
export const INTERVENTION_STATUS = {
    EN_ATTENTE: "En attente",
    EN_COURS: "En cours",
    TERMINEE: "Terminée",
    EN_RETARD: "En retard",
    CLOTURE: "Cloturé",
};

// ============================================
// HEADERS DE TABLEAUX
// ============================================

export const TABLE_HEADERS = {

    /********************************
     *  DEMANDES D'INTERVENTIONS
     *******************************/
    FAILURES_SUPER_LIGHT: [
        {
            title: "N°",
            align: "start",
            sortable: true,
            value: "id",
        },
        {
            title: "Nom",
            align: "start",
            sortable: true,
            value: "nom",
        },
        {
            title: "Statut",
            align: "center",
            sortable: true,
            value: "statut",
        },
    ],

    FAILURES_LIGHT: [
        {
            title: "N°",
            align: "start",
            sortable: true,
            value: "id",
        },
        {
            title: "Nom",
            align: "start",
            sortable: true,
            value: "nom",
        },
        {
            title: "Créateur",
            align: "center",
            sortable: true,
            value: "createur",
        },
        {
            title: "Statut",
            align: "center",
            sortable: true,
            value: "statut",
        },
    ],

    FAILURES: [
        {
            title: "N°",
            align: "start",
            sortable: true,
            value: "id",
        },
        {
            title: "Nom",
            align: "start",
            sortable: true,
            value: "nom",
        },
        {
            title: "Commentaire",
            align: "center",
            sortable: false,
            value: "commentaire",
        },
        {
            title: "Créateur",
            align: "center",
            sortable: true,
            value: "createur",
        },
        {
            title: "Statut",
            align: "center",
            sortable: true,
            value: "statut",
        },
        {
            title: "Équipement",
            align: "center",
            sortable: true,
            value: "equipement",
        },
    ],

    /********************************
     *  BONS DE TRAVAIL
     *******************************/

    INTERVENTIONS: [
        {
            title: "Nom",
            align: "start",
            sortable: true,
            value: "nomIntervention",
        },
        {
            title: "Date d'assignation",
            align: "center",
            sortable: true,
            value: "dateAssignation",
        },
        {
            title: "Responsable",
            align: "center",
            sortable: true,
            value: "responsable",
        },
        {
            title: "Niveau",
            align: "center",
            sortable: false,
            value: "niveau",
        },
    ],

    INTERVENTIONS_LIGHT: [
        {
            title: "Nom",
            align: "start",
            sortable: true,
            value: "nom",
        },
        {
            title: "Date d'assignation",
            align: "center",
            sortable: true,
            value: "date_assignation",
        },
        {
            title: "Statut",
            align: "center",
            sortable: true,
            value: "statut",
        },
        {
            title: "Visualiser",
            align: "start",
            sortable: false,
            value: "action",
        },
    ],

    /********************************
     *  ÉQUIPEMENTS
     *******************************/

    EQUIPMENTS: [
        {
            title: "Désignation",
            value: "modeleEquipement.nomModeleEquipement",
            sortable: true,
            align: "center",
        },
        {
            title: "Lieu",
            value: "lieu.nomLieu",
            sortable: true,
            align: "center",
        },
        {
            title: "Statut",
            value: "statut.statutEquipement",
            sortable: true,
            align: "center",
        },
    ],

    COUNTERS: [
        {
            title: "ID",
            value: "id",
            sortable: true,
            align: "center",
        },
        {
            title: "Nom du compteur",
            value: "nom",
            sortable: false,
            align: "center",
        },
        {
            title: "Valeur Courante",
            value: "valeurCourante",
            sortable: false,
            align: "center",
        },
        {
            title: "Prochaine Maintenance",
            value: "prochaineMaintenance",
            sortable: false,
            align: "center",
        },
        {
            title: "Unité",
            value: "unite",
            sortable: false,
            align: "center",
        },
        {
            title: "Visualiser",
            value: "action",
            sortable: false,
            align: "center",
        }
    ],

    CONSUMABLES: [
        {
            title: "Désignation",
            value: "designation",
            sortable: true,
            align: "center",
        },
        {
            title: "Fabricant",
            value: "fabricant",
            sortable: true,
            align: "center",
        }
    ],

    /********************************
     * DOCUMENTS
     *******************************/
    DOCUMENTS: [
        {
            title: "Doucument",
            value: "nomDocument",
            sortable: false,
            align: "center",
        },
        {
            title: "Type",
            value: "typeDocument",
            sortable: true,
            align: "center",
        },
        {
            title: "Télécharger",
            value: "action",
            sortable: false,
            align: "center",
        },
    ],

};
