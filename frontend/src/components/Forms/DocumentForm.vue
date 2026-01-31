<template>
	<div>
		<v-row
			v-for="(doc, index) in documents"
			:key="index"
			dense
			class="mb-3"
		>
			<v-col cols="12" md="3">
				<FormField
					:model-value="doc.nomDocument"
					@update:modelValue="(value) => updateDocument(index, { nomDocument: value })"
					:field-name="`document_nom_${index}`"
					label="Nom"
					placeholder="Nom du document"
					clearable
				/>
			</v-col>
			
			<v-col cols="12" md="3">
				<FormSelect
					:model-value="doc.typeDocument_id"
					@update:modelValue="(value) => updateDocument(index, { typeDocument_id: value })"
					:field-name="`document_type_${index}`"
					label="Type"
					:items="typeDocuments"
					item-title="nomTypeDocument"
					item-value="id"
					placeholder="Sélectionner un type"
					:rules="[v => !!v || 'Le type est requis']"
				/>
			</v-col>

			<v-col cols="12" md="5">
				<FormFileInput
					:model-value="doc.file"
					@update:modelValue="(value) => updateDocument(index, { file: value })"
					:name="`document_file_${index}`"
					label="Fichier"
				/>
				<div v-if="doc.existingFileName" class="mt-1 text-caption text-grey">
					Fichier actuel: {{ doc.existingFileName }}
				</div>
			</v-col>

			<v-col cols="12" md="1" class="d-flex align-center justify-center">
				<v-btn
					icon="mdi-delete"
					size="small"
					color="error"
					@click="openDeleteModal(index)"
				/>
			</v-col>
		</v-row>

		<v-row dense>
			<v-col cols="12">
				<v-btn
					color="primary"
					variant="text"
					prepend-icon="mdi-plus"
					@click="addDocument"
				>
					Ajouter un document
				</v-btn>
			</v-col>
		</v-row>

		<!-- Modale de confirmation de suppression -->
		<ConfirmationModal
			v-model="showDeleteModal"
			type="error"
			title="Supprimer le document"
			message="Êtes-vous sûr de vouloir supprimer ce document ?\n\nCette action est irréversible."
			confirm-text="Supprimer"
			cancel-text="Annuler"
			confirm-icon="mdi-delete"
			:loading="deletingDoc"
			@confirm="confirmDelete"
			@cancel="cancelDelete"
		/>
	</div>
</template>

<script setup>
import { computed, onMounted, provide, ref } from 'vue';
import { FormField, FormSelect, FormFileInput } from '@/components/common';
import ConfirmationModal from '@/components/common/ConfirmationModal.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const props = defineProps({
	modelValue: {
		type: Array,
		default: () => []
	},
	typeDocuments: {
		type: Array,
		default: () => []
	}
});

const emit = defineEmits(['update:modelValue']);

const EMPTY_ROW = { 
	document_id: null, 
	nomDocument: '', 
	typeDocument_id: null, 
	file: null,
	existingFileName: null
};

const normalize = (value) => {
	const base = Array.isArray(value) ? value : [];
	return base.length ? base : [EMPTY_ROW];
};

const documents = computed(() => normalize(props.modelValue));

// Fonction isFieldRequired personnalisée pour gérer les fichiers existants
const isFieldRequired = (fieldName) => {
	// Extraire l'index du nom du champ
	const match = fieldName.match(/document_(\w+)_(\d+)/);
	if (!match) return false;
	
	const [, fieldType, indexStr] = match;
	const index = parseInt(indexStr);
	
	// Type est toujours requis
	if (fieldType === 'type') return true;
	
	// Fichier requis seulement si pas de fichier existant
	if (fieldType === 'file') {
		return !documents.value[index]?.existingFileName;
	}
	
	return false;
};

// Fournir isFieldRequired aux composants enfants
provide('isFieldRequired', isFieldRequired);

onMounted(() => {
	if (!Array.isArray(props.modelValue) || props.modelValue.length === 0) {
		emit('update:modelValue', [EMPTY_ROW]);
	}
});

const updateDocument = (index, patch) => {
	const current = normalize(props.modelValue);
	const next = current.map((doc, i) => (i === index ? { ...doc, ...patch } : doc));
	emit('update:modelValue', next);
};

const addDocument = () => {
	const current = normalize(props.modelValue);
	emit('update:modelValue', [...current, { ...EMPTY_ROW }]);
};

const showDeleteModal = ref(false);
const deletingDoc = ref(false);
const indexToDelete = ref(null);

const openDeleteModal = (index) => {
	const current = normalize(props.modelValue);
	const doc = current[index];
	
	// Si c'est un document existant (avec ID), on ouvre la modale
	if (doc?.document_id && Number.isInteger(Number(doc.document_id)) && Number(doc.document_id) > 0) {
		indexToDelete.value = index;
		showDeleteModal.value = true;
	} else {
		// Sinon, on supprime directement la ligne vide
		const next = current.filter((_, i) => i !== index);
		emit('update:modelValue', next.length ? next : [{ ...EMPTY_ROW }]);
	}
};

const cancelDelete = () => {
	showDeleteModal.value = false;
	indexToDelete.value = null;
};

const confirmDelete = async () => {
	if (indexToDelete.value === null) return;
	
	const current = normalize(props.modelValue);
	const doc = current[indexToDelete.value];
	
	// Si le document a un ID (document existant), on le supprime du backend
	if (doc?.document_id && Number.isInteger(Number(doc.document_id)) && Number(doc.document_id) > 0) {
		deletingDoc.value = true;
		try {
			const api = useApi(API_BASE_URL);
			await api.remove(`documents/${doc.document_id}/`);
		} catch (error) {
			console.error('Erreur lors de la suppression du document:', error);
		} finally {
			deletingDoc.value = false;
		}
	}
	
	const next = current.filter((_, i) => i !== indexToDelete.value);
	emit('update:modelValue', next.length ? next : [{ ...EMPTY_ROW }]);
	
	showDeleteModal.value = false;
	indexToDelete.value = null;
};
</script>
