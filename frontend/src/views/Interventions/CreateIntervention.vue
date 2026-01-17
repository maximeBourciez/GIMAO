<template>
	<v-app>
		<v-main>
			<v-container>
				<InterventionForm
					v-model="formData"
					:base-form-props="baseFormProps"
					:equipments="equipments"
					:users="users"
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

const connectedUser = computed(() => store.getters.currentUser);

const formData = ref({
	equipement_id: null,
	nom: '',
	type: 'CORRECTIF',
	date_prevue: null,
	commentaire: '',
	diagnostic: '',
	responsable_id: null,
	utilisateur_assigne_ids: []
});

const loadUsers = async () => {
	users.value = await api.get('utilisateurs/');
};

const loadEquipments = async () => {
	equipments.value = await api.get('equipements/');
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
			utilisateur_assigne_ids: payload.utilisateur_assigne_ids
		});

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
		await Promise.all([loadUsers(), loadEquipments()]);
	} catch (error) {
		console.error('Erreur lors du chargement:', error);
		formState.errorMessage = 'Erreur lors du chargement des données';
	} finally {
		formState.loading = false;
	}
});
</script>

