<template>
  <v-row>
    <v-col cols="12" md="4">
      <v-card elevation="1" class="rounded-lg pa-4" color="error-lighten-5">
        <div class="d-flex align-center justify-space-between">
          <div>
            <p class="text-caption text-grey-darken-1 mb-1">Hors stock</p>
            <p class="text-h4 font-weight-bold text-error">{{ horsStockCount }}</p>
          </div>
          <v-icon size="48" color="error" class="opacity-50">mdi-alert-circle</v-icon>
        </div>
      </v-card>
    </v-col>
    <v-col cols="12" md="4">
      <v-card elevation="1" class="rounded-lg pa-4" color="warning-lighten-5">
        <div class="d-flex align-center justify-space-between">
          <div>
            <p class="text-caption text-grey-darken-1 mb-1">Sous le seuil</p>
            <p class="text-h4 font-weight-bold text-warning">{{ sousSeuilCount }}</p>
          </div>
          <v-icon size="48" color="warning" class="opacity-50">mdi-alert</v-icon>
        </div>
      </v-card>
    </v-col>
    <v-col cols="12" md="4">
      <v-card elevation="1" class="rounded-lg pa-4" color="success-lighten-5">
        <div class="d-flex align-center justify-space-between">
          <div>
            <p class="text-caption text-grey-darken-1 mb-1">Stock suffisant</p>
            <p class="text-h4 font-weight-bold text-success">{{ stockSuffisantCount }}</p>
          </div>
          <v-icon size="48" color="success" class="opacity-50">mdi-check-circle</v-icon>
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
  }
});

// Statistiques de stock
const horsStockCount = computed(() => {
  return props.consommables.filter(c => c.quantite === 0).length;
});

const sousSeuilCount = computed(() => {
  return props.consommables.filter(c => 
    c.quantite > 0 && c.seuilStockFaible !== null && c.quantite <= c.seuilStockFaible
  ).length;
});

const stockSuffisantCount = computed(() => {
  return props.consommables.filter(c => 
    c.seuilStockFaible === null || c.quantite > c.seuilStockFaible
  ).length;
});
</script>

<style scoped>
.opacity-50 {
  opacity: 0.5;
}
</style>
