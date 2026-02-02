<template>
  <div>
    <h3 class="text-subtitle-2 text-primary mb-2">Filtrer par magasin</h3>
    <v-row dense>
      <!-- Tous les magasins -->
      <v-col cols="12" sm="6" md="4" lg="3" xl="2">
        <v-card 
          elevation="1" 
          class="rounded-lg pa-2 cursor-pointer magasin-card"
          :class="{ 'selected-card': selectedMagasin === null }"
          @click="handleSelectMagasin(null)"
        >
          <div class="d-flex align-center">
            <v-icon size="24" color="primary" class="mr-2">mdi-view-grid</v-icon>
            <div>
              <p class="text-caption font-weight-medium mb-0">Tous les magasins</p>
              <p class="text-caption text-grey-darken-1 mb-0" style="font-size: 0.7rem;">{{ totalCount }} consommables</p>
            </div>
          </div>
        </v-card>
      </v-col>

      <!-- Chaque magasin -->
      <v-col 
        v-for="magasin in magasins" 
        :key="magasin.id"
        cols="12" 
        sm="6" 
        md="4" 
        lg="3"
        xl="2"
      >
        <v-card 
          elevation="1" 
          class="rounded-lg pa-2 cursor-pointer magasin-card"
          :class="{ 'selected-card': selectedMagasin === magasin.id }"
          @click="handleSelectMagasin(magasin.id)"
        >
          <div class="d-flex align-center">
            <v-icon 
              size="24" 
              :color="magasin.estMobile ? 'orange' : 'blue'" 
              class="mr-2"
            >
              {{ magasin.estMobile ? 'mdi-truck' : 'mdi-warehouse' }}
            </v-icon>
            <div>
              <p class="text-caption font-weight-medium mb-0">{{ magasin.nom }}</p>
              <p class="text-caption text-grey-darken-1 mb-0" style="font-size: 0.7rem;">
                {{ getConsommableCountByMagasin(magasin.id) }} consommables
              </p>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
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
  return props.consommables.filter(c => c.stocks.find(s => s.magasin === magasinId)).length;
};

const handleSelectMagasin = (magasinId) => {
  emit('update:selectedMagasin', magasinId);
};
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}

.magasin-card {
  transition: all 0.2s ease-in-out;
  border: 2px solid rgba(0, 0, 0, 0.12);
}

.magasin-card:hover {
  transform: translateY(-2px);
  border-color: rgb(var(--v-theme-primary));
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.selected-card {
  border-color: rgb(var(--v-theme-primary));
  background-color: rgba(var(--v-theme-primary), 0.08);
}
</style>
