<template>
	<InterventionListComponent
		title="Liste des Bons de Travail"
		variant="auto"
		:statut="selectedStatut"
		:show-create-button="isResponsableGMAO"
		create-button-text="Nouveau bon de travail"
		no-data-text="Aucun bon de travail enregistré"
		@row-click="handleRowClick"
		@create="handleCreate"
	>
		<template #filters>
			<v-select
				v-model="selectedStatut"
				label="Statut"
				:items="statutOptions"
				item-title="title"
				item-value="value"
				density="compact"
				variant="outlined"
				clearable
				hide-details
			/>
		</template>
	</InterventionListComponent>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import InterventionListComponent from '../../components/InterventionListComponent.vue';
import { INTERVENTION_STATUS } from '@/utils/constants';

const router = useRouter();
const store = useStore();

const userRole = computed(() => store.getters.userRole);
const isResponsableGMAO = computed(() => userRole.value === 'Responsable GMAO');

const selectedStatut = ref('');

const statutOptions = computed(() => {
  const options = [{ value: '', title: 'Tous (hors clôturés)' }];
  for (const [value, label] of Object.entries(INTERVENTION_STATUS)) {
    options.push({ value, title: label });
  }
  return options;
});

const handleRowClick = (item) => {
  router.push({ name: 'InterventionDetail', params: { id: item.id } });
};

const handleCreate = () => {
  router.push({ name: 'CreateIntervention' });
};
</script>
