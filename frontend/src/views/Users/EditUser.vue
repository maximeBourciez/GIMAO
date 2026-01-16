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
			<v-sheet
				class="pa-4 mb-4 user-photo-dropzone"
				elevation="1"
				rounded
				:class="{ 'user-photo-dropzone--active': isPhotoDragActive }"
				@dragenter.prevent="onPhotoDragEnter"
				@dragover.prevent="onPhotoDragOver"
				@dragleave.prevent="onPhotoDragLeave"
				@drop.prevent="onPhotoDrop"
			>
				<div class="d-flex align-center justify-space-between">
					<div class="d-flex align-center" style="min-width: 0;">
						<v-avatar size="64" color="grey lighten-3" class="mr-3">
							<v-img v-if="displayPhotoUrl" :src="displayPhotoUrl" cover />
							<v-icon v-else color="grey darken-1">mdi-account</v-icon>
						</v-avatar>

						<div style="min-width: 0;">
							<div class="text-body-1 font-weight-medium">Photo de profil</div>
							<div class="caption" :class="photoError ? 'error--text' : 'grey--text'">
								{{ photoError || photoFileLabel }}
							</div>
						</div>
					</div>

					<div class="d-flex align-center" style="gap: 8px;">
						<template v-if="hasPhoto">
							<v-btn icon small title="Supprimer la photo" @click.stop="deletePhoto">
								<v-icon>mdi-delete</v-icon>
							</v-btn>

							<v-btn icon small title="Télécharger la photo" @click.stop="downloadPhoto">
								<v-icon>mdi-download</v-icon>
							</v-btn>

							<v-btn icon small title="Modifier la photo" @click.stop="triggerPhotoPicker">
								<v-icon>mdi-pencil</v-icon>
							</v-btn>
						</template>

						<v-btn v-else icon small title="Téléverser une photo" @click.stop="triggerPhotoPicker">
							<v-icon>mdi-upload</v-icon>
						</v-btn>
					</div>
				</div>

				<input
					ref="photoInput"
					type="file"
					accept="image/*"
					class="d-none"
					@change="onPhotoPicked"
				/>
			</v-sheet>

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
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import BaseForm from '@/components/common/BaseForm.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL, MEDIA_BASE_URL } from '@/utils/constants';

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
	photoProfil: null,
});

const existingPhotoPath = ref('');
const removeExistingPhoto = ref(false);

const photoInput = ref(null);
const isPhotoDragActive = ref(false);
const photoPreviewUrl = ref('');
const photoError = ref('');

const existingPhotoUrl = computed(() => {
	if (!existingPhotoPath.value) return '';
	return `${MEDIA_BASE_URL}${existingPhotoPath.value}`;
});

const displayPhotoUrl = computed(() => {
	if (photoPreviewUrl.value) return photoPreviewUrl.value;
	if (removeExistingPhoto.value) return '';
	return existingPhotoUrl.value;
});

const canDeletePhoto = computed(() => {
	return !!photoPreviewUrl.value || (!!existingPhotoPath.value && !removeExistingPhoto.value);
});

const photoFileLabel = computed(() => {
	const file = form.value.photoProfil;
	if (file instanceof File) return file.name;
	if (existingPhotoPath.value && !removeExistingPhoto.value) return existingPhotoPath.value.split('/').pop();
	return 'Aucun fichier';
});

const hasPhoto = computed(() => {
	return !!displayPhotoUrl.value;
});

const revokePhotoPreviewUrl = () => {
	if (photoPreviewUrl.value) {
		URL.revokeObjectURL(photoPreviewUrl.value);
		photoPreviewUrl.value = '';
	}
};

const setPhotoFile = (file) => {
	photoError.value = '';
	if (!file) {
		form.value.photoProfil = null;
		revokePhotoPreviewUrl();
		if (photoInput.value) photoInput.value.value = '';
		return;
	}

	if (!file.type || !file.type.startsWith('image/')) {
		photoError.value = 'Le fichier doit être une image.';
		return;
	}

	form.value.photoProfil = file;
	removeExistingPhoto.value = false;
	revokePhotoPreviewUrl();
	photoPreviewUrl.value = URL.createObjectURL(file);
};

const triggerPhotoPicker = () => {
	photoError.value = '';
	photoInput.value?.click?.();
};

const clearPhoto = () => {
	setPhotoFile(null);
};

const deletePhoto = () => {
	// Si une nouvelle photo est sélectionnée (preview), on la retire.
	if (photoPreviewUrl.value) {
		clearPhoto();
		return;
	}

	// Sinon on marque la suppression de la photo existante.
	if (existingPhotoPath.value) {
		removeExistingPhoto.value = true;
		existingPhotoPath.value = '';
	}
};

const downloadPhoto = () => {
	const url = displayPhotoUrl.value;
	if (!url) return;
	const filename = form.value.photoProfil instanceof File
		? form.value.photoProfil.name
		: existingPhotoPath.value
			? existingPhotoPath.value.split('/').pop()
			: 'photo-profil';
	const link = document.createElement('a');
	link.href = url;
	link.download = filename;
	link.rel = 'noopener';
	link.target = '_blank';
	document.body.appendChild(link);
	link.click();
	link.remove();
};

const onPhotoPicked = (e) => {
	const file = e?.target?.files?.[0];
	setPhotoFile(file || null);
};

const onPhotoDragEnter = () => {
	isPhotoDragActive.value = true;
};
const onPhotoDragOver = () => {
	isPhotoDragActive.value = true;
};
const onPhotoDragLeave = () => {
	isPhotoDragActive.value = false;
};
const onPhotoDrop = (e) => {
	isPhotoDragActive.value = false;
	const file = e?.dataTransfer?.files?.[0];
	setPhotoFile(file || null);
};

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
			photoProfil: null,
		};
		existingPhotoPath.value = data?.photoProfil ?? '';
		removeExistingPhoto.value = false;
		revokePhotoPreviewUrl();
		photoError.value = '';
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
		const payloadHasFile = form.value.photoProfil instanceof File;
		const payload = payloadHasFile ? new FormData() : {};

		const setField = (key, value) => {
			if (payload instanceof FormData) {
				payload.append(key, value);
			} else {
				payload[key] = value;
			}
		};

		setField('nomUtilisateur', form.value.nomUtilisateur);
		setField('prenom', form.value.prenom);
		setField('nomFamille', form.value.nomFamille);
		setField('email', form.value.email);
		setField('actif', String(!!form.value.actif));
		setField('role_id', String(form.value.role_id));
		if (payloadHasFile) {
			payload.append('photoProfil', form.value.photoProfil);
		} else if (removeExistingPhoto.value) {
			setField('photoProfil', null);
		}

		// Envoi simple DRF : JSON si pas de fichier, sinon multipart
		await api.put(`utilisateurs/${userId}/`, payload);

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

onBeforeUnmount(() => {
	revokePhotoPreviewUrl();
});
</script>

<style scoped>
.user-photo-dropzone {
	border-style: dashed !important;
	cursor: pointer;
	transition: border-color 0.15s ease, background-color 0.15s ease;
}

.user-photo-dropzone--active {
	border-color: #1976d2 !important;
	background-color: rgba(25, 118, 210, 0.05);
}
</style>
