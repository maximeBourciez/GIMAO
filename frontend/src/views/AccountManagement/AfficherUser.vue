<template>
	<BaseDetailView
		:data="userData"
		:loading="isLoading"
		:error-message="errorMessage"
		:success-message="successMessage"
		:title="'Détail de l\'utilisateur'"
		:auto-display="false"
		:show-edit-button="false"
		:show-delete-button="false"
		@clear-error="errorMessage = ''"
		@clear-success="successMessage = ''"
	>
		<template #default="{ data }">
			<v-row v-if="data" dense>
				<!-- Informations générales -->
				<v-col cols="12">
					<h3 class="text-h6 mb-3">Informations générales</h3>
				</v-col>

				<v-col cols="12" md="6">
					<strong>Nom complet</strong>
					<div>{{ fullName || '-' }}</div>
				</v-col>

				<v-col cols="12" md="6">
					<strong>Nom d'utilisateur</strong>
					<div>{{ data.nomUtilisateur || '-' }}</div>
				</v-col>

				<v-col cols="12" md="6">
					<strong>Email</strong>
					<div>{{ data.email || '-' }}</div>
				</v-col>

				<v-col cols="12" md="6">
					<strong>Rôle</strong>
					<div>
						<v-chip color="primary" variant="outlined" size="small">
							{{ data.role?.nomRole || '-' }}
						</v-chip>
					</div>
				</v-col>

				<v-col cols="12" md="6">
					<strong>Actif</strong>
					<div>
						<v-chip :color="data.actif ? 'success' : 'error'" variant="outlined" size="small">
							{{ data.actif ? 'Oui' : 'Non' }}
						</v-chip>
					</div>
				</v-col>

				<v-col cols="12" md="6">
					<strong>Dernière connexion</strong>
					<div>{{ formatDateTime(data.derniereConnexion) }}</div>
				</v-col>

				<v-col cols="12" md="6">
					<strong>Date de création</strong>
					<div>{{ formatDateTime(data.dateCreation) }}</div>
				</v-col>

				<!-- Rôles supplémentaires -->
				<v-col cols="12" class="mt-4">
					<h3 class="text-h6 mb-3">Rôles supplémentaires</h3>
				</v-col>

				<v-col cols="12">
					<div v-if="Array.isArray(data.avoirs) && data.avoirs.length" class="d-flex flex-wrap gap-2">
						<template v-for="avoir in data.avoirs" :key="avoir.id">
							<v-chip
								v-for="role in (avoir.roles || [])"
								:key="`${avoir.id}-${role.id}`"
								color="secondary"
								variant="outlined"
								size="small"
							>
								{{ role.nomRole }}
							</v-chip>
						</template>
					</div>
					<v-alert v-else type="info" variant="outlined">
						Aucun rôle supplémentaire.
					</v-alert>
				</v-col>

				<!-- Logs récents -->
				<v-col cols="12" class="mt-4">
					<h3 class="text-h6 mb-3">Logs récents</h3>
				</v-col>

				<v-col cols="12">
					<v-list v-if="Array.isArray(data.logs_recents) && data.logs_recents.length" density="compact">
						<v-list-item v-for="log in data.logs_recents" :key="log.id">
							<v-list-item-title>
								{{ log.type }} — {{ log.nomTable }}
							</v-list-item-title>
							<v-list-item-subtitle>
								{{ formatDateTime(log.date) }}
							</v-list-item-subtitle>
						</v-list-item>
					</v-list>
					<v-alert v-else type="info" variant="outlined">
						Aucun log récent.
					</v-alert>
				</v-col>
			</v-row>

			<v-row v-else>
				<v-col>
					<v-alert type="info" variant="outlined">
						Aucune donnée disponible pour cet utilisateur.
					</v-alert>
				</v-col>
			</v-row>
		</template>
	</BaseDetailView>

	<!-- Bouton flottant pour modifier -->
	<v-btn
		color="primary"
		size="large"
		icon
		class="floating-edit-button"
		elevation="4"
		@click="editUser"
	>
		<v-icon size="large">mdi-pencil</v-icon>
		<v-tooltip activator="parent" location="left">
			Modifier l'utilisateur
		</v-tooltip>
	</v-btn>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import BaseDetailView from '@/components/common/BaseDetailView.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants.js';

const route = useRoute();
const router = useRouter();
const userId = route.params.id;

const userData = ref(null);
const isLoading = ref(true);
const errorMessage = ref('');
const successMessage = ref('');

const api = useApi(API_BASE_URL);

const fullName = computed(() => {
	const prenom = userData.value?.prenom ?? '';
	const nomFamille = userData.value?.nomFamille ?? '';
	return `${prenom} ${nomFamille}`.trim();
});

const formatDateTime = (value) => {
	if (!value) return '-';
	const date = new Date(value);
	if (Number.isNaN(date.getTime())) return String(value);
	return new Intl.DateTimeFormat('fr-FR', {
		dateStyle: 'short',
		timeStyle: 'short',
	}).format(date);
};

const loadUserData = async () => {
	isLoading.value = true;
	errorMessage.value = '';

	if (!userId) {
		errorMessage.value = "Impossible d'afficher l'utilisateur : id manquant dans l'URL.";
		userData.value = null;
		isLoading.value = false;
		return;
	}

	try {
		// DRF DefaultRouter utilise des URLs avec slash final : /api/utilisateurs/:id/
		userData.value = await api.get(`utilisateurs/${userId}/`);
	} catch (error) {
		console.error('Error loading user data:', error);
		errorMessage.value = "Erreur lors du chargement de l'utilisateur.";
		userData.value = null;
	} finally {
		isLoading.value = false;
	}
};

onMounted(() => {
	loadUserData();
});

const editUser = () => {
	if (!userId) {
		errorMessage.value = "Impossible de modifier l'utilisateur : id manquant dans l'URL.";
		return;
	}

	router.push({
		name: 'ModifierUser',
		params: { id: userId },
	});
};
</script>

<style scoped>
.gap-2 {
	gap: 8px;
}

.floating-edit-button {
	position: fixed;
	bottom: 24px;
	right: 24px;
	z-index: 1000;
}
</style>
