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

			<v-sheet class="pa-4 mt-4" elevation="1" rounded>
				<h4 class="mb-3">Mot de passe</h4>
				<v-row dense>
					<v-col cols="12" md="6">
						<v-text-field
							v-model="passwordForm.ancien"
							label="Ancien mot de passe"
							type="password"
							outlined
							dense
							hint="Laisser vide si l'utilisateur n'a pas encore de mot de passe (première définition)."
							persistent-hint
						/>
					</v-col>

					<v-col cols="12" md="6" />

					<v-col cols="12" md="6">
						<v-text-field
							v-model="passwordForm.nouveau"
							label="Nouveau mot de passe"
							type="password"
							outlined
							dense
							:rules="[(v) => !v || v.length >= 8 || '8 caractères minimum']"
						/>
					</v-col>

					<v-col cols="12" md="6">
						<v-text-field
							v-model="passwordForm.confirmation"
							label="Confirmation nouveau mot de passe"
							type="password"
							outlined
							dense
							:rules="[(v) => !passwordForm.nouveau || v === passwordForm.nouveau || 'Les mots de passe ne correspondent pas']"
						/>
					</v-col>

					<v-col cols="12" class="d-flex justify-end">
						<v-btn
							color="primary"
							:loading="isChangingPassword"
							:disabled="isSaving || isChangingPassword"
							type="button"
							@click="handlePasswordUpdate"
						>
							Mettre à jour le mot de passe
						</v-btn>
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
const isChangingPassword = ref(false);
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

const passwordForm = ref({
	ancien: '',
	nouveau: '',
	confirmation: '',
});

const roleOptions = computed(() =>
	(roles.value || []).map((r) => ({
		label: r.nomRole,
		value: r.id,
	}))
);

const isValidEmail = (email) => {
	return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
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
			router.push({ name: 'UserDetail', params: { id: userId } });
		}, 800);
	} catch (e) {
		console.error('Error updating user:', e);
		saveErrorMessage.value = "Erreur lors de la modification de l'utilisateur.";
	} finally {
		isSaving.value = false;
	}
};

const handlePasswordUpdate = async () => {
	if (!userId) {
		saveErrorMessage.value = "Impossible de modifier le mot de passe : id manquant dans l'URL.";
		return;
	}

	saveErrorMessage.value = '';
	successMessage.value = '';

	const ancien = passwordForm.value.ancien;
	const nouveau = passwordForm.value.nouveau;
	const confirmation = passwordForm.value.confirmation;

	const anyPasswordFieldFilled = !!(ancien || nouveau || confirmation);
	if (!anyPasswordFieldFilled) {
		saveErrorMessage.value = 'Veuillez renseigner au moins le nouveau mot de passe.';
		return;
	}

	if (!nouveau || nouveau.length < 8) {
		saveErrorMessage.value = 'Le nouveau mot de passe doit contenir au moins 8 caractères.';
		return;
	}

	if (!confirmation) {
		saveErrorMessage.value = 'La confirmation du nouveau mot de passe est requise.';
		return;
	}

	if (nouveau !== confirmation) {
		saveErrorMessage.value = 'Les mots de passe ne correspondent pas.';
		return;
	}

	isChangingPassword.value = true;
	try {
		// Si l'ancien mot de passe est fourni, on utilise l'endpoint de changement.
		if (ancien && ancien.trim() !== '') {
			await api.post(`utilisateurs/${userId}/changer_mot_de_passe/`, {
				ancien_motDePasse: ancien,
				nouveau_motDePasse: nouveau,
				nouveau_motDePasse_confirmation: confirmation,
			});
			successMessage.value = 'Mot de passe mis à jour avec succès.';
		} else {
			// Sinon, on tente la première définition (utilisateur sans mot de passe, jamais connecté).
			if (!form.value.nomUtilisateur) {
				saveErrorMessage.value = "Nom d'utilisateur manquant : impossible de définir un mot de passe.";
				return;
			}

			await api.post('utilisateurs/definir_mot_de_passe/', {
				nomUtilisateur: form.value.nomUtilisateur,
				nouveau_motDePasse: nouveau,
				nouveau_motDePasse_confirmation: confirmation,
			});
			successMessage.value = 'Mot de passe défini avec succès.';
		}

		passwordForm.value = { ancien: '', nouveau: '', confirmation: '' };
	} catch (e) {
		const detail = e?.response?.data?.detail;
		if (typeof detail === 'string' && detail.trim() !== '') {
			saveErrorMessage.value = detail;
		} else {
			saveErrorMessage.value = "Erreur lors de la mise à jour du mot de passe.";
		}
	} finally {
		isChangingPassword.value = false;
	}
};

const goBack = () => {
	if (!userId) {
		router.push({ name: 'UserList' });
		return;
	}
	router.push({ name: 'UserDetail', params: { id: userId } });
};

onMounted(async () => {
	await Promise.all([loadRoles(), loadUser()]);
});
</script>
