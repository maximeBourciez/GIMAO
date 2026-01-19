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

const formState = reactive({
	loading: false,
	errorMessage: '',
	successMessage: ''
});

const baseFormProps = {
	title: 'Créer un bon de travail',
	submitButtonText: 'Créer',
	submitButtonColor: 'success'
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

const buildConsommablesPayload = (payload) => {
	const lines = Array.isArray(payload?.consommables) ? payload.consommables : [];
	return lines
		.filter((c) => c && c.consommable_id !== null && c.consommable_id !== undefined && c.consommable_id !== '')
		.map((c) => {
			const id = Number(c.consommable_id);
			const qRaw = Number.isFinite(Number(c.quantite_utilisee)) ? Number(c.quantite_utilisee) : 0;
			const q = Math.max(0, Math.trunc(qRaw));
			return { consommable_id: id, quantite_utilisee: q };
		});
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
		// Si l'utilisateur a choisi un document existant, on ne l'upload pas.
		const existingId = Number(doc.document_id);
		if (Number.isInteger(existingId) && existingId > 0) continue;
		if (!doc.file && !doc.typeDocument_id && !(doc.nomDocument || '').trim()) continue;
		if (!doc.file || !doc.typeDocument_id) {
			errors.push(doc.nomDocument || doc.file?.name || 'Document');
			continue;
		}

		try {
			// 1) Crée le document via le CRUD
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

			// 2) Lie le document au BT
			try {
				await api.post(`bons-travail/${bonTravailId}/ajouter_document/`, {
					document_id: newId,
					user: connectedUser.value?.id,
				});
			} catch (e) {
				try {
					// evitrer les documents orphelins
					await api.delete(`documents/${newId}/`);
				} catch (_) {
					// ignore
				}
				errors.push(doc.nomDocument || doc.file?.name || 'Document');
			}
		} catch (e) {
			errors.push(doc.nomDocument || doc.file?.name || 'Document');
		}
	}

	return errors;
};

const submit = async (payload) => {
	formState.loading = true;
	formState.errorMessage = '';
	formState.successMessage = '';

	try {
		if (!connectedUser.value?.id) {
			formState.errorMessage = "Utilisateur non identifié";
			return;
		}

		const createdDemande = await api.post('demandes-intervention/', {
			nom: payload.nom,
			commentaire: payload.commentaire,
			equipement_id: payload.equipement_id,
			utilisateur_id: connectedUser.value?.id
		});

		await api.patch(`demandes-intervention/${createdDemande.id}/updateStatus/`, {
			statut: 'TRANSFORMEE'
		});

		const createdBonTravail = await api.post('bons-travail/', {
			demande_intervention: createdDemande.id,
			utilisateur_id: connectedUser.value?.id,
			nom: payload.nom,
			type: payload.type,
			date_prevue:
				payload.date_prevue && String(payload.date_prevue).length === 16
					? `${payload.date_prevue}:00`
					: payload.date_prevue || null,
			commentaire: payload.commentaire,
			diagnostic: payload.diagnostic,
			responsable_id: payload.responsable_id,
			utilisateur_assigne_ids: (Array.isArray(payload?.utilisateur_assigne_ids) ? payload.utilisateur_assigne_ids : [])
				.map((x) => Number(x))
				.filter((x) => Number.isFinite(x) && x > 0),
			consommables: buildConsommablesPayload(payload)
		});

		const linkErrors = await linkExistingDocumentsToBonTravail(createdBonTravail.id, payload);
		const createErrors = await createNewDocumentsThenLinkToBonTravail(createdBonTravail.id, payload);
		const docErrors = [...linkErrors, ...createErrors];
		if (docErrors.length) {
			formState.errorMessage = `Certains documents n'ont pas pu être ajoutés: ${docErrors.join(', ')}`;
			return;
		}

		formState.successMessage = "Bon de travail créé avec succès";
		setTimeout(() => {
			router.push({ name: 'InterventionDetail', params: { id: createdBonTravail.id } });
		}, 1000);
	} catch (error) {
		console.error('Erreur lors de la création du bon de travail:', error);
		formState.errorMessage = 'Erreur lors de la création du bon de travail';
	} finally {
		formState.loading = false;
	}
};

const goBack = () => {
	router.back();
};

onMounted(async () => {
	try {
		formState.loading = true;
		formData.value.responsable_id = connectedUser.value?.id ?? null;
		await Promise.all([loadUsers(), loadEquipments(), loadConsommables(), loadTypeDocuments()]);
	} catch (error) {
		console.error('Erreur lors du chargement:', error);
		formState.errorMessage = 'Erreur lors du chargement des données';
	} finally {
		formState.loading = false;
	}
});
</script>

