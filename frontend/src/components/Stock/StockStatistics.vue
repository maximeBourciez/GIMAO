<template>
  <v-card elevation="1" class="rounded-lg pa-3">
    <v-card-title class="font-weight-bold text-uppercase text-primary text-body-2 mb-2">
      Statistiques
    </v-card-title>
    <v-divider class="mb-3"></v-divider>
    <v-row dense>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-2">
          <span class="text-caption text-grey-darken-1">Hors stock</span>
          <v-chip size="small" color="error" variant="tonal">
            {{ horsStockCount }}
          </v-chip>
        </div>
      </v-col>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-2">
          <span class="text-caption text-grey-darken-1">Sous le seuil</span>
          <v-chip size="small" color="warning" variant="tonal">
            {{ sousSeuilCount }}
          </v-chip>
        </div>
      </v-col>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center">
          <span class="text-caption text-grey-darken-1">Stock suffisant</span>
          <v-chip size="small" color="success" variant="tonal">
            {{ stockSuffisantCount }}
          </v-chip>
        </div>
      </v-col>
    </v-row>
  </v-card>
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
