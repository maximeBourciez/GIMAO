<template>
  <InterventionListComponent
    title="Liste des Bons de Travail"
    variant="auto"
    :show-create-button="false"
    no-data-text="Aucun bon de travail enregistré"
    @row-click="handleRowClick"
  />
</template>

<script setup>
import { useRouter } from 'vue-router';
import InterventionListComponent from '../../components/InterventionListComponent.vue';

const router = useRouter();

const handleRowClick = (item) => {
  router.push({ name: 'InterventionDetail', params: { id: item.id } });
};
</script>
