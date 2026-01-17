<template>
  <v-row>
    <v-col cols="6">
      <FailureListComponent @create="handleCreate" @row-click="handleRowClick" />
    </v-col>
    <v-col cols="6">
      <InterventionListComponent />
    </v-col>
  </v-row>
</template>

<script setup>
import FailureListComponent from '@/components/FailureListComponent.vue';
import InterventionListComponent from '@/components/InterventionListComponent.vue';

const handleCreate = () => {
  // Handle create logic
};

const handleRowClick = (row) => {
  // Handle row click logic
};
</script>