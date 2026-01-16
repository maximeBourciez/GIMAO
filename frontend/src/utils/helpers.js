import {
  EQUIPMENT_STATUS,
  EQUIPMENT_STATUS_COLORS,
  INTERVENTION_STATUS_COLORS,
} from "./constants";

// ============================================
// FONCTIONS DE COULEURS
// ============================================

/**
 * Retourne la couleur associée à un statut d'équipement
 * @param {string} status - Le statut de l'équipement
 * @returns {string} La couleur correspondante
 */
export function getStatusColor(code) {
  return EQUIPMENT_STATUS_COLORS[code] || "grey";
}

/**
 * Retourne le libellé associé à un code de statut d'équipement
 * @param {string} code 
 * @returns  {string} Le libellé du statut
 */
export function getStatusLabel(code) {
  return EQUIPMENT_STATUS[code] || "Inconnu";
}


/**
 * Retourne la couleur associée à un niveau de défaillance
 * @param {string} level - Le niveau de défaillance
 * @returns {string} La couleur correspondante
 */
export function getFailureLevelColor(level) {
  return EQUIPMENT_STATUS_COLORS[level] || "grey";
}

/**
 * Retourne la couleur (token Vuetify) associée à un statut de bon de travail
 * @param {string} statusCode
 * @returns {string}
 */
export function getInterventionStatusColor(statusCode) {
  return INTERVENTION_STATUS_COLORS[statusCode] || "grey";
}

// ============================================
// FONCTIONS DE FORMATAGE
// ============================================

/**
 * Formate une date au format français (JJ/MM/AAAA)
 * @param {string} dateString - La date à formater
 * @returns {string} La date formatée
 */
export function formatDate(dateString) {
  if (!dateString) return "Non spécifié";
  const date = new Date(dateString);
  return date.toLocaleDateString("fr-FR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}

/**
 * Formate une date avec l'heure au format français
 * @param {string} dateString - La date à formater
 * @returns {string} La date et l'heure formatées
 */
export function formatDateTime(dateString) {
  if (!dateString) return "Non spécifié";
  const date = new Date(dateString);
  return date.toLocaleString("fr-FR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
