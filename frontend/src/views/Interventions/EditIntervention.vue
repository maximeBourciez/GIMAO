<template>
	<v-app>
		<v-main>
			<v-container>
				<InterventionForm
					v-model="formData"
					:base-form-props="baseFormProps"
					:equipments="equipments"
					:users="users"
					:consommables="consommables"
					:type-documents="typeDocuments"
					:equipement-read-only="true"
					:responsable-read-only="true"
					:state="formState"
					@submit="submit"
					@cancel="goBack"
					@clear-error="formState.errorMessage = ''"
					@clear-success="formState.successMessage = ''"
				/>
			</v-container>
		</v-main>
	</v-app>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';
import InterventionForm from '@/components/Forms/InterventionForm.vue';

const route = useRoute();
const router = useRouter();
const store = useStore();
const api = useApi(API_BASE_URL);

const bonId = route.params.id;

const formState = reactive({
	loading: false,
	errorMessage: '',
	successMessage: ''
});

const baseFormProps = {
	title: 'Modifier un bon de travail',
	submitButtonText: 'Enregistrer',
	submitButtonColor: 'primary'
};

const users = ref([]);
const equipments = ref([]);
const consommables = ref([]);
const typeDocuments = ref([]);

const connectedUser = computed(() => store.getters.currentUser);

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

const toDatetimeLocalValue = (value) => {
	if (!value) return null;
	if (typeof value !== 'string') return null;

	// Accepte :
	// - "2026-01-10 09:00:00.000000" (format DB)
	// - "2026-01-10T09:00:00" / "2026-01-10T09:00:00.000000" (ISO)
	const match = value.match(/^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2})/);
	if (!match) return null;
	return `${match[1]}T${match[2]}`;
};

const loadUsers = async () => {
	users.value = await api.get('utilisateurs/');
};

const loadEquipments = async () => {
	equipments.value = await api.get('equipements/');
};

const loadConsommables = async () => {
	consommables.value = await api.get('consommables/');
};

const loadTypeDocuments = async () => {
	typeDocuments.value = await api.get('types-documents/');
};

const loadBonTravail = async () => {
	const bon = await api.get(`bons-travail/${bonId}/`);

	const consommablesLines = Array.isArray(bon?.consommables)
		? bon.consommables
			.map((c) => ({
				consommable_id: c?.consommable ?? null,
				quantite_utilisee: Number.isFinite(Number(c?.quantite)) ? Number(c.quantite) : 0
			}))
		: [];

	const documentsLines = Array.isArray(bon?.documentsBT)
		? bon.documentsBT.map((d) => ({
				document_id: d?.id ?? null,
				nomDocument: '',
				typeDocument_id: null,
				file: null
		  }))
		: [];

	formData.value = {
		equipement_id: bon?.demande_intervention?.equipement?.id ?? null,
		nom: bon?.nom ?? '',
		type: bon?.type ?? 'CORRECTIF',
		date_prevue: toDatetimeLocalValue(bon?.date_prevue),
		commentaire: bon?.commentaire ?? '',
		diagnostic: bon?.diagnostic ?? '',
		responsable_id: bon?.responsable?.id ?? null,
		utilisateur_assigne_ids: Array.isArray(bon?.utilisateur_assigne)
			? bon.utilisateur_assigne.map((u) => u.id)
			: [],
		consommables: consommablesLines.length ? consommablesLines : [{ consommable_id: null, quantite_utilisee: null }],
		documents: documentsLines.length ? documentsLines : [{ document_id: null, nomDocument: '', typeDocument_id: null, file: null }]
	};

	originalFormData.value = JSON.parse(JSON.stringify(formData.value));
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

	const newConsommables = buildConsommablesPayload(payload);
	const oldConsommables = buildConsommablesPayload(original);
	const sameConsommables = JSON.stringify(newConsommables) === JSON.stringify(oldConsommables);
	if (!sameConsommables) {
		patch.consommables = newConsommables;
	}

	return patch;
};

const linkExistingDocumentsToBonTravail = async (bonTravailId, payload) => {
	const docs = Array.isArray(payload?.documents) ? payload.documents : [];
	const ids = docs
		.map((d) => Number(d?.document_id))
		.filter((x) => Number.isInteger(x) && x > 0);

	const errors = [];
	for (const id of ids) {
		try {
			await api.post(`bons-travail/${bonTravailId}/ajouter_document/`, {
				document_id: id,
				user: connectedUser.value?.id,
			});
		} catch (e) {
			errors.push(`Document #${id}`);
		}
	}
	return errors;
};

const createNewDocumentsThenLinkToBonTravail = async (bonTravailId, payload) => {
	const docs = Array.isArray(payload?.documents) ? payload.documents : [];
	const errors = [];

	for (const doc of docs) {
		if (!doc) continue;
		const existingId = Number(doc.document_id);
		if (Number.isInteger(existingId) && existingId > 0) continue;
		if (!doc.file && !doc.typeDocument_id && !(doc.nomDocument || '').trim()) continue;
		if (!doc.file || !doc.typeDocument_id) {
			errors.push(doc.nomDocument || doc.file?.name || 'Document');
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
					user: connectedUser.value?.id,
				});
			} catch (e) {
				try {
					await api.delete(`documents/${newId}/`);
				} catch (_) {}
				errors.push(doc.nomDocument || doc.file?.name || 'Document');
			}
		} catch (e) {
			errors.push(doc.nomDocument || doc.file?.name || 'Document');
		}
	}

	return errors;
};

const removeUnlinkedDocuments = async (bonTravailId, payload) => {
	const originalDocs = Array.isArray(originalFormData.value?.documents) ? originalFormData.value.documents : [];
	const currentDocs = Array.isArray(payload?.documents) ? payload.documents : [];

	const originalIds = originalDocs
		.map((d) => Number(d?.document_id))
		.filter((x) => Number.isInteger(x) && x > 0);

	const currentIds = currentDocs
		.map((d) => Number(d?.document_id))
		.filter((x) => Number.isInteger(x) && x > 0);

	const removedIds = originalIds.filter((id) => !currentIds.includes(id));

	const errors = [];
	for (const id of removedIds) {
		try {
			await api.patch(`bons-travail/${bonTravailId}/delink_document/`, {
				document_id: id,
				user: connectedUser.value?.id,
			});
		} catch (e) {
			errors.push(`Document #${id}`);
		}
	}
	return errors;
};

const haveDocumentsChanged = (payload) => {
	const originalDocs = Array.isArray(originalFormData.value?.documents) ? originalFormData.value.documents : [];
	const currentDocs = Array.isArray(payload?.documents) ? payload.documents : [];

	const originalIds = originalDocs
		.map((d) => Number(d?.document_id))
		.filter((x) => Number.isInteger(x) && x > 0)
		.sort((a, b) => a - b);

	const currentIds = currentDocs
		.map((d) => Number(d?.document_id))
		.filter((x) => Number.isInteger(x) && x > 0)
		.sort((a, b) => a - b);

	// Vérifier si des documents ont été retirés ou ajoutés
	if (originalIds.length !== currentIds.length) return true;
	if (!originalIds.every((id, i) => id === currentIds[i])) return true;

	// Vérifier si de nouveaux documents vont être créés
	const hasNewDocuments = currentDocs.some((doc) => {
		if (!doc) return false;
		const existingId = Number(doc.document_id);
		if (Number.isInteger(existingId) && existingId > 0) return false;
		return doc.file || doc.typeDocument_id || (doc.nomDocument || '').trim();
	});

	return hasNewDocuments;
};

const submit = async (payload) => {
	formState.loading = true;
	formState.errorMessage = '';
	formState.successMessage = '';

	try {
		if (!connectedUser.value?.id) {
			formState.errorMessage = 'Utilisateur non identifié';
			return;
		}

		const patch = buildPatchPayload(payload);
		const documentsChanged = haveDocumentsChanged(payload);
		
		if (Object.keys(patch).length === 0 && !documentsChanged) {
			formState.successMessage = 'Aucune modification à enregistrer';
			return;
		}

		// Appliquer le patch seulement s'il y a des changements de champs
		if (Object.keys(patch).length > 0) {
			patch.user = connectedUser.value.id;
			await api.patch(`bons-travail/${bonId}/`, patch);
		}

		// Gestion des documents
		const removeErrors = await removeUnlinkedDocuments(bonId, payload);
		const linkErrors = await linkExistingDocumentsToBonTravail(bonId, payload);
		const createErrors = await createNewDocumentsThenLinkToBonTravail(bonId, payload);
		const docErrors = [...removeErrors, ...linkErrors, ...createErrors];
		if (docErrors.length) {
			formState.errorMessage = `Certains documents n'ont pas pu être traités: ${docErrors.join(', ')}`;
			return;
		}

		formState.successMessage = 'Bon de travail modifié avec succès';
		setTimeout(() => {
			router.push({ name: 'InterventionDetail', params: { id: bonId } });
		}, 1000);
	} catch (error) {
		console.error('Erreur lors de la modification du bon de travail:', error);
		formState.errorMessage = 'Erreur lors de la modification du bon de travail';
	} finally {
		formState.loading = false;
	}
};

const goBack = () => {
	router.back();
};

onMounted(async () => {
	formState.loading = true;
	formState.errorMessage = '';
	try {
		await Promise.all([loadUsers(), loadEquipments(), loadConsommables(), loadTypeDocuments(), loadBonTravail()]);
	} catch (error) {
		console.error('Erreur lors du chargement:', error);
		formState.errorMessage = 'Erreur lors du chargement des données';
	} finally {
		formState.loading = false;
	}
});
</script>
