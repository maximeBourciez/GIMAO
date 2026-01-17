<template>
	<BaseForm
		v-model="formData"
		v-bind="mergedBaseFormProps"
		:validation-schema="validationSchema"
		:loading="state.loading"
		:error-message="state.errorMessage"
		:success-message="state.successMessage"
		:custom-disabled="!isFormValidForSubmit"
		:handleSubmit="forwardSubmit"
		actions-container-class="d-flex justify-end gap-2 mt-2"
		submit-button-class="mt-2"
		cancel-button-class="mt-2 mr-3"
		@cancel="emit('cancel')"
		@clear-error="emit('clear-error')"
		@clear-success="emit('clear-success')"
	>
		<template #default>
			<!-- Informations générales -->
			<v-sheet class="pa-4 mb-4" elevation="1" rounded>
				<h4 class="mb-3">Bon de travail</h4>
				<v-row dense>
					<v-col v-if="showEquipement" cols="12" md="6">
						<FormSelect
							v-model="formData.equipement_id"
							field-name="equipement_id"
							label="Équipement"
							:items="equipments"
							item-title="designation"
							item-value="id"
						/>
					</v-col>

					<v-col cols="12" md="6">
						<FormField
							v-model="formData.nom"
							field-name="nom"
							label="Nom du bon de travail"
							placeholder="Saisir le nom"
							:maxlength="MAX_NOM_LENGTH"
							counter
						/>
					</v-col>

					<v-col cols="12" md="6">
						<FormSelect
							v-model="formData.type"
							field-name="type"
							label="Type"
							:items="typeItems"
							item-title="label"
							item-value="value"
						/>
					</v-col>

					<v-col cols="12" md="6">
						<FormField
							v-model="formData.date_prevue"
							field-name="date_prevue"
							label="Date prévue"
							type="datetime-local"
							clearable
						/>
					</v-col>
				</v-row>
			</v-sheet>

			<!-- Affectation -->
			<v-sheet class="pa-4 mb-4" elevation="1" rounded>
				<h4 class="mb-3">Affectation</h4>
				<v-row dense>
					<v-col cols="12" md="6">
						<FormSelect
							v-model="formData.responsable_id"
							field-name="responsable_id"
							label="Responsable"
							:items="userItems"
							item-title="label"
							item-value="id"
						/>
					</v-col>

					<v-col cols="12" md="6">
						<FormSelect
							v-model="formData.utilisateur_assigne_ids"
							field-name="utilisateur_assigne_ids"
							label="Utilisateurs assignés"
							:items="userItems"
							item-title="label"
							item-value="id"
							multiple
							chips
							clearable
						/>
					</v-col>
				</v-row>
			</v-sheet>

			<!-- Détails -->
			<v-sheet class="pa-4" elevation="1" rounded>
				<h4 class="mb-3">Détails</h4>
				<v-row dense>
					<v-col cols="12">
						<FormTextarea
							v-model="formData.diagnostic"
							field-name="diagnostic"
							label="Diagnostic"
							placeholder="Saisir un diagnostic"
							rows="2"
							:maxlength="MAX_TEXT_LENGTH"
							counter
						/>
					</v-col>

					<v-col cols="12">
						<FormTextarea
							v-model="formData.commentaire"
							field-name="commentaire"
							label="Commentaire"
							placeholder="Saisir un commentaire"
							rows="4"
							:maxlength="MAX_TEXT_LENGTH"
							counter
						/>
					</v-col>
				</v-row>
			</v-sheet>
		</template>
	</BaseForm>
</template>

<script setup>
import { computed } from 'vue';
import { BaseForm, FormField, FormSelect, FormTextarea } from '@/components/common';

const props = defineProps({
	modelValue: {
		type: Object,
		required: true
	},
	equipments: {
		type: Array,
		default: () => []
	},
	baseFormProps: {
		type: Object,
		default: () => ({})
	},
	users: {
		type: Array,
		default: () => []
	},
	state: {
		type: Object,
		default: () => ({
			loading: false,
			errorMessage: '',
			successMessage: ''
		})
	}

});

const emit = defineEmits(['update:modelValue', 'submit', 'cancel', 'clear-error', 'clear-success']);

const formData = computed({
	get: () => props.modelValue,
	set: (value) => emit('update:modelValue', value)
});

const mergedBaseFormProps = computed(() => ({
	title: props.baseFormProps?.title ?? 'Bon de travail',
	submitButtonText: props.baseFormProps?.submitButtonText ?? 'Valider',
	submitButtonColor: props.baseFormProps?.submitButtonColor ?? 'primary',
	elevation: props.baseFormProps?.elevation ?? 2,
	cardClass: props.baseFormProps?.cardClass ?? 'rounded-lg',
	contentClass: props.baseFormProps?.contentClass ?? 'pa-6'
}));

const typeItems = [
	{ label: 'Correctif', value: 'CORRECTIF' },
	{ label: 'Préventif', value: 'PREVENTIF' }
];

const formatUserLabel = (user) => {
	const parts = [user?.prenom, user?.nomFamille].filter(Boolean);
	if (parts.length) return parts.join(' ');
	return user?.nomUtilisateur || user?.email || `Utilisateur #${user?.id}`;
};

const userItems = computed(() =>
	(props.users || []).map((user) => ({
		...user,
		label: formatUserLabel(user)
	}))
);

const showEquipement = computed(() => Array.isArray(props.equipments) && props.equipments.length > 0);

const validationSchema = computed(() => {
	const schema = {
		nom: ['required', { name: 'minLength', params: [2] }, { name: 'maxLength', params: [200] }],
		type: ['required'],
		responsable_id: ['required'],
		diagnostic: [
			'required',
			{ name: 'minLength', params: [2] },
			{ name: 'maxLength', params: [2000] }
		],
		commentaire: [{ name: 'maxLength', params: [2000] }]
	};

	if (showEquipement.value) {
		schema.equipement_id = ['required'];
	}

	return schema;
});

const isFormValidForSubmit = computed(() => {
	const nom = (formData.value?.nom ?? '').trim();
	const diagnostic = (formData.value?.diagnostic ?? '').trim();
	const type = formData.value?.type;
	const responsableId = formData.value?.responsable_id;

	if (showEquipement.value && !formData.value?.equipement_id) return false;
	if (!nom || nom.length < 2 || nom.length > 2000) return false;
	if (!type) return false;
	if (!responsableId) return false;
	if (!diagnostic || diagnostic.length < 2 || diagnostic.length > 2000) return false;

	const commentaire = (formData.value?.commentaire ?? '').trim();
	if (commentaire.length > 2000) return false;

	// date_prevue est optionnelle; si renseignée, on vérifie juste le format minimal
	const datePrevue = formData.value?.date_prevue;
	if (datePrevue && typeof datePrevue !== 'string') return false;
	// datetime-local renvoie typiquement 'YYYY-MM-DDTHH:mm'
	if (datePrevue && String(datePrevue).length < 16) return false;
	return true;
});

const forwardSubmit = (payload) => {
	emit('submit', payload);
};
</script>

