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
							<v-img v-if="photoPreviewUrl" :src="photoPreviewUrl" cover />
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
							<v-btn icon small title="Supprimer la photo" @click.stop="clearPhoto">
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
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import BaseForm from '@/components/common/BaseForm.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';
import { getUserCreateErrorMessage } from '@/utils/drfErrors';

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
	photoProfil: null,
});

const photoInput = ref(null);
const isPhotoDragActive = ref(false);
const photoPreviewUrl = ref('');
const photoError = ref('');

const photoFileLabel = computed(() => {
	const file = form.value.photoProfil;
	if (file instanceof File) return file.name;
	return 'Aucun fichier';
});

const hasPhoto = computed(() => {
	return form.value.photoProfil instanceof File && !!photoPreviewUrl.value;
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
	revokePhotoPreviewUrl();
	photoPreviewUrl.value = URL.createObjectURL(file);
};

const triggerPhotoPicker = () => {
	photoError.value = '';
	photoInput.value?.click?.();
};

const downloadPhoto = () => {
	if (!photoPreviewUrl.value) return;
	const filename = form.value.photoProfil instanceof File ? form.value.photoProfil.name : 'photo-profil';
	const link = document.createElement('a');
	link.href = photoPreviewUrl.value;
	link.download = filename;
	link.rel = 'noopener';
	link.target = '_blank';
	document.body.appendChild(link);
	link.click();
	link.remove();
};

const clearPhoto = () => {
	setPhotoFile(null);
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

const handleSubmit = async () => {
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
		setField('role', String(form.value.role));
		if (payloadHasFile) {
			payload.append('photoProfil', form.value.photoProfil);
		}

		const created = await api.post('utilisateurs/', payload);

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
		saveErrorMessage.value = getUserCreateErrorMessage(e);
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
