<template>
  <v-dialog
    v-model="dialogVisible"
    max-width="450"
    persistent
  >
    <v-card class="rounded-lg">
      <!-- Header -->
      <v-card-title class="d-flex align-center pa-4" :class="headerClass">
        <v-icon :color="iconColor" size="28" class="mr-3">{{ modalIcon }}</v-icon>
        <span class="modal-title">{{ title }}</span>
      </v-card-title>

      <v-divider></v-divider>

      <!-- Content -->
      <v-card-text class="pa-4">
        <p class="modal-message mb-0">{{ formattedMessage }}</p>
        <slot name="content"></slot>
      </v-card-text>

      <v-divider></v-divider>

      <!-- Actions -->
      <v-card-actions class="pa-4 d-flex justify-end">
        <v-btn
          variant="outlined"
          color="grey-darken-1"
          @click="handleCancel"
          :disabled="loading"
          class="mr-2"
        >
          {{ cancelText }}
        </v-btn>
        <v-btn
          variant="flat"
          :color="confirmButtonColor"
          @click="handleConfirm"
          :loading="loading"
          :disabled="loading"
        >
          <v-icon left class="mr-1" size="20">{{ confirmIcon }}</v-icon>
          {{ confirmText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  // Contrôle de la visibilité
  modelValue: {
    type: Boolean,
    default: false
  },
  // Type de modale (success, warning, error, info)
  type: {
    type: String,
    default: 'warning',
    validator: (value) => ['success', 'warning', 'error', 'info'].includes(value)
  },
  // Contenu
  title: {
    type: String,
    default: 'Confirmation requise'
  },
  message: {
    type: String,
    default: 'Êtes-vous sûr de vouloir effectuer cette action ?'
  },
  // Personnalisation des boutons
  confirmText: {
    type: String,
    default: 'Confirmer'
  },
  cancelText: {
    type: String,
    default: 'Annuler'
  },
  confirmIcon: {
    type: String,
    default: 'mdi-check'
  },
  // Couleur personnalisée (optionnel)
  confirmColor: {
    type: String,
    default: ''
  },
  // État de chargement perrmet de désactiver les boutons pendant les requêtes ou chargements
  loading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel']);

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

// Configuration par type
const typeConfig = {
  success: {
    icon: 'mdi-check-circle-outline',
    color: 'success',
    iconColor: 'success'
  },
  warning: {
    icon: 'mdi-alert-circle-outline',
    color: 'warning',
    iconColor: 'warning'
  },
  error: {
    icon: 'mdi-close-circle-outline',
    color: 'error',
    iconColor: 'error'
  },
  info: {
    icon: 'mdi-information-outline',
    color: 'primary',
    iconColor: 'primary'
  }
};

const modalIcon = computed(() => typeConfig[props.type]?.icon || typeConfig.warning.icon);
const iconColor = computed(() => typeConfig[props.type]?.iconColor || 'warning');
const headerClass = computed(() => '');

const confirmButtonColor = computed(() => {
  if (props.confirmColor) return props.confirmColor;
  return typeConfig[props.type]?.color || 'warning';
});

// Remplace les \n en vrais retours à la ligne
const formattedMessage = computed(() => {
  return props.message.replace(/\\n/g, '\n');
});

const handleConfirm = () => {
  emit('confirm');
};

const handleCancel = () => {
  emit('cancel');
  dialogVisible.value = false;
};
</script>

<style scoped>
.modal-title {
  font-weight: 600;
  font-size: 1.125rem;
  color: #05004E;
}

.modal-message {
  font-size: 0.95rem;
  color: #3C3C3C;
  line-height: 1.5;
  white-space: pre-line;
}
</style>
