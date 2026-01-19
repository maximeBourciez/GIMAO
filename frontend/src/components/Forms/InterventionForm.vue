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
					<v-col cols="12" md="6">
						<FormSelect
							v-model="formData.equipement_id"
							field-name="equipement_id"
							label="Équipement"
							:items="equipments"
							item-title="designation"
							item-value="id"
							:disabled="equipementReadOnly"
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

			<!-- Détails -->
			<v-sheet class="pa-4 mb-4" elevation="1" rounded>
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

			<!-- Affectation -->
			<v-sheet class="pa-4 mb-4" elevation="1" rounded>
				<h4 class="mb-3">Affectation</h4>
				<v-row dense>
					<v-col cols="12" md="6">
						<FormSelect
							v-model="formData.responsable_id"
							field-name="responsable_id"
							label="Responsable"
							:items="responsableItems"
							item-title="label"
							item-value="id"
							:disabled="responsableReadOnly"
						/>
					</v-col>

					<v-col cols="12" md="6">
						<FormSelect
							v-model="formData.utilisateur_assigne_ids"
							field-name="utilisateur_assigne_ids"
							label="Techniciens assignés"
							:items="assignableUserItems"
							item-title="label"
							item-value="id"
							multiple
							chips
							clearable
						/>
					</v-col>
				</v-row>
			</v-sheet>

			<!-- Consommables -->
			<v-sheet class="pa-4 mb-4" elevation="1" rounded>
				<h4 class="mb-3">Consommables</h4>
				<v-row
					v-for="(c, index) in consommableLines"
					:key="index"
					dense
					class="mb-2"
				>
					<v-col cols="12" md="7">
						<FormSelect
							v-model="c.consommable_id"
							:field-name="`consommable_${index}`"
							label="Consommable"
							:items="getAvailableConsommablesForIndex(index)"
							item-title="designation"
							item-value="id"
							clearable
							@focus="markTouched('consommable', index)"
							:error="shouldShowConsommableError(index) && Boolean(getConsommableLineError(index))"
							:error-messages="shouldShowConsommableError(index) && getConsommableLineError(index) ? [getConsommableLineError(index)] : []"
						/>
					</v-col>

					<v-col cols="10" md="4">
						<FormField
							v-model.number="c.quantite_utilisee"
							:field-name="`quantite_utilisee_${index}`"
							type="number"
							label="Quantité"
							placeholder="1"
							min="0"
							step="1"
							@focus="markTouched('quantite', index)"
							:error="Boolean(getQuantiteLineError(index))"
							:error-messages="getQuantiteLineError(index) ? [getQuantiteLineError(index)] : []"
						/>
					</v-col>

					<v-col cols="2" md="1" class="d-flex align-center justify-center">
						<v-btn
							icon="mdi-delete"
							size="small"
							color="error"
							variant="text"
							@click="removeConsommableLine(index)"
						/>
					</v-col>
				</v-row>

				<v-row dense>
					<v-col cols="12">
						<v-btn
							color="primary"
							variant="text"
							prepend-icon="mdi-plus"
							@click="addConsommableLine"
						>
							Ajouter un consommable
						</v-btn>
					</v-col>
				</v-row>
			</v-sheet>

			<!-- Documents -->
			<v-sheet v-if="typeDocumentItems.length" class="pa-4 mb-4" elevation="1" rounded>
				<h4 class="mb-3">Documents</h4>
				<DocumentForm v-model="formData.documents" :type-documents="typeDocumentItems" />
			</v-sheet>
		</template>
	</BaseForm>
</template>

<script setup>
import { computed, reactive, watch } from 'vue';
import { BaseForm, FormField, FormSelect, FormTextarea } from '@/components/common';
import DocumentForm from '@/components/Forms/DocumentForm.vue';

const props = defineProps({
	modelValue: {
		type: Object,
		required: true
	},
	equipementReadOnly: {
		type: Boolean,
		default: false
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
	consommables: {
		type: Array,
		default: () => []
	},
	typeDocuments: {
		type: Array,
		default: () => []
	},
	responsableReadOnly: {
		type: Boolean,
		default: false
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

const consommableItems = computed(() => props.consommables || []);
const typeDocumentItems = computed(() => props.typeDocuments || []);

const touched = reactive({
	consommable: {},
	quantite: {},
});

const markTouched = (type, index) => {
	if (type === 'consommable') touched.consommable[index] = true;
	if (type === 'quantite') touched.quantite[index] = true;
};

const ensureConsommablesLines = () => {
	if (!formData.value) return;
	if (!Array.isArray(formData.value.consommables)) {
		formData.value.consommables = [];
	}
	if (formData.value.consommables.length === 0) {
		formData.value.consommables.push({ consommable_id: null, quantite_utilisee: null });
	}
};

watch(
	() => formData.value,
	() => {
		ensureConsommablesLines();
	},
	{ immediate: true, deep: true }
);

const consommableLines = computed(() => {
	ensureConsommablesLines();
	return formData.value?.consommables || [];
});

const addConsommableLine = () => {
	ensureConsommablesLines();
	formData.value.consommables.push({ consommable_id: null, quantite_utilisee: null });
};

const removeConsommableLine = (index) => {
	ensureConsommablesLines();
	formData.value.consommables.splice(index, 1);
	if (formData.value.consommables.length === 0) {
		formData.value.consommables.push({ consommable_id: null, quantite_utilisee: null });
	}
};

watch(
	() => formData.value?.consommables,
	(lines) => {
		if (!Array.isArray(lines)) return;
		for (const line of lines) {
			if (!line) continue;
			const hasId = line.consommable_id !== null && line.consommable_id !== undefined && line.consommable_id !== '';
			const hasQty = line.quantite_utilisee !== null && line.quantite_utilisee !== undefined && line.quantite_utilisee !== '';
			// Si on choisit un consommable, on initialise la quantité à 1 si vide.
			if (hasId && !hasQty) {
				line.quantite_utilisee = 1;
			}
		}
	},
	{ deep: true }
);

const getSelectedConsommableIds = () => {
	const ids = (Array.isArray(formData.value?.consommables) ? formData.value.consommables : [])
		.map((x) => Number(x?.consommable_id))
		.filter((x) => Number.isFinite(x));
	return ids;
};

const getAvailableConsommablesForIndex = (index) => {
	const selected = getSelectedConsommableIds();
	const currentId = Number(formData.value?.consommables?.[index]?.consommable_id);
	const blocked = new Set(selected.filter((id) => id !== currentId));
	return consommableItems.value.filter((c) => !blocked.has(Number(c?.id)));
};

const getConsommableLineError = (index) => {
	const line = formData.value?.consommables?.[index];
	if (!line) return null;
	const id = line.consommable_id;
	const q = line.quantite_utilisee;

	const hasId = id !== null && id !== undefined && id !== '';
	const hasQty = q !== null && q !== undefined && q !== '';
	if (!hasId && !hasQty) return null;
	// Mais si l'utilisateur a mis une quantité, il faut un consommable.
	if (!hasId && hasQty) return 'Choisir un consommable';

	const numericId = Number(id);
	if (!Number.isFinite(numericId)) return 'Consommable invalide';
	const ids = getSelectedConsommableIds();
	const count = ids.filter((x) => x === numericId).length;
	if (count > 1) return 'Déjà sélectionné';
	return null;
};

const getQuantiteLineError = (index) => {
	const line = formData.value?.consommables?.[index];
	if (!line) return null;
	const id = line.consommable_id;
	const q = line.quantite_utilisee;

	const hasId = id !== null && id !== undefined && id !== '';
	const hasQty = q !== null && q !== undefined && q !== '';
	if (!hasId && !hasQty) return null;
	if (hasId && !hasQty) return 'Quantité requise';
	// Si pas de consommable, on ne force pas la quantité.
	if (!hasId) return null;

	const n = Number(q);
	if (!Number.isFinite(n)) return 'Doit être un nombre';
	if (!Number.isInteger(n)) return 'Doit être un entier';
	if (n < 0) return 'Doit être ≥ 0';
	return null;
};

const shouldShowConsommableError = (index) => Boolean(touched.consommable[index]);

const getDocumentLineError = (doc) => {
	if (!doc) return null;
	const hasExistingId = doc.document_id !== null && doc.document_id !== undefined && doc.document_id !== '';
	if (hasExistingId) {
		const n = Number(doc.document_id);
		if (!Number.isFinite(n)) return 'Document invalide';
		return null;
	}
	const hasName = Boolean((doc.nomDocument ?? '').trim());
	const hasType = doc.typeDocument_id !== null && doc.typeDocument_id !== undefined && doc.typeDocument_id !== '';
	const hasFile = Boolean(doc.file);
	if (!hasName && !hasType && !hasFile) return null;
	if (!hasType) return 'Type requis';
	if (!hasFile) return 'Fichier requis';
	return null;
};


const ROLE_TECHNICIEN = 'Technicien';
const ROLE_RESPONSABLE_GMAO = 'Responsable GMAO';

const getRoleName = (user) => user?.role?.nomRole || user?.role || '';

const assignableUserItems = computed(() =>
	userItems.value.filter((user) => {
		const roleName = getRoleName(user);
		return roleName === ROLE_TECHNICIEN || roleName === ROLE_RESPONSABLE_GMAO;
	})
);

const selectedResponsableItem = computed(() => {
	const selectedId = formData.value?.responsable_id;
	if (!selectedId) return null;
	return (
		userItems.value.find((user) => user.id === selectedId) || {
			id: selectedId,
			label: `Utilisateur #${selectedId}`
		}
	);
});

const responsableItems = computed(() => {
	const base = userItems.value.filter((user) => getRoleName(user) === ROLE_RESPONSABLE_GMAO);
	const selected = selectedResponsableItem.value;
	if (!selected) return base;
	if (base.some((user) => user.id === selected.id)) return base;
	return [selected, ...base];
});

const validationSchema = computed(() => {
	const schema = {
		equipement_id: ['required'],
		nom: ['required', { name: 'minLength', params: [2] }, { name: 'maxLength', params: [200] }],
		type: ['required'],
		responsable_id: ['required'],
		diagnostic: [
			'required',
			{ name: 'minLength', params: [2] },
			{ name: 'maxLength', params: [2000] }
		],
		commentaire: [{ name: 'maxLength', params: [2000] }],
	};

	return schema;
});

const isFormValidForSubmit = computed(() => {
	const nom = (formData.value?.nom ?? '').trim();
	const diagnostic = (formData.value?.diagnostic ?? '').trim();
	const type = formData.value?.type;
	const responsableId = formData.value?.responsable_id;

	if (!formData.value?.equipement_id) return false;
	if (!nom || nom.length < 2 || nom.length > 200) return false;
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

	ensureConsommablesLines();
	const lines = Array.isArray(formData.value?.consommables) ? formData.value.consommables : [];
	for (let i = 0; i < lines.length; i++) {
		if (getConsommableLineError(i)) return false;
		if (getQuantiteLineError(i)) return false;
	}

	const docs = Array.isArray(formData.value?.documents) ? formData.value.documents : [];
	for (const doc of docs) {
		if (getDocumentLineError(doc)) return false;
	}
	return true;
});

const forwardSubmit = (payload) => {
	emit('submit', payload);
};
</script>

