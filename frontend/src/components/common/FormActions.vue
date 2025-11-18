<template>
  <div :class="containerClass">
    <v-btn
      v-if="showCancelButton"
      :color="cancelButtonColor"
      :class="cancelButtonClass"
      @click="handleCancel"
      :disabled="loading"
      :variant="cancelButtonVariant"
    >
      {{ cancelButtonText }}
    </v-btn>

    <v-btn
      v-if="showResetButton"
      :color="resetButtonColor"
      :class="resetButtonClass"
      @click="handleReset"
      :disabled="loading"
      :variant="resetButtonVariant"
    >
      {{ resetButtonText }}
    </v-btn>

    <v-spacer v-if="spacer"></v-spacer>

    <v-btn
      type="submit"
      :color="submitButtonColor"
      :class="submitButtonClass"
      :disabled="submitDisabled"
      :loading="loading"
      :variant="submitButtonVariant"
    >
      {{ submitButtonText }}
    </v-btn>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  // Bouton de soumission
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
  submitDisabled: {
    type: Boolean,
    default: false
  },

  // Bouton d'annulation
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

  // État de chargement
  loading: {
    type: Boolean,
    default: false
  },

  // Layout
  containerClass: {
    type: String,
    default: 'mt-4'
  },
  spacer: {
    type: Boolean,
    default: false
  },

  // Navigation personnalisée
  customCancelAction: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['cancel', 'reset']);
const router = useRouter();

const handleCancel = () => {
  emit('cancel');
  if (!props.customCancelAction) {
    router.go(-1);
  }
};

const handleReset = () => {
  emit('reset');
};
</script>
