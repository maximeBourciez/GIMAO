<template>
  <InterventionListComponent
    title="Liste des Bons de Travail"
    variant="auto"
	:show-create-button="true"
	create-button-text="Nouveau bon de travail"
    no-data-text="Aucun bon de travail enregistré"
    @row-click="handleRowClick"
	@create="handleCreate"
  />
</template>

<script setup>
import { useRouter } from 'vue-router';
import InterventionListComponent from '../../components/InterventionListComponent.vue';

const router = useRouter();

const handleRowClick = (item) => {
  router.push({ name: 'InterventionDetail', params: { id: item.id } });
};

const handleCreate = () => {
  router.push({ name: 'CreateIntervention' });
};
</script>
