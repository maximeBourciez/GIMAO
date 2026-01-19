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
	consommables: [{ consommable_id: null, quantite_utilisee: 1 }]
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

const loadBonTravail = async () => {
	const bon = await api.get(`bons-travail/${bonId}/`);

	const consommablesLines = Array.isArray(bon?.consommables)
		? bon.consommables
			.map((c) => ({
				consommable_id: c?.consommable ?? null,
				quantite_utilisee: Number.isFinite(Number(c?.quantite)) ? Number(c.quantite) : 0
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
		consommables: consommablesLines.length ? consommablesLines : [{ consommable_id: null, quantite_utilisee: 1 }]
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
		if (Object.keys(patch).length === 0) {
			formState.successMessage = 'Aucune modification à enregistrer';
			return;
		}

		patch.user = connectedUser.value.id;
		await api.patch(`bons-travail/${bonId}/`, patch);

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
		await Promise.all([loadUsers(), loadEquipments(), loadConsommables(), loadBonTravail()]);
	} catch (error) {
		console.error('Erreur lors du chargement:', error);
		formState.errorMessage = 'Erreur lors du chargement des données';
	} finally {
		formState.loading = false;
	}
});
</script>
