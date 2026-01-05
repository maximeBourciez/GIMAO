import { ref } from "vue";
import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api/";

/**
 * Composable API flexible
 * @param {string|Object} config - URL ou objet de configuration { url, method }
 * @returns {Object} État et méthodes pour les appels API
 */
export function useApi(config = null) {
  const data = ref(null);
  const loading = ref(false);
  const error = ref(null);

  // Si config est une string, c'est une URL de base
  const baseUrl = typeof config === "string" ? config : config?.url || null;

  /**
   * Appel API avec axios direct (si baseUrl fourni)
   * @param {string} endpoint - Endpoint à appeler
   * @param {Object} options - Options axios (method, data, params, etc.)
   * @returns {Promise} Résultat de l'API
   */
  const fetch = async (endpoint = "", options = {}) => {
    if (!baseUrl) {
      throw new Error(
        "baseUrl non défini. Utilisez call() pour api.js ou passez une URL à useApi()"
      );
    }

    loading.value = true;
    error.value = null;
    try {
      const url = endpoint.startsWith("http")
        ? endpoint
        : `${baseUrl}${endpoint}`;
      const response = await axios({
        url,
        method: options.method || "GET",
        ...options,
      });
      data.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.message || "Erreur lors de l'appel API";
      console.error(`Error fetching ${endpoint}:`, err);
      throw err;
    } finally {
      loading.value = false;
    }
  };

  /**
   * GET request
   * @param {string} endpoint - Endpoint relatif ou complet
   * @param {Object} params - Paramètres de requête
   */
  const get = async (endpoint, params = {}) => {
    return await fetch(endpoint, { method: "GET", params });
  };

  /**
   * POST request
   * @param {string} endpoint - Endpoint relatif ou complet
   * @param {Object} payload - Données à envoyer
   * @param {Object} options - Options supplémentaires (ex: headers)
   */
  const post = async (endpoint, payload, options = {}) => {
    return await fetch(endpoint, { method: "POST", data: payload, ...options });
  };

  /**
   * PUT request
   * @param {string} endpoint - Endpoint relatif ou complet
   * @param {Object} payload - Données à envoyer
   * @param {Object} options - Options supplémentaires (ex: headers)
   */
  const put = async (endpoint, payload, options = {}) => {
    return await fetch(endpoint, { method: "PUT", data: payload, ...options });
  };

  /**
   * PATCH request
   * @param {string} endpoint - Endpoint relatif ou complet
   * @param {Object} payload - Données à mettre à jour
   */
  const patch = async (endpoint, payload) => {
    return await fetch(endpoint, { method: "PATCH", data: payload });
  };

  /**
   * DELETE request
   * @param {string} endpoint - Endpoint relatif ou complet
   */
  const remove = async (endpoint) => {
    return await fetch(endpoint, { method: "DELETE" });
  };

  /**
   * Reset de l'état
   */
  const reset = () => {
    data.value = null;
    error.value = null;
    loading.value = false;
  };

  return {
    // State
    data,
    loading,
    error,

    // Methods
    fetch,
    get,
    post,
    put,
    patch,
    remove,
    reset,
  };
}
