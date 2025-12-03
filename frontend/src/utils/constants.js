// ============================================
// CONSTANTES GÉNÉRALES
// ============================================

export const API_BASE_URL = "http://localhost:8000/api/";
export const BASE_URL = "http://localhost:8000";
export const DEFAULT_ITEMS_PER_PAGE = 10;

// ============================================
// STATUTS D'ÉQUIPEMENT
// ============================================

export const EQUIPMENT_STATUS = {
  FUNCTIONING: "Fonctionnel",
  STOPPED: "A l'arrêt",
  DEGRADED: "Dégradé"
};

export const EQUIPMENT_STATUS_COLORS = {
  [EQUIPMENT_STATUS.FUNCTIONING]: "green",
  [EQUIPMENT_STATUS.STOPPED]: "red",
  [EQUIPMENT_STATUS.DEGRADED]: "orange"
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
// HEADERS DE TABLEAUX
// ============================================

export const TABLE_HEADERS = {
  FAILURES: [
    {
      title: "Commentaire",
      align: "start",
      sortable: true,
      value: "commentaireDefaillance",
    },
    {
      title: "Traitée",
      align: "center",
      sortable: true,
      value: "traite",
    },
    {
      title: "Niveau",
      align: "center",
      sortable: true,
      value: "niveau",
    },
    {
      title: "Équipement",
      align: "center",
      sortable: false,
      value: "equipement",
    },
  ],

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
};
