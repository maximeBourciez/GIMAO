<template>
	<BaseForm
		v-model="formData"
		v-bind="mergedBaseFormProps"
		:validation-schema="validationSchema"
		:loading="loading"
		:error-message="errorMessage"
		:success-message="successMessage"
		:custom-disabled="!isFormValidForSubmit"
		:handleSubmit="save"
		:custom-cancel-action="close"
		actions-container-class="d-flex justify-end gap-2 mt-2"
		submit-button-class="mt-2"
		cancel-button-class="mt-2 mr-3"
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
						:disabled="isEdit"
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
							:disabled="isEdit"
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

			<!-- Documents -->
			<v-sheet v-if="typeDocumentItems.length" class="pa-4 mb-4" elevation="1" rounded>
				<h4 class="mb-3">Documents</h4>
				<DocumentForm v-model="formData.documents" :type-documents="typeDocumentItems" />
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

		</template>
	</BaseForm>
</template>

<script setup>
import { computed, reactive, watch, ref } from 'vue';
import { BaseForm, FormField, FormSelect, FormTextarea } from '@/components/common';
import DocumentForm from '@/components/Forms/DocumentForm.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const props = defineProps({
	title: {
		type: String,
		default: 'Bon de travail'
	},
	submitButtonText: {
		type: String,
		default: 'Valider'
	},
	submitButtonColor: {
		type: String,
		default: 'primary'
	},
	isEdit: {
		type: Boolean,
		default: false
	},
	initialData: {
		type: Object,
		default: () => ({})
	},
	equipments: {
		type: Array,
		default: () => []
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
	connectedUserId: {
		type: Number,
		default: null
	}
});

const emit = defineEmits(['created', 'updated', 'close']);

const formData = ref({
	equipement_id: null,
	nom: '',
	type: 'CORRECTIF',
	date_prevue: null,
	commentaire: '',
	diagnostic: '',
	responsable_id: null,
	utilisateur_assigne_ids: [],
	consommables: [{ consommable_id: null, quantite_utilisee: null }],
	documents: [{ document_id: null, nomDocument: '', typeDocument_id: null, file: null }]
});

const originalFormData = ref(null);
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

// Initialiser les données
watch(() => props.initialData, (newData) => {
	if (newData && Object.keys(newData).length > 0) {
		formData.value = {
			equipement_id: newData.equipement_id || null,
			nom: newData.nom || '',
			type: newData.type || 'CORRECTIF',
			date_prevue: newData.date_prevue || null,
			commentaire: newData.commentaire || '',
			diagnostic: newData.diagnostic || '',
			responsable_id: newData.responsable_id || null,
			utilisateur_assigne_ids: newData.utilisateur_assigne_ids || [],
			consommables: newData.consommables?.length ? newData.consommables : [{ consommable_id: null, quantite_utilisee: null }],
			documents: newData.documents?.length ? newData.documents : [{ document_id: null, nomDocument: '', typeDocument_id: null, file: null }]
		};
		// Sauvegarder l'état original pour comparaison
		if (props.isEdit) {
			originalFormData.value = JSON.parse(JSON.stringify(formData.value));
		}
	}
}, { immediate: true, deep: true });

const close = () => {
	emit('close');
};

const buildConsommablesPayload = (source) => {
	const lines = Array.isArray(source?.consommables) ? source.consommables : [];
	return lines
		.filter((c) => c && c.consommable_id !== null && c.consommable_id !== undefined && c.consommable_id !== '')
		.map((c) => {
			const id = Number(c.consommable_id);
			const qRaw = Number.isFinite(Number(c.quantite_utilisee)) ? Number(c.quantite_utilisee) : 0;
			const q = Math.max(0, Math.trunc(qRaw));
			return { consommable_id: id, quantite_utilisee: q };
		})
		.sort((a, b) => a.consommable_id - b.consommable_id);
};

const createAndLinkDocuments = async (bonTravailId, documents, originalDocuments = []) => {
	const docs = Array.isArray(documents) ? documents : [];
	const errors = [];
	const api = useApi(API_BASE_URL);

	for (const doc of docs) {
		if (!doc) continue;
		
		// Ignorer les lignes vides
		if (!doc.file && !doc.typeDocument_id && !(doc.nomDocument || '').trim()) continue;
		
		// Gérer les documents existants (mise à jour seulement si modifié)
		if (doc.document_id) {
			// Trouver le document original
			const original = originalDocuments.find(o => o.document_id === doc.document_id);
			
			// Vérifier si au moins un champ a changé
			const hasChanges = 
				(original && doc.nomDocument !== original.nomDocument) ||
				(original && doc.typeDocument_id !== original.typeDocument_id) ||
				doc.file; // Nouveau fichier = toujours un changement
			
			if (!hasChanges) {
				// Aucun changement, on passe au suivant
				continue;
			}
			
			try {
				// Toujours utiliser FormData pour la compatibilité avec le backend
				const form = new FormData();
				form.append('nomDocument', doc.nomDocument || '');
				form.append('typeDocument_id', String(doc.typeDocument_id));
				if (doc.file) {
					form.append('cheminAcces', doc.file);
				}
				await api.patch(`documents/${doc.document_id}/`, form);
			} catch (e) {
				console.error('Erreur lors de la mise à jour du document:', e);
				errors.push(doc.nomDocument || 'Document existant');
			}
			continue;
		}
		
		// Vérifier les champs requis pour les nouveaux documents
		if (!doc.file || !doc.typeDocument_id) {
			errors.push(doc.nomDocument || 'Document');
			continue;
		}

		try {
			const form = new FormData();
			form.append('nomDocument', (doc.nomDocument || doc.file.name || '').toString());
			form.append('typeDocument_id', String(doc.typeDocument_id));
			form.append('cheminAcces', doc.file);

			const created = await api.post('documents/', form);
			const newId = Number(created?.id);
			if (!Number.isInteger(newId) || newId <= 0) {
				errors.push(doc.nomDocument || doc.file?.name || 'Document');
				continue;
			}

			try {
				await api.post(`bons-travail/${bonTravailId}/ajouter_document/`, {
					document_id: newId,
					user: props.connectedUserId,
				});
			} catch (e) {
				try {
					await api.remove(`documents/${newId}/`);
				} catch (_) {}
				errors.push(doc.nomDocument || doc.file?.name || 'Document');
			}
		} catch (e) {
			errors.push(doc.nomDocument || doc.file?.name || 'Document');
		}
	}

	return errors;
};

const buildPatchPayload = (payload) => {
	const original = originalFormData.value;
	if (!original) return {};

	const patch = {};

	if ((payload?.nom ?? '') !== (original?.nom ?? '')) patch.nom = payload.nom;
	if ((payload?.type ?? null) !== (original?.type ?? null)) patch.type = payload.type;
	if ((payload?.diagnostic ?? '') !== (original?.diagnostic ?? '')) patch.diagnostic = payload.diagnostic;
	if ((payload?.commentaire ?? '') !== (original?.commentaire ?? '')) patch.commentaire = payload.commentaire;
	if ((payload?.responsable_id ?? null) !== (original?.responsable_id ?? null)) patch.responsable_id = payload.responsable_id;

	const currentDatePrevue = payload?.date_prevue || null;
	const originalDatePrevue = original?.date_prevue || null;
	if ((currentDatePrevue ?? null) !== (originalDatePrevue ?? null)) {
		patch.date_prevue =
			currentDatePrevue && String(currentDatePrevue).length === 16
				? `${currentDatePrevue}:00`
				: currentDatePrevue || null;
	}

	const newIds = (Array.isArray(payload?.utilisateur_assigne_ids) ? payload.utilisateur_assigne_ids : [])
		.map((x) => Number(x))
		.filter((x) => Number.isFinite(x));
	const oldIds = (Array.isArray(original?.utilisateur_assigne_ids) ? original.utilisateur_assigne_ids : [])
		.map((x) => Number(x))
		.filter((x) => Number.isFinite(x));
	const sameIds = newIds.length === oldIds.length && newIds.every((id, i) => id === oldIds[i]);
	if (!sameIds) {
		patch.utilisateur_assigne_ids = newIds;
	}

	const newConsommables = buildConsommablesPayload(payload);
	const oldConsommables = buildConsommablesPayload(original);
	const sameConsommables = JSON.stringify(newConsommables) === JSON.stringify(oldConsommables);
	if (!sameConsommables) {
		patch.consommables = newConsommables;
	}

	return patch;
};

const haveDocumentsChanged = (payload) => {
	const originalDocs = Array.isArray(originalFormData.value?.documents) ? originalFormData.value.documents : [];
	const currentDocs = Array.isArray(payload?.documents) ? payload.documents : [];

	// Vérifier si de nouveaux documents vont être créés
	const hasNewDocuments = currentDocs.some((doc) => {
		if (!doc) return false;
		const existingId = Number(doc.document_id);
		if (Number.isInteger(existingId) && existingId > 0) return false;
		return doc.file || doc.typeDocument_id || (doc.nomDocument || '').trim();
	});
	if (hasNewDocuments) return true;

	// Vérifier si des documents existants ont été modifiés
	for (const doc of currentDocs) {
		if (!doc?.document_id) continue;
		const original = originalDocs.find(o => o.document_id === doc.document_id);
		if (!original) continue;
		
		const hasChanges = 
			doc.nomDocument !== original.nomDocument ||
			doc.typeDocument_id !== original.typeDocument_id ||
			doc.file; // Nouveau fichier
		
		if (hasChanges) return true;
	}

	return false;
};

const save = async () => {
	loading.value = true;
	errorMessage.value = '';
	successMessage.value = '';

	const api = useApi(API_BASE_URL);

	try {
		if (!props.connectedUserId) {
			errorMessage.value = 'Utilisateur non identifié';
			loading.value = false;
			return;
		}

		if (props.isEdit) {
			// Mode édition
			const patch = buildPatchPayload(formData.value);
			const documentsChanged = haveDocumentsChanged(formData.value);
			
			if (Object.keys(patch).length === 0 && !documentsChanged) {
				successMessage.value = 'Aucune modification à enregistrer';
				loading.value = false;
				return;
			}

			// Appliquer le patch seulement s'il y a des changements de champs
			if (Object.keys(patch).length > 0) {
				patch.user = props.connectedUserId;
				await api.patch(`bons-travail/${props.initialData.id}/`, patch);
			}

			// Gestion des documents avec détection de changements
			const docErrors = await createAndLinkDocuments(
				props.initialData.id,
				formData.value.documents,
				originalFormData.value.documents
			);
			if (docErrors.length) {
				errorMessage.value = `Certains documents n'ont pas pu être traités: ${docErrors.join(', ')}`;
				loading.value = false;
				return;
			}

			successMessage.value = 'Bon de travail modifié avec succès';
			emit('updated');
		} else {
			// Mode création
			const createdDemande = await api.post('demandes-intervention/', {
				nom: formData.value.nom,
				commentaire: formData.value.commentaire,
				equipement_id: formData.value.equipement_id,
				utilisateur_id: props.connectedUserId
			});

			await api.patch(`demandes-intervention/${createdDemande.id}/updateStatus/`, {
				statut: 'TRANSFORMEE'
			});

			const createdBonTravail = await api.post('bons-travail/', {
				demande_intervention: createdDemande.id,
				utilisateur_id: props.connectedUserId,
				nom: formData.value.nom,
				type: formData.value.type,
				date_prevue:
					formData.value.date_prevue && String(formData.value.date_prevue).length === 16
						? `${formData.value.date_prevue}:00`
						: formData.value.date_prevue || null,
				commentaire: formData.value.commentaire,
				diagnostic: formData.value.diagnostic,
				responsable_id: formData.value.responsable_id,
				utilisateur_assigne_ids: (Array.isArray(formData.value?.utilisateur_assigne_ids) ? formData.value.utilisateur_assigne_ids : [])
					.map((x) => Number(x))
					.filter((x) => Number.isFinite(x) && x > 0),
				consommables: buildConsommablesPayload(formData.value)
			});

			// Gestion des documents
			const docErrors = await createAndLinkDocuments(createdBonTravail.id, formData.value.documents);
			if (docErrors.length) {
				errorMessage.value = `BT créé mais certains documents n'ont pas pu être ajoutés: ${docErrors.join(', ')}`;
				loading.value = false;
				return;
			}

			successMessage.value = 'Bon de travail créé avec succès';
			emit('created', createdBonTravail);
		}

		setTimeout(() => {
			emit('close');
		}, 1500);
	} catch (error) {
		console.error('Erreur lors de l\'enregistrement:', error);
		errorMessage.value = error.message || 'Une erreur est survenue lors de l\'enregistrement du bon de travail';
	} finally {
		loading.value = false;
	}
};

const mergedBaseFormProps = computed(() => ({
	title: props.title,
	submitButtonText: props.submitButtonText,
	submitButtonColor: props.submitButtonColor,
	elevation: 2,
	cardClass: 'rounded-lg',
	contentClass: 'pa-6'
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
</script>

