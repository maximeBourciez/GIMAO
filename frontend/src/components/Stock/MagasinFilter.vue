<template>
  <v-card elevation="1" class="rounded-lg pa-2">
    <v-card-title class="font-weight-bold text-uppercase text-primary text-body-2">
      Magasins
    </v-card-title>
    <v-divider></v-divider>
    <v-list dense>
      <v-list-item 
        link 
        @click="handleSelectMagasin(null)"
        :class="{ 'selected-item bg-primary-lighten-5': selectedMagasin === null }"
      >
        <v-list-item-title>Tous les magasins</v-list-item-title>
        <template v-slot:append>
          <v-chip size="small" color="primary">{{ totalCount }}</v-chip>
        </template>
      </v-list-item>
      <v-list-item 
        v-for="magasin in magasins" 
        :key="magasin.id" 
        link
        @click="handleSelectMagasin(magasin.id)"
        :class="{ 'selected-item bg-primary-lighten-5': selectedMagasin === magasin.id }"
      >
        <v-list-item-title>
          <v-icon v-if="magasin.estMobile" size="small" class="mr-1">mdi-truck</v-icon>
          <v-icon v-else size="small" class="mr-1">mdi-warehouse</v-icon>
          {{ magasin.nom }}
        </v-list-item-title>
        <template v-slot:append>
          <v-chip size="small" color="primary">
            {{ getConsommableCountByMagasin(magasin.id) }}
          </v-chip>
        </template>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  magasins: {
    type: Array,
    default: () => []
  },
  consommables: {
    type: Array,
    default: () => []
  },
  selectedMagasin: {
    type: Number,
    default: null
  }
});

const emit = defineEmits(['update:selectedMagasin']);

const totalCount = computed(() => props.consommables.length);

const getConsommableCountByMagasin = (magasinId) => {
  return props.consommables.filter(c => c.magasin === magasinId).length;
};

const handleSelectMagasin = (magasinId) => {
  emit('update:selectedMagasin', magasinId);
};
</script>

<style scoped>
.selected-item {
  border-left: 3px solid rgb(var(--v-theme-primary));
}
</style>
