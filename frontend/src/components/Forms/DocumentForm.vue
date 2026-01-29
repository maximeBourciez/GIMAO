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
					label="Nom (optionnel)"
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
					@click="removeDocument(index)"
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
	</div>
</template>

<script setup>
import { computed, onMounted, provide, watch } from 'vue';
import { FormField, FormSelect, FormFileInput } from '@/components/common';
import { useApi } from '@/composables/useApi';
import { useFormValidation } from '@/composables/useFormValidation';
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

// Créer un schéma de validation dynamique basé sur le nombre de documents
const validationSchema = computed(() => {
	const schema = {};
	documents.value.forEach((doc, index) => {
		// Type est requis
		schema[`document_type_${index}`] = ['required'];
		// Fichier est requis seulement si pas de fichier existant
		if (!doc.existingFileName) {
			schema[`document_file_${index}`] = ['required'];
		}
	});
	return schema;
});

// Utiliser useFormValidation avec le schéma dynamique (accepte un computed)
const validation = useFormValidation(validationSchema);

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

// Fournir validation et isFieldRequired aux composants enfants
provide('validation', validation);
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

const removeDocument = async (index) => {
	const current = normalize(props.modelValue);
	const doc = current[index];
	
	// Si le document a un ID (document existant), on le supprime du backend
	if (doc?.document_id && Number.isInteger(Number(doc.document_id)) && Number(doc.document_id) > 0) {
		try {
			const api = useApi(API_BASE_URL);
			await api.delete(`documents/${doc.document_id}/`);
		} catch (error) {
			console.error('Erreur lors de la suppression du document:', error);
		}
	}
	
	const next = current.filter((_, i) => i !== index);
	emit('update:modelValue', next.length ? next : [{ ...EMPTY_ROW }]);
};
</script>
