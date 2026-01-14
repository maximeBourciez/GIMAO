<template>
  <div>
  <v-row align="center" class="mb-2" justify="space-between">
    
    <h3 class="mb-3" v-if="showTitle">Sélectionner un lieu</h3>
    <v-btn v-if="showCreateButton" color="primary" @click="createWithoutParent">
      <v-icon left>mdi-plus</v-icon>
      Créer un nouveau lieu
    </v-btn>
  </v-row>
    <p v-if="!items || items.length === 0" class="text-caption">
      Pas de données disponibles.
    </p>

    <VTreeview v-else :items="items" item-key="id" item-title="nomLieu" :open.sync="openNodes" activatable hoverable
      rounded density="compact">
      <!-- Ligne personnalisée -->
      <template #prepend="{ item, open }">
        <!-- Case à cocher -->
        <v-checkbox :model-value="isSelected(item)" @update:model-value="() => onSelect(item)" density="compact"
          hide-details :disabled="isLocked && !isSelected(item)"></v-checkbox>
      </template>

      <template #append="{ item }">
        <v-btn v-if="showCreateButton" icon color="primary" class="tiny-btn" @click.stop="onCreate(item)">
          <v-icon size="16">mdi-plus</v-icon>
        </v-btn>
      </template>

    </VTreeview>

    <!-- Chip avec le lieu -->
    <v-chip v-if="selected" color="primary" class="mt-2" closable @click:close="emit('update:selected', null)">
      Lieu sélectionné : {{ selected.nomLieu }}
    </v-chip>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { VTreeview } from 'vuetify/labs/components'

const props = defineProps({
  items: Array,
  selected: Object,
  lockSelection: { type: Boolean, default: false },
  showTitle: { type: Boolean, default: true },
  showCreateButton: { type: Boolean, default: false },
});

const emit = defineEmits(["update:selected", "create"]);

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

// Transmission de l’événement de création
const onCreate = (item) => {
  console.log("Create location under parent:", item); // Debug
  emit("create", item.id);
};

const createWithoutParent = () => {
  emit("create", null);
};


</script>


<style scoped>
.tiny-btn {
  width: 30px !important;
  height: 30px !important;
  min-width: 20px !important;
  padding: 0 !important;
}
</style>

