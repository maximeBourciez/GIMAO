<template>
  <FormContainer
    :title="title"
    :subtitle="subtitle"
    :cols="cols"
    :md="md"
    :lg="lg"
    :xl="xl"
    :justify="justify"
    :fluid="fluid"
    :elevation="elevation"
    :container-class="containerClass"
    :card-class="cardClass"
    :title-class="titleClass"
    :subtitle-class="subtitleClass"
    :content-class="contentClass"
    :showActions="true"
  >
    <!-- Alerts -->
    <FormAlert
      v-if="errorMessage"
      :message="errorMessage"
      type="error"
      :dismissible="dismissibleAlerts"
      @close="$emit('clear-error')"
    />

    <FormAlert
      v-if="loading && loadingMessage"
      :message="loadingMessage"
      type="info"
    />

    <FormAlert
      v-if="successMessage"
      :message="successMessage"
      type="success"
      :dismissible="dismissibleAlerts"
      @close="$emit('clear-success')"
    />

    <!-- Form -->
    <v-form 
      ref="formRef" 
      v-model="formValid" 
      @submit.prevent="handleSubmit"
    >
      <!-- Slot pour le contenu du formulaire -->
      <slot 
        :form-data="formData"
        :is-loading="loading"
        :is-valid="formValid"
        :reset-form="resetForm"
        :reset-validation="resetValidation"
      ></slot>

      <!-- Actions -->
      <FormActions
        :submit-button-text="submitButtonText"
        :submit-button-color="submitButtonColor"
        :submit-button-class="submitButtonClass"
        :submit-button-variant="submitButtonVariant"
        :submit-disabled="!formValid || loading || customDisabled"
        :show-cancel-button="showCancelButton"
        :cancel-button-text="cancelButtonText"
        :cancel-button-color="cancelButtonColor"
        :cancel-button-class="cancelButtonClass"
        :cancel-button-variant="cancelButtonVariant"
        :show-reset-button="showResetButton"
        :reset-button-text="resetButtonText"
        :reset-button-color="resetButtonColor"
        :reset-button-class="resetButtonClass"
        :reset-button-variant="resetButtonVariant"
        :loading="loading"
        :container-class="actionsContainerClass"
        :spacer="actionsSpacer"
        :custom-cancel-action="customCancelAction"
        @cancel="handleCancel"
        @reset="handleReset"
        v-if="showActions"
      />
    </v-form>
  </FormContainer>
</template>

<script setup>
import { ref, computed } from 'vue';
import { FormAlert, FormActions, FormContainer } from '.';

const props = defineProps({
  // Titre et sous-titre
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },

  // Données du formulaire
  modelValue: {
    type: Object,
    default: () => ({})
  },

  // Messages
  loading: {
    type: Boolean,
    default: false
  },
  errorMessage: {
    type: String,
    default: ''
  },
  successMessage: {
    type: String,
    default: ''
  },
  loadingMessage: {
    type: String,
    default: 'Chargement...'
  },
  dismissibleAlerts: {
    type: Boolean,
    default: false
  },

  // Boutons de soumission
  submitButtonText: {
    type: String,
    default: 'Enregistrer'
  },
  submitButtonColor: {
    type: String,
    default: 'primary'
  },
  submitButtonClass: {
    type: String,
    default: ''
  },
  submitButtonVariant: {
    type: String,
    default: 'elevated'
  },

  // Boutons d'annulation
  showCancelButton: {
    type: Boolean,
    default: true
  },
  cancelButtonText: {
    type: String,
    default: 'Annuler'
  },
  cancelButtonColor: {
    type: String,
    default: 'secondary'
  },
  cancelButtonClass: {
    type: String,
    default: 'mr-2'
  },
  cancelButtonVariant: {
    type: String,
    default: 'elevated'
  },
  customCancelAction: {
    type: Boolean,
    default: false
  },

  // Bouton de réinitialisation
  showResetButton: {
    type: Boolean,
    default: false
  },
  resetButtonText: {
    type: String,
    default: 'Réinitialiser'
  },
  resetButtonColor: {
    type: String,
    default: 'warning'
  },
  resetButtonClass: {
    type: String,
    default: 'mr-2'
  },
  resetButtonVariant: {
    type: String,
    default: 'elevated'
  },

  // Layout responsive
  cols: {
    type: [String, Number],
    default: 12
  },
  md: {
    type: [String, Number],
    default: 12
  },
  lg: {
    type: [String, Number],
    default: 12
  },
  xl: {
    type: [String, Number],
    default: 12
  },
  justify: {
    type: String,
    default: 'start'
  },
  fluid: {
    type: Boolean,
    default: false
  },

  // Styles
  elevation: {
    type: [String, Number],
    default: 2
  },
  containerClass: {
    type: String,
    default: ''
  },
  cardClass: {
    type: String,
    default: ''
  },
  titleClass: {
    type: String,
    default: ''
  },
  subtitleClass: {
    type: String,
    default: ''
  },
  contentClass: {
    type: String,
    default: ''
  },
  actionsContainerClass: {
    type: String,
    default: 'mt-4'
  },
  actionsSpacer: {
    type: Boolean,
    default: false
  },

  // Validation
  customValidation: {
    type: Function,
    default: () => true
  },
  customDisabled: {
    type: Boolean,
    default: false
  },

  // Handling de la soumission
  handleSubmit: {
    type: Function,
    default: false
  },

  // Affichage des actions
  showActions: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(['update:modelValue', 'submit', 'cancel', 'reset', 'clear-error', 'clear-success']);

const formRef = ref(null);
const formValid = ref(false);

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const handleSubmit = () => {
  // Si une fonction personnalisée est fournie, l'utiliser
  if (props.handleSubmit && typeof props.handleSubmit === 'function') {
    props.handleSubmit(formData.value);
    return;
  }
  
  // Sinon, utiliser le comportement par défaut
  console.log('Submitting form with data:', formData.value);
  
  if (formRef.value) {
    formRef.value.validate();
  }
  
  if (formValid.value && props.customValidation()) {
    emit('submit', formData.value);
  }
};

const handleCancel = () => {
  emit('cancel');
};

const handleReset = () => {
  resetForm();
  emit('reset');
};

const resetForm = () => {
  if (formRef.value) {
    formRef.value.reset();
  }
};

const resetValidation = () => {
  if (formRef.value) {
    formRef.value.resetValidation();
  }
};

defineExpose({
  resetForm,
  resetValidation,
  formRef,
  formValid
});
</script>

<style scoped>
</style>
