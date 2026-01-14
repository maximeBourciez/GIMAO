<template>
  <div>
    <label v-if="label" class="field-label">{{ label }}</label>
    <v-file-input
      :model-value="modelValue"
      @update:model-value="$emit('update:modelValue', $event)"
      :placeholder="placeholder"
      :accept="accept"
      :multiple="multiple"
      :show-size="showSize"
      :clearable="clearable"
      :disabled="disabled"
      :readonly="readonly"
      :prepend-icon="prependIcon"
      :prepend-inner-icon="prependInnerIcon"
      :append-icon="appendIcon"
      :append-inner-icon="appendInnerIcon"
      :hint="hint"
      :persistent-hint="persistentHint"
      :error-messages="errorMessages"
      :rules="rules"
      variant="outlined"
      density="comfortable"
      hide-details="auto"
      v-bind="$attrs"
    >
      <template v-if="$slots.selection" #selection>
        <slot name="selection"></slot>
      </template>
    </v-file-input>
  </div>
</template>

<script setup>
defineOptions({
  inheritAttrs: false
});

defineProps({
  modelValue: {
    type: [File, Array],
    default: null
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Sélectionner un fichier'
  },
  accept: {
    type: String,
    default: undefined
  },
  multiple: {
    type: Boolean,
    default: false
  },
  showSize: {
    type: Boolean,
    default: true
  },
  clearable: {
    type: Boolean,
    default: true
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  prependIcon: {
    type: String,
    default: ''
  },
  prependInnerIcon: {
    type: String,
    default: 'mdi-paperclip'
  },
  appendIcon: {
    type: String,
    default: undefined
  },
  appendInnerIcon: {
    type: String,
    default: undefined
  },
  hint: {
    type: String,
    default: undefined
  },
  persistentHint: {
    type: Boolean,
    default: false
  },
  errorMessages: {
    type: [String, Array],
    default: undefined
  },
  rules: {
    type: Array,
    default: () => []
  }
});

defineEmits(['update:modelValue']);
</script>

<style scoped>
.field-label {
  display: block;
  margin-bottom: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.87);
}
</style>
