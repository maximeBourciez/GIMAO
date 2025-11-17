import { EQUIPMENT_STATUS_COLORS, FAILURE_LEVEL_COLORS } from "./constants";

// ============================================
// FONCTIONS DE COULEURS
// ============================================

/**
 * Retourne la couleur associée à un statut d'équipement
 * @param {string} status - Le statut de l'équipement
 * @returns {string} La couleur correspondante
 */
export function getStatusColor(status) {
  return EQUIPMENT_STATUS_COLORS[status] || "grey";
}

/**
 * Retourne la couleur associée à un niveau de défaillance
 * @param {string} level - Le niveau de défaillance
 * @returns {string} La couleur correspondante
 */
export function getFailureLevelColor(level) {
  return FAILURE_LEVEL_COLORS[level] || "grey";
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
