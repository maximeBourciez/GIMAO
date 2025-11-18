/**
 * Export centralisé des composants de formulaire
 *
 * Usage local (recommandé):
 * import { FormAlert, FormActions, FormContainer } from '@/components/common';
 *
 * Usage global (via plugin):
 * import formComponents from '@/components/common/plugin';
 * app.use(formComponents);
 */

// Export des composants individuels
export { default as FormAlert } from "./FormAlert.vue";
export { default as FormActions } from "./FormActions.vue";
export { default as FormContainer } from "./FormContainer.vue";

// Export du composant principal (aussi disponible directement)
export { default as BaseForm } from "../BaseForm.vue";

// Export du plugin Vue (pour enregistrement global)
export { default as formComponentsPlugin } from "./plugin.js";
