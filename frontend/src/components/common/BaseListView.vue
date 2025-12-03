<template>
  <v-container :fluid="fluid">
    <!-- Header avec titre et actions -->
    <v-row v-if="title || showCreateButton || $slots.actions" class="mb-4">
      <v-col>
        <div class="d-flex align-center justify-space-between">
          <div>
            <h1 v-if="title" :class="titleClass">{{ title }}</h1>
            <p v-if="subtitle" :class="subtitleClass">{{ subtitle }}</p>
          </div>
          <div class="d-flex gap-2">
            <slot name="actions">
              <v-btn v-if="showCreateButton" :color="createButtonColor" :prepend-icon="createButtonIcon"
                @click="$emit('create')">
                {{ createButtonText }}
              </v-btn>
            </slot>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Barre de recherche et filtres -->
    <div class="justify-end">
      <v-row v-if="showSearch || $slots.filters" class="mb-4">
        <v-col v-if="showSearch" :cols="searchCols" :md="searchMd">
          <v-text-field v-model="searchQuery" :label="searchLabel" :placeholder="searchPlaceholder"
            prepend-inner-icon="mdi-magnify" clearable variant="outlined" density="compact" hide-details
            @input="handleSearch"></v-text-field>
        </v-col>
        <v-col v-if="$slots.filters">
          <slot name="filters" :search-query="searchQuery"></slot>
        </v-col>
      </v-row>
    </div>


    <!-- Alerts -->
    <FormAlert v-if="errorMessage" :message="errorMessage" type="error" dismissible class="mb-4"
      @close="$emit('clear-error')" />

    <FormAlert v-if="loading && loadingMessage" :message="loadingMessage" type="info" class="mb-4" />

    <!-- Slot avant le tableau pour contenu personnalisé -->
    <slot name="before-table"></slot>

    <!-- Tableau de données -->
    <v-card :elevation="elevation" :class="cardClass">
      <v-data-table :headers="headers" :items="computedItems" :loading="loading" :items-per-page="itemsPerPage"
        :items-per-page-options="itemsPerPageOptions" :search="internalSearch ? searchQuery : undefined"
        :sort-by="sortBy" :class="tableClass" @click:row="handleRowClick">
        <!-- Pass through all item slots -->
        <template v-for="(_, slot) in $slots" v-slot:[slot]="scope">
          <slot :name="slot" v-bind="scope"></slot>
        </template>

        <!-- Default no-data template -->
        <template v-slot:no-data>
          <div class="text-center pa-4">
            <v-icon size="64" color="grey">{{ noDataIcon }}</v-icon>
            <p class="text-h6 mt-2">{{ noDataText }}</p>
          </div>
        </template>

        <!-- Default loading template -->
        <template v-slot:loading>
          <div class="text-center pa-4">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            <p class="mt-2">{{ loadingMessage }}</p>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Slot après le tableau -->
    <slot name="after-table"></slot>
  </v-container>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import FormAlert from './FormAlert.vue';

const props = defineProps({
  // Données
  items: {
    type: Array,
    default: () => []
  },
  headers: {
    type: Array,
    required: true
  },

  // Titre et sous-titre
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  titleClass: {
    type: String,
    default: 'text-h4 text-primary'
  },
  subtitleClass: {
    type: String,
    default: 'text-subtitle-1 text-grey'
  },

  // Bouton de création
  showCreateButton: {
    type: Boolean,
    default: true
  },
  createButtonText: {
    type: String,
    default: 'Créer'
  },
  createButtonColor: {
    type: String,
    default: 'primary'
  },
  createButtonIcon: {
    type: String,
    default: 'mdi-plus'
  },

  // Recherche
  showSearch: {
    type: Boolean,
    default: true
  },
  searchLabel: {
    type: String,
    default: 'Rechercher'
  },
  searchPlaceholder: {
    type: String,
    default: 'Tapez pour rechercher...'
  },
  searchCols: {
    type: [Number, String],
    default: 12
  },
  searchMd: {
    type: [Number, String],
    default: 6
  },
  internalSearch: {
    type: Boolean,
    default: false
  },

  // Messages
  loading: {
    type: Boolean,
    default: false
  },
  loadingMessage: {
    type: String,
    default: 'Chargement des données...'
  },
  errorMessage: {
    type: String,
    default: ''
  },

  // Configuration du tableau
  itemsPerPage: {
    type: Number,
    default: 10
  },
  itemsPerPageOptions: {
    type: Array,
    default: () => [5, 10, 25, 50, 100]
  },
  sortBy: {
    type: Array,
    default: () => []
  },

  // Messages vides
  noDataText: {
    type: String,
    default: 'Aucune donnée disponible'
  },
  noDataIcon: {
    type: String,
    default: 'mdi-database-off'
  },

  // Styles
  fluid: {
    type: Boolean,
    default: false
  },
  elevation: {
    type: [Number, String],
    default: 1
  },
  cardClass: {
    type: String,
    default: 'rounded-lg'
  },
  tableClass: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['create', 'row-click', 'search', 'clear-error']);

const searchQuery = ref('');

const computedItems = computed(() => props.items || []);

const handleSearch = (value) => {
  emit('search', value);
};

const handleRowClick = (event, { item }) => {
  emit('row-click', item);
};

// Watcher pour réinitialiser la recherche si les items changent
watch(() => props.items, () => {
  if (!props.internalSearch) {
    searchQuery.value = '';
  }
});
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
