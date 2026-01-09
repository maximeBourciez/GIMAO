<template>
  <v-row>
    <v-col cols="12" md="4">
      <v-card 
        elevation="1" 
        class="rounded-lg pa-2 cursor-pointer stat-card" 
        color="error-lighten-5"
        :class="{ 'selected-stat': selectedFilter === 'hors-stock' }"
        @click="handleFilterClick('hors-stock')"
      >
        <div class="d-flex align-center justify-space-between">
          <div>
            <p class="text-caption text-grey-darken-1 mb-0" style="font-size: 0.7rem;">Hors stock</p>
            <p class="text-h5 font-weight-bold text-error mb-0">{{ horsStockCount }}</p>
          </div>
          <v-icon size="32" color="error" class="opacity-50">mdi-alert-circle</v-icon>
        </div>
      </v-card>
    </v-col>
    <v-col cols="12" md="4">
      <v-card 
        elevation="1" 
        class="rounded-lg pa-2 cursor-pointer stat-card" 
        color="warning-lighten-5"
        :class="{ 'selected-stat': selectedFilter === 'sous-seuil' }"
        @click="handleFilterClick('sous-seuil')"
      >
        <div class="d-flex align-center justify-space-between">
          <div>
            <p class="text-caption text-grey-darken-1 mb-0" style="font-size: 0.7rem;">Sous le seuil</p>
            <p class="text-h5 font-weight-bold text-warning mb-0">{{ sousSeuilCount }}</p>
          </div>
          <v-icon size="32" color="warning" class="opacity-50">mdi-alert</v-icon>
        </div>
      </v-card>
    </v-col>
    <v-col cols="12" md="4">
      <v-card 
        elevation="1" 
        class="rounded-lg pa-2 cursor-pointer stat-card" 
        color="success-lighten-5"
        :class="{ 'selected-stat': selectedFilter === 'stock-suffisant' }"
        @click="handleFilterClick('stock-suffisant')"
      >
        <div class="d-flex align-center justify-space-between">
          <div>
            <p class="text-caption text-grey-darken-1 mb-0" style="font-size: 0.7rem;">Stock suffisant</p>
            <p class="text-h5 font-weight-bold text-success mb-0">{{ stockSuffisantCount }}</p>
          </div>
          <v-icon size="32" color="success" class="opacity-50">mdi-check-circle</v-icon>
        </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  consommables: {
    type: Array,
    default: () => []
  },
  selectedFilter: {
    type: String,
    default: null
  }
});

const emit = defineEmits(['filter-change']);

// Statistiques de stock
const horsStockCount = computed(() => {
  return props.consommables.filter(c => (c.quantite_totale ?? c.quantite ?? 0) === 0).length;
});

const sousSeuilCount = computed(() => {
  return props.consommables.filter(c => {
    const quantite = c.quantite_totale ?? c.quantite ?? 0;
    return quantite > 0 && c.seuilStockFaible !== null && quantite <= c.seuilStockFaible;
  }).length;
});

const stockSuffisantCount = computed(() => {
  return props.consommables.filter(c => {
    const quantite = c.quantite_totale ?? c.quantite ?? 0;
    return c.seuilStockFaible === null || quantite > c.seuilStockFaible;
  }).length;
});

const handleFilterClick = (filterType) => {
  // Si on clique sur le même filtre, on le désactive
  if (props.selectedFilter === filterType) {
    emit('filter-change', null);
  } else {
    emit('filter-change', filterType);
  }
};
</script>

<style scoped>
.opacity-50 {
  opacity: 0.5;
}

.cursor-pointer {
  cursor: pointer;
}

.stat-card {
  transition: all 0.2s ease-in-out;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.selected-stat {
  border: 2px solid rgb(var(--v-theme-primary));
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.3);
}
</style>
