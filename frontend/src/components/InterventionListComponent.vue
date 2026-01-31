<template>
	<BaseListView
		ref="tableContainer"
		:title="title"
		:subtitle="subtitle"
		:headers="vuetifyHeaders"
		:items="filteredItems"
		:sort-by="defaultSortBy"
		:loading="loading"
		:error-message="errorMessage"
		:show-search="showSearch"
		:show-create-button="false"
		:create-button-text="createButtonText"
		:internal-search="internalSearch"
		table-class="bt-table"
		no-data-icon="mdi-wrench-outline"
		:no-data-text="noDataText"
		@row-click="onRowClick"
		@create="$emit('create')"
		@clear-error="errorMessage = ''"
	>
		<template #filters>
			<v-select
				v-if="showStatutFilter"
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
			<slot name="filters"></slot>
		</template>

		<!-- Nom (tronqué si la colonne est trop étroite) -->
		<template #item.nom="{ item }">
			<span
				class="bt-diagnostic-truncate"
				:title="item.nom || ''"
			>
				{{ item.nom || '-' }}
			</span>
		</template>

		<!-- Date d'assignation -->
		<template #item.date_assignation="{ item }">
			{{ formatDateTime(item.date_assignation) }}
		</template>

		<!-- Équipement -->
		<template #item.equipement_designation="{ item }">
			{{ item.equipement_designation || '-' }}
		</template>

		<!-- Diagnostic (tronqué si la colonne est trop étroite) -->
		<template #item.diagnostic="{ item }">
			<span
				class="bt-diagnostic-truncate"
				:title="item.diagnostic || ''"
			>
				{{ item.diagnostic || '-' }}
			</span>
		</template>

		<!-- Date de clôture -->
		<template #item.date_cloture="{ item }">
			{{ item.date_cloture ? formatDateTime(item.date_cloture) : '-' }}
		</template>

		<!-- Date prévue -->
		<template #item.date_prevue="{ item }">
			{{ item.date_prevue ? formatDateTime(item.date_prevue) : '-' }}
		</template>

		<!-- Responsable -->
		<template #item.responsable="{ item }">
			<span v-if="item.responsable">
				{{ formatUserDisplay(item.responsable) || '-' }}
			</span>
			<span v-else>-</span>
		</template>

		<!-- Statut (si présent) -->
		<template #item.statut="{ item }">
			<v-chip
				v-if="item.statut"
				:color="getInterventionStatusColor(item.statut)"
			>
				{{ INTERVENTION_STATUS[item.statut] || item.statut }}
			</v-chip>
			<span v-else>-</span>
		</template>
	</BaseListView>

	<!-- Bouton flottant en bas à droite (comme DI) -->
	<v-btn
		v-if="showCreateButton"
		color="primary"
		size="large"
		icon
		class="floating-add-button"
		elevation="4"
		@click="$emit('create')"
	>
		<v-icon size="large">mdi-plus</v-icon>
		<v-tooltip activator="parent" location="left">
			{{ createButtonText }}
		</v-tooltip>
	</v-btn>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick, onBeforeUnmount } from 'vue';
import { useStore } from 'vuex';
import { useDisplay } from 'vuetify';
import BaseListView from '@/components/common/BaseListView.vue';
import { useApi } from '@/composables/useApi';
import { formatDateTime, getInterventionStatusColor } from '@/utils/helpers';
import { API_BASE_URL, TABLE_HEADERS, INTERVENTION_STATUS } from '@/utils/constants';

const props = defineProps({
	// UI
	title: { type: String, default: 'Liste des bons de travail' },
	subtitle: { type: String, default: '' },
	showSearch: { type: Boolean, default: true },
	internalSearch: { type: Boolean, default: true },
	createButtonText: { type: String, default: 'Créer' },
	noDataText: { type: String, default: 'Aucun bon de travail' },
	showCreateButton: { type: Boolean, default: true },

	// Data sourcing
	items: { type: Array, default: null },
	fetchOnMount: { type: Boolean, default: true },

	// DataTable columns
	variant: {
		type: String,
		default: 'auto',
		validator: (v) => ['auto', 'mobile', 'light', 'full'].includes(v)
	},

	// Filters
	showStatutFilter: { type: Boolean, default: false },
	statut: { type: String, default: '' }
});

const emit = defineEmits(['row-click', 'create', 'loaded']);
const store = useStore();
const showCreateButton = computed(() => store.getters.hasPermission('bt:create'));

const { smAndDown, lgAndUp } = useDisplay();

const api = useApi(API_BASE_URL);

const errorMessage = ref('');
const containerWidth = ref(0);
const tableContainer = ref(null);
let resizeObserver;
let rafId = null;
const cachedItemsWithoutCloture = ref([]);
const cachedItemsWithCloture = ref([]);
const hasFetchedCloture = ref(false);

const selectedStatut = ref('');

const statutOptions = computed(() => {
	const options = [
		{ value: '', title: 'Tous (hors clôturés)' },
		{ value: 'ALL', title: 'Tous (avec clôturés)' }
	];
	for (const [value, label] of Object.entries(INTERVENTION_STATUS)) {
		options.push({ value, title: label });
	}
	return options;
});

const loading = computed(() => api.loading.value);

const allItems = computed(() => {
	if (Array.isArray(props.items)) return props.items;
	
	// Détermine si on a besoin des clôturés
	const activeStatut = props.showStatutFilter ? selectedStatut.value : props.statut;
	const needsCloture = activeStatut === 'CLOTURE' || activeStatut === 'ALL';
	
	// Utilise le cache approprié
	if (needsCloture && hasFetchedCloture.value) {
		return cachedItemsWithCloture.value;
	}
	return cachedItemsWithoutCloture.value;
});

// Filtre côté front :
// - statut vide => comportement historique: on masque les BT clôturés
// - statut 'ALL' => tous les BT (avec clôturés)
// - statut renseigné => on n'affiche que ce statut (y compris CLOTURE)
const filteredItems = computed(() => {
	const items = Array.isArray(allItems.value) ? allItems.value : [];
	const activeStatut = props.showStatutFilter ? selectedStatut.value : props.statut;
	const statutValue = String(activeStatut || '').trim();

	if (!statutValue) {
		return items.filter((i) => i && i.statut !== 'CLOTURE');
	}

	if (statutValue === 'ALL') {
		return items;
	}

	return items.filter((i) => i && i.statut === statutValue);
});

const resolvedVariant = computed(() => {
	if (props.variant === 'auto') {
		if (smAndDown.value) return 'mobile';
		return lgAndUp.value ? 'full' : 'light';
	}
	return props.variant;
});

const baseHeaders = computed(() => {
  // Si on a une largeur de conteneur < 860px et variant auto, on priorise le mobile
  if (containerWidth.value < 860 && props.variant === 'auto') {
    return TABLE_HEADERS.INTERVENTIONS_MOBILE || [];
  }
  
  if (resolvedVariant.value === 'full') return TABLE_HEADERS.INTERVENTIONS || [];
  if (resolvedVariant.value === 'mobile') return TABLE_HEADERS.INTERVENTIONS_MOBILE || [];
  return TABLE_HEADERS.INTERVENTIONS_LIGHT || [];
});

// Vuetify 3 expects `key` in headers; repo constants use `value`.
const vuetifyHeaders = computed(() => {
	return baseHeaders.value.map((h) => ({
		title: h.title,
		key: h.key || h.value,
		value: h.value, // harmless if present
		align: h.align,
		sortable: h.sortable,
		width: h.width,
		maxWidth: h.maxWidth,
	}));
});

const defaultSortBy = [{ key: 'id', order: 'desc' }];

const fetchBonsTravail = async ({ includeCloture } = { includeCloture: false }) => {
	if (Array.isArray(props.items)) return;
	if (!props.fetchOnMount) return;

	errorMessage.value = '';
	try {
		if (includeCloture) {
			await api.get('bons-travail', { cloture: true });
			cachedItemsWithCloture.value = api.data.value || [];
			hasFetchedCloture.value = true;
		} else {
			await api.get('bons-travail');
			cachedItemsWithoutCloture.value = api.data.value || [];
		}

		emit('loaded', allItems.value);
	} catch (error) {
		errorMessage.value = 'Erreur lors du chargement des bons de travail';
	}
};

const onRowClick = (item) => {
	emit('row-click', item);
};

const formatUserDisplay = (user) => {
	if (!user) return '';
	const prenom = String(user.prenom || '').trim();
	const nomFamille = String(user.nomFamille || '').trim();
	if (prenom || nomFamille) return `${prenom} ${nomFamille}`.trim();
	const nomUtilisateur = String(user.nomUtilisateur || '').trim();
	return nomUtilisateur || '';
};

const observeTableContainer = () => {
  if (!resizeObserver) return;
  if (tableContainer.value && tableContainer.value.$el) {
    const tableEl = tableContainer.value.$el.querySelector('.v-data-table') || tableContainer.value.$el;
    if (tableEl) {
      try {
        resizeObserver.observe(tableEl);
      } catch (e) {
        console.warn('ResizeObserver observe failed:', e);
      }
    }
  }
};

watch(
	() => [props.fetchOnMount],
	() => {
		fetchBonsTravail({ includeCloture: false });
	}
);

watch(
	() => props.showStatutFilter ? selectedStatut.value : props.statut,
	(newStatut) => {
		// On fetch les clôturés une seule fois si nécessaire
		const next = String(newStatut || '').trim();
		const needsCloture = next === 'CLOTURE' || next === 'ALL';

		// Fetch uniquement si on a besoin des clôturés et qu'on ne les a pas encore
		if (needsCloture && !hasFetchedCloture.value) {
			fetchBonsTravail({ includeCloture: true });
		}
	}
);

onMounted(() => {
	fetchBonsTravail({ includeCloture: false });
	
	// Initialise l'observateur de redimensionnement
	try {
		resizeObserver = new ResizeObserver(entries => {
			if (entries && entries[0]) {
				// Utiliser requestAnimationFrame pour éviter les boucles infinies
				if (rafId) cancelAnimationFrame(rafId);
				rafId = requestAnimationFrame(() => {
					const entry = entries[0];
					containerWidth.value = Math.round(entry.contentRect.width);
				});
			}
		});
		
		// Observe le conteneur du tableau
		nextTick(() => {
			observeTableContainer();
		});
	} catch (e) {
		console.warn('ResizeObserver initialization failed:', e);
	}
});

onBeforeUnmount(() => {
	if (rafId) {
		cancelAnimationFrame(rafId);
		rafId = null;
	}
	if (resizeObserver) {
		try {
			resizeObserver.disconnect();
		} catch (e) {
			console.warn('ResizeObserver disconnect failed:', e);
		}
		resizeObserver = null;
	}
});
</script>

<style scoped>
.floating-add-button {
	position: fixed !important;
	bottom: 24px;
	right: 24px;
	z-index: 100;
}

.floating-add-button:hover {
	transform: scale(1.1);
	transition: transform 0.2s ease;
}
</style>

<style scoped>
.bt-diagnostic-truncate {
	display: block;
	max-width: 100%;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

:deep(.bt-table .v-table__wrapper > table) {
	table-layout: fixed;
	width: 100%;
}

:deep(.bt-table td) {
	overflow: hidden;
}
</style>