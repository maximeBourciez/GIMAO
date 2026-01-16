<template>
  <div>
    <v-row align="center" class="mb-2" justify="space-between">
      <v-col v-if="showTitle" cols="auto">
        <h3 class="mb-0">Sélectionner un lieu</h3>
      </v-col>
      <v-col v-if="showCreateButton" cols="auto">
        <v-btn color="primary" @click="createWithoutParent">
          <v-icon left>mdi-plus</v-icon>
          Créer un nouveau lieu
        </v-btn>
      </v-col>
    </v-row>

    <p v-if="!items || items.length === 0" class="text-caption">
      Pas de données disponibles.
    </p>

    <VTreeview v-else :items="items" item-key="id" item-title="nomLieu" :open.sync="openNodes" activatable hoverable
      rounded density="compact">
      <!-- Checkbox après la flèche par défaut -->
      <template #prepend="{ item }">
        <v-checkbox 
          :model-value="isSelected(item)" 
          @update:model-value="() => onSelect(item)" 
          density="compact"
          hide-details 
          :disabled="isLocked && !isSelected(item)"
        />
      </template>

      <!-- Titre avec marge à droite -->
      <template #title="{ item }">
        <span class="mr-5">{{ item.nomLieu }}</span>
      </template>

      <!-- Bouton + à droite -->
      <template #append="{ item }">
        <v-btn 
          v-if="showCreateButton" 
          icon 
          color="primary" 
          size="x-small"
          @click.stop="onCreate(item)"
        >
          <v-icon size="18">mdi-plus</v-icon>
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
/* Masquer la flèche d'expansion pour les items sans enfants */
:deep(.v-treeview-item:not(:has(.v-treeview-item__children))) .v-treeview-item__toggle {
  visibility: hidden;
}

/* S'assurer que tout est sur une seule ligne avec le bon espacement */
:deep(.v-treeview-item__content) {
  display: flex !important;
  align-items: center !important;
  width: 100% !important;
  gap: 8px !important;
}

:deep(.v-treeview-item__prepend) {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

:deep(.v-treeview-item__label) {
  flex: 1 !important;
  display: flex;
  align-items: center;
  min-width: 0;
}

:deep(.v-treeview-item__append) {
  margin-left: auto !important;
  display: flex;
  align-items: center;
  flex-shrink: 0;
  padding-left: 24px !important;
}
</style>

