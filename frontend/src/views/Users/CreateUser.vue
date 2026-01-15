<template>
	<BaseForm
		title="Créer un utilisateur"
		:loading="isSaving"
		:error-message="saveErrorMessage"
		:success-message="successMessage"
		submit-button-text="Créer l'utilisateur"
		@submit="handleSubmit"
		@cancel="goBack"
		@clear-error="saveErrorMessage = ''"
		@clear-success="successMessage = ''"
		actions-container-class="d-flex justify-end gap-2 mt-2"
	>
		<template #default>
			<v-sheet class="pa-4" elevation="1" rounded>
				<h4 class="mb-3">Informations</h4>
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
							:rules="[(v) => !!v || 'Email requis', (v) => !v || isValidEmail(v) || 'Email invalide']"
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
							v-model="form.role"
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
import { useRouter } from 'vue-router';
import BaseForm from '@/components/common/BaseForm.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const router = useRouter();
const api = useApi(API_BASE_URL);

const isSaving = ref(false);
const saveErrorMessage = ref('');
const successMessage = ref('');

const roles = ref([]);

const form = ref({
	nomUtilisateur: '',
	prenom: '',
	nomFamille: '',
	email: '',
	actif: true,
	role: null,
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

const handleSubmit = async () => {
	isSaving.value = true;
	saveErrorMessage.value = '';
	successMessage.value = '';

	try {
		const created = await api.post('utilisateurs/', {
			nomUtilisateur: form.value.nomUtilisateur,
			prenom: form.value.prenom,
			nomFamille: form.value.nomFamille,
			email: form.value.email,
			actif: form.value.actif,
			role: form.value.role,
		});

		successMessage.value = 'Utilisateur créé avec succès.';
		setTimeout(() => {
			if (created?.id) {
				router.push({ name: 'UserDetail', params: { id: created.id } });
			} else {
				router.push({ name: 'UserList' });
			}
		}, 800);
	} catch (e) {
		console.error('Error creating user:', e);
		saveErrorMessage.value = "Erreur lors de la création de l'utilisateur.";
	} finally {
		isSaving.value = false;
	}
};

const goBack = () => {
	router.push({ name: 'UserList' });
};

onMounted(() => {
	loadRoles();
});
</script>
