<template>
  <div>
    <h3 class="mb-3">Sélectionner un lieu</h3>

    <p v-if="!items || items.length === 0" class="text-caption">
      Pas de données disponibles.
    </p>

    <VTreeview
      v-else
      :items="items"
      item-key="id"
      item-title="nomLieu"
      :open.sync="openNodes"
      activatable
      hoverable
      rounded
      density="compact"
    >
      <!-- Ligne personnalisée -->
      <template #prepend="{ item, open }">
        <!-- Triangle -->
        <v-icon
          v-if="item.children && item.children.length > 0"
          @click.stop="toggleNode(item)"
          :class="{ 'rotate-icon': open }"
        >
          {{ open ? 'mdi-triangle-down' : 'mdi-triangle-right' }}
        </v-icon>

        <span v-else class="tree-icon-placeholder"></span>

        <!-- Case à cocher -->
        <v-checkbox
          :model-value="isSelected(item)"
          @update:model-value="() => onSelect(item)"
          density="compact"
          hide-details
          :disabled="isLocked && !isSelected(item)"
        ></v-checkbox>
      </template>
    </VTreeview>

    <!-- Chip avec le lieu -->
    <v-chip
      v-if="selected"
      color="primary"
      class="mt-2"
      closable
      @click:close="emit('update:selected', null)"
    >
      Lieu sélectionné : {{ selected.nomLieu }}
    </v-chip>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { VTreeview } from "vuetify/labs/components";

const props = defineProps({
  items: Array,
  selected: Object,
  lockSelection: { type: Boolean, default: false },
});

const emit = defineEmits(["update:selected"]);

const openNodes = ref([]);

// Détecte si sélection bloquée
const isLocked = computed(() => props.lockSelection && props.selected !== null);

// Détecte si un item est celui sélectionné
const isSelected = (item) => {
  return props.selected && props.selected.id === item.id;
};

// Sélection via checkbox
const onSelect = (item) => {
  if (isLocked.value && !isSelected(item)) return; // sélection bloquée

  emit("update:selected", isSelected(item) ? null : item);
};

// Gestion de l’ouverture des nœuds
const toggleNode = (item) => {
  const index = openNodes.value.indexOf(item.id);
  if (index === -1) openNodes.value.push(item.id);
  else openNodes.value.splice(index, 1);
};
</script>

<style scoped>
.tree-icon-placeholder {
  display: inline-block;
  width: 24px;
}

.rotate-icon {
  transform: rotate(90deg);
  transition: transform 0.15s ease;
}
</style>
