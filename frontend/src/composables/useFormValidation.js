import { ref, computed } from "vue";

/**
 * Composable pour gérer les validations de formulaire
 * @param {Object} formData - Données du formulaire (ref ou reactive)
 * @param {Object} rules - Règles de validation
 * @returns {Object} État de validation et fonctions utilitaires
 */
export function useFormValidation(formData, rules = {}) {
  const commonRules = {
    required: (value) => !!value || "Ce champ est requis",
    email: (value) => {
      const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return !value || pattern.test(value) || "Email invalide";
    },
    phone: (value) => {
      const pattern = /^[\d\s+\-()]+$/;
      return !value || pattern.test(value) || "Numéro de téléphone invalide";
    },
    minLength: (min) => (value) =>
      !value || value.length >= min || `Minimum ${min} caractères`,
    maxLength: (max) => (value) =>
      !value || value.length <= max || `Maximum ${max} caractères`,
    number: (value) => !value || !isNaN(value) || "Doit être un nombre",
    positive: (value) => !value || Number(value) > 0 || "Doit être positif",
    url: (value) => {
      const pattern =
        /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/;
      return !value || pattern.test(value) || "URL invalide";
    },
  };

  /**
   * Combine les règles required avec d'autres règles
   */
  const createRules = (ruleNames = []) => {
    return ruleNames
      .map((ruleName) => {
        if (typeof ruleName === "string") {
          return commonRules[ruleName];
        } else if (typeof ruleName === "function") {
          return ruleName;
        } else if (ruleName.name && ruleName.param) {
          return commonRules[ruleName.name](ruleName.param);
        }
        return null;
      })
      .filter(Boolean);
  };

  /**
   * Valide si tous les champs requis sont remplis
   */
  const isValid = computed(() => {
    for (const [field, fieldRules] of Object.entries(rules)) {
      const value = formData.value ? formData.value[field] : formData[field];

      if (Array.isArray(fieldRules)) {
        for (const rule of fieldRules) {
          const result = typeof rule === "function" ? rule(value) : true;
          if (result !== true) {
            return false;
          }
        }
      }
    }
    return true;
  });

  /**
   * Génère les règles Vuetify pour un champ
   */
  const getFieldRules = (fieldName) => {
    const fieldRules = rules[fieldName];
    if (!fieldRules) return [];

    if (Array.isArray(fieldRules)) {
      return fieldRules;
    }

    return createRules(fieldRules);
  };

  /**
   * Valide un email
   */
  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  /**
   * Valide un numéro de téléphone
   */
  const validatePhone = (phone) => {
    const re = /^[\d\s+\-()]+$/;
    return re.test(phone);
  };

  /**
   * Vérifie si tous les champs obligatoires sont remplis
   */
  const checkRequiredFields = (requiredFields) => {
    for (const field of requiredFields) {
      const value = formData.value ? formData.value[field] : formData[field];
      if (!value || (typeof value === "string" && value.trim() === "")) {
        return false;
      }
    }
    return true;
  };

  return {
    commonRules,
    createRules,
    isValid,
    getFieldRules,
    validateEmail,
    validatePhone,
    checkRequiredFields,
  };
}

/**
 * Hook pour créer un formulaire avec validation
 * @param {Object} initialData - Données initiales du formulaire
 * @param {Object} validationRules - Règles de validation
 * @returns {Object} État du formulaire et fonctions
 */
export function useForm(initialData = {}, validationRules = {}) {
  const formData = ref(initialData);
  const errorMessage = ref("");
  const successMessage = ref("");
  const loading = ref(false);

  const validation = useFormValidation(formData, validationRules);

  const resetForm = () => {
    formData.value = { ...initialData };
    errorMessage.value = "";
    successMessage.value = "";
  };

  const setError = (message) => {
    errorMessage.value = message;
    successMessage.value = "";
  };

  const setSuccess = (message) => {
    successMessage.value = message;
    errorMessage.value = "";
  };

  const clearMessages = () => {
    errorMessage.value = "";
    successMessage.value = "";
  };

  return {
    formData,
    errorMessage,
    successMessage,
    loading,
    validation,
    resetForm,
    setError,
    setSuccess,
    clearMessages,
  };
}
