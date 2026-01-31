<template>
	<InterventionListComponent
		title="Liste des Bons de Travail"
		variant="auto"
		show-statut-filter
		:show-create-button="isResponsableGMAO"
		create-button-text="Nouveau bon de travail"
		no-data-text="Aucun bon de travail enregistré"
		@row-click="handleRowClick"
		@create="handleCreate"
	/>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import InterventionListComponent from '../../components/InterventionListComponent.vue';

const router = useRouter();
const store = useStore();

const userRole = computed(() => store.getters.userRole);
const isResponsableGMAO = computed(() => userRole.value === 'Responsable GMAO');

const handleRowClick = (item) => {
  router.push({ name: 'InterventionDetail', params: { id: item.id } });
};

const handleCreate = () => {
  router.push({ name: 'CreateIntervention' });
};
</script>
