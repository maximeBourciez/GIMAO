<template>
	<BaseForm
		title="Modifier l'utilisateur"
		:loading="isSaving"
		:error-message="saveErrorMessage"
		:success-message="successMessage"
		submit-button-text="Enregistrer les modifications"
		@submit="handleSubmit"
		@cancel="goBack"
		@clear-error="saveErrorMessage = ''"
		@clear-success="successMessage = ''"
		actions-container-class="d-flex justify-end gap-2 mt-2"
	>
		<template #default>
			<v-sheet class="pa-4" elevation="1" rounded>
				<h4 class="mb-3">Utilisateur</h4>
				<v-row dense>
					<v-col cols="12" md="6">
						<v-text-field
							v-model="form.nomUtilisateur"
							label="Nom d'utilisateur *"
							outlined
							dense
							:rules="[(v) => (!!v && !!v.trim()) || 'Le nom d\'utilisateur est requis']"
						/>
					</v-col>

					<v-col cols="12" md="6">
						<v-text-field
							v-model="form.email"
							label="Email *"
							outlined
							dense
							:rules="[(v) => !v || isValidEmail(v) || 'Email invalide']"
						/>
					</v-col>

					<v-col cols="12" md="6">
						<v-text-field
							v-model="form.prenom"
							label="Prénom *"
							outlined
							dense
							:rules="[(v) => (!!v && !!v.trim()) || 'Le prénom est requis']"
						/>
					</v-col>

					<v-col cols="12" md="6">
						<v-text-field
							v-model="form.nomFamille"
							label="Nom de famille *"
							outlined
							dense
							:rules="[(v) => (!!v && !!v.trim()) || 'Le nom de famille est requis']"
						/>
					</v-col>

					<v-col cols="12" md="6">
						<v-select
							v-model="form.role_id"
							:items="roleOptions"
							item-title="label"
							item-value="value"
							label="Rôle *"
							outlined
							dense
							:rules="[(v) => !!v || 'Le rôle est requis']"
						/>
					</v-col>

					<v-col cols="12" md="6" class="d-flex align-center">
						<v-checkbox v-model="form.actif" label="Compte actif" dense />
					</v-col>
				</v-row>
			</v-sheet>
		</template>
	</BaseForm>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import BaseForm from '@/components/common/BaseForm.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const route = useRoute();
const router = useRouter();
const api = useApi(API_BASE_URL);

const userId = route.params.id;

const isSaving = ref(false);
const saveErrorMessage = ref('');
const successMessage = ref('');

const roles = ref([]);
const original = ref(null);

const form = ref({
	nomUtilisateur: '',
	prenom: '',
	nomFamille: '',
	email: '',
	actif: true,
	role_id: null,
});

const roleOptions = computed(() =>
	(roles.value || []).map((r) => ({
		label: r.nomRole,
		value: r.id,
	}))
);

const isValidEmail = (email) => {
	return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

const loadRoles = async () => {
	try {
		const result = await api.get('roles/');
		roles.value = Array.isArray(result) ? result : [];
	} catch (e) {
		roles.value = [];
	}
};

const loadUser = async () => {
	if (!userId) {
		saveErrorMessage.value = "Impossible de modifier l'utilisateur : id manquant dans l'URL.";
		return;
	}

	try {
		const data = await api.get(`utilisateurs/${userId}/`);
		form.value = {
			nomUtilisateur: data?.nomUtilisateur ?? '',
			prenom: data?.prenom ?? '',
			nomFamille: data?.nomFamille ?? '',
			email: data?.email ?? '',
			actif: !!data?.actif,
			role_id: data?.role?.id ?? null,
		};
		original.value = JSON.parse(JSON.stringify(form.value));
	} catch (e) {
		console.error('Error loading user for edit:', e);
		saveErrorMessage.value = "Erreur lors du chargement de l'utilisateur.";
	}
};

const handleSubmit = async () => {
	if (!userId) {
		saveErrorMessage.value = "Impossible de modifier l'utilisateur : id manquant dans l'URL.";
		return;
	}

	isSaving.value = true;
	saveErrorMessage.value = '';
	successMessage.value = '';

	try {
		// Envoi d'un payload simple compatible DRF (pas de structure {ancienne/nouvelle})
		await api.put(`utilisateurs/${userId}/`, {
			nomUtilisateur: form.value.nomUtilisateur,
			prenom: form.value.prenom,
			nomFamille: form.value.nomFamille,
			email: form.value.email,
			actif: form.value.actif,
			role_id: form.value.role_id,
		});

		successMessage.value = 'Utilisateur modifié avec succès.';
		setTimeout(() => {
			router.push({ name: 'AfficherUser', params: { id: userId } });
		}, 800);
	} catch (e) {
		console.error('Error updating user:', e);
		saveErrorMessage.value = "Erreur lors de la modification de l'utilisateur.";
	} finally {
		isSaving.value = false;
	}
};

const goBack = () => {
	if (!userId) {
		router.push({ name: 'AccountManagement' });
		return;
	}
	router.push({ name: 'AfficherUser', params: { id: userId } });
};

onMounted(async () => {
	await Promise.all([loadRoles(), loadUser()]);
});
</script>
