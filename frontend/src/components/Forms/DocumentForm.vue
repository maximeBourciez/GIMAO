<template>
	<div>
		<v-row
			v-for="(doc, index) in documents"
			:key="index"
			dense
			class="mb-2"
		>
			<v-col cols="12" md="11">
				<FormSelect
					:model-value="doc.document_id"
					@update:modelValue="(value) => onSelectDocument(index, value)"
					:field-name="`document_select_${index}`"
					label="Document"
					:items="documentSelectItems"
					item-title="label"
					item-value="id"
					clearable
				/>

				<div v-if="hasNewDocumentData(doc)" class="mt-1 text-caption text-grey">
					Nouveau document: {{ (doc.nomDocument || doc.file?.name || 'Document') }}
					<span v-if="doc.typeDocument_id"> — {{ getTypeName(doc.typeDocument_id) }}</span>
					<v-btn
						size="x-small"
						variant="text"
						class="ml-2"
						@click="openCreateModal(index, doc)"
					>
						Modifier
					</v-btn>
				</div>
			</v-col>

			<v-col cols="12" md="1" class="d-flex align-center justify-center">
				<v-btn
					icon="mdi-delete"
					size="small"
					color="error"
					variant="text"
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

		<!-- Modale : créer un nouveau document -->
		<v-dialog v-model="showCreate" max-width="720" scrollable>
			<v-card>
				<v-card-title class="text-h6">Nouveau document</v-card-title>
				<v-card-text class="pt-2">
					<v-alert v-if="createError" type="error" variant="tonal" class="mb-3">
						{{ createError }}
					</v-alert>
					<v-row dense>
						<v-col cols="12" md="4">
							<FormField
								v-model="createForm.nomDocument"
								field-name="document_create_nom"
								label="Nom (optionnel)"
								clearable
							/>
						</v-col>
						<v-col cols="12" md="4">
							<FormSelect
								v-model="createForm.typeDocument_id"
								field-name="document_create_type"
							label="Type *"
								:items="typeDocuments"
								item-title="nomTypeDocument"
								item-value="id"
							/>
						</v-col>
						<v-col cols="12" md="4">
							<FormFileInput
								v-model="createForm.file"
								field-name="document_create_file"
							label="Fichier *"
								prepend-inner-icon="mdi-file-document"
								clearable
							/>
						</v-col>
					</v-row>
				</v-card-text>
				<v-card-actions class="justify-end">
					<v-btn variant="text" @click="cancelCreate">Annuler</v-btn>
					<v-btn color="primary" :disabled="!canConfirmCreate" @click="confirmCreate">
						Valider
					</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>
	</div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { FormField, FormSelect, FormFileInput } from '@/components/common';
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
	},
	excludeDocumentIds: {
		type: Array,
		default: () => []
	}
});

const emit = defineEmits(['update:modelValue']);

const EMPTY_ROW = { document_id: null, nomDocument: '', typeDocument_id: null, file: null };
const CREATE_OPTION_ID = '__create__';

const api = useApi(API_BASE_URL);

const existingDocuments = ref([]);

const showCreate = ref(false);
const createError = ref('');
const createIndex = ref(null);
const createForm = ref({ nomDocument: '', typeDocument_id: null, file: null });

const normalize = (value) => {
	const base = Array.isArray(value) ? value : [];
	return base.length ? base : [EMPTY_ROW];
};

const documents = computed(() => normalize(props.modelValue));

onMounted(() => {
	if (!Array.isArray(props.modelValue) || props.modelValue.length === 0) {
		emit('update:modelValue', [EMPTY_ROW]);
	}
	loadExistingDocuments();
});

const loadExistingDocuments = async () => {
	try {
		existingDocuments.value = await api.get('documents/');
	} catch (e) {
		existingDocuments.value = [];
	}
};

const getTypeName = (typeId) => {
	const id = Number(typeId);
	if (!Number.isFinite(id)) return '—';
	return props.typeDocuments?.find((t) => Number(t?.id) === id)?.nomTypeDocument || '—';
};

const excludedIdSet = computed(() => {
	const raw = Array.isArray(props.excludeDocumentIds) ? props.excludeDocumentIds : [];
	const ids = raw
		.map((x) => Number(x))
		.filter((x) => Number.isInteger(x) && x > 0);
	return new Set(ids);
});

const documentSelectItems = computed(() => {
	const createItem = { id: CREATE_OPTION_ID, label: '+ Créer un nouveau document…' };
	const docs = Array.isArray(existingDocuments.value) ? existingDocuments.value : [];
	const docItems = docs
		.map((d) => {
			const id = d?.id;
			const name = d?.nomDocument || d?.titre || `Document #${id}`;
			const typeName = getTypeName(d?.typeDocument || d?.type);
			return { id, label: typeName && typeName !== '—' ? `${name} — ${typeName}` : name };
		})
		.filter((x) => x.id !== null && x.id !== undefined)
		.filter((x) => !excludedIdSet.value.has(Number(x.id)))
		.sort((a, b) => Number(b.id) - Number(a.id));

	return [createItem, ...docItems];
});

const hasNewDocumentData = (doc) => {
	if (!doc) return false;
	const hasName = Boolean((doc.nomDocument ?? '').trim());
	const hasType = doc.typeDocument_id !== null && doc.typeDocument_id !== undefined && doc.typeDocument_id !== '';
	const hasFile = Boolean(doc.file);
	return hasName || hasType || hasFile;
};

const updateDocument = (index, patch) => {
	const current = normalize(props.modelValue);
	const next = current.map((doc, i) => (i === index ? { ...doc, ...patch } : doc));
	emit('update:modelValue', next);
};

const onSelectDocument = (index, value) => {
	if (value === CREATE_OPTION_ID) {
		openCreateModal(index, null);
		// On garde la ligne sur "nouveau" (pas de document_id)
		updateDocument(index, { document_id: null });
		return;
	}
	if (value === null || value === undefined || value === '') {
		updateDocument(index, { document_id: null, nomDocument: '', typeDocument_id: null, file: null });
		return;
	}
	const id = Number(value);
	updateDocument(index, { document_id: Number.isFinite(id) ? id : value, nomDocument: '', typeDocument_id: null, file: null });
};

const openCreateModal = (index, existingRow) => {
	createIndex.value = index;
	createError.value = '';
	createForm.value = {
		nomDocument: (existingRow?.nomDocument ?? '').toString(),
		typeDocument_id: existingRow?.typeDocument_id ?? null,
		file: existingRow?.file ?? null,
	};
	showCreate.value = true;
};

const cancelCreate = () => {
	showCreate.value = false;
	createError.value = '';
	createIndex.value = null;
	createForm.value = { nomDocument: '', typeDocument_id: null, file: null };
};

const canConfirmCreate = computed(() => {
	const hasType = createForm.value?.typeDocument_id !== null && createForm.value?.typeDocument_id !== undefined && createForm.value?.typeDocument_id !== '';
	const hasFile = Boolean(createForm.value?.file);
	return hasType && hasFile && createIndex.value !== null;
});

const confirmCreate = () => {
	createError.value = '';
	if (createIndex.value === null) return;
	if (!canConfirmCreate.value) {
		createError.value = 'Type et fichier requis.';
		return;
	}
	updateDocument(createIndex.value, {
		document_id: null,
		nomDocument: (createForm.value.nomDocument || '').toString(),
		typeDocument_id: createForm.value.typeDocument_id,
		file: createForm.value.file,
	});
	cancelCreate();
};

const addDocument = () => {
	const current = normalize(props.modelValue);
	emit('update:modelValue', [...current, { ...EMPTY_ROW }]);
};

const removeDocument = (index) => {
	const current = normalize(props.modelValue);
	const next = current.filter((_, i) => i !== index);
	emit('update:modelValue', next.length ? next : [{ ...EMPTY_ROW }]);
};
</script>
