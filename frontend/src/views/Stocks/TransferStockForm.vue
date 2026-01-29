<template>
  <v-dialog v-model="dialog" max-width="600px">
    <BaseForm
      title="Transférer du stock"
      :submit-button-text="'Transférer'"
      :submit-disabled="!isValid"
      :handle-submit="submit"
      @cancel="close"
      :loading="loading"
    >
        <template #default>
          <v-container>
            <!-- Source Store -->
            <v-select
              v-model="sourceStore"
              :items="availableStores"
              item-title="title"
              item-value="magasin"
              label="Magasin Source"
              return-object
              required
              :rules="[v => !!v || 'Magasin source requis']"
            ></v-select>

            <v-divider class="my-4"></v-divider>
            <div class="text-subtitle-1 mb-2">Vers:</div>

            <!-- Destinations -->
            <div v-for="(transfer, index) in transfers" :key="index" class="d-flex align-center mb-2">
              <v-autocomplete
                v-model="transfer.to_magasin"
                :items="allStores"
                item-title="nom"
                item-value="id"
                label="Magasin Destination"
                class="mr-2"
                density="compact"
                hide-details
              ></v-autocomplete>
              <v-text-field
                v-model.number="transfer.quantite"
                label="Quantité"
                type="number"
                min="1"
                density="compact"
                hide-details
                style="max-width: 100px"
              ></v-text-field>
              <v-btn icon="mdi-delete" size="small" variant="text" color="error" @click="removeTransfer(index)"></v-btn>
            </div>

            <v-btn color="primary" variant="tonal" size="small" @click="addTransfer" class="mt-2">
              + Ajouter destination
            </v-btn>

            <v-alert v-if="remainingStock < 0" type="error" density="compact" class="mt-4">
              Stock insuffisant (Manque: {{ Math.abs(remainingStock) }})
            </v-alert>
             <v-alert v-else type="info" density="compact" class="mt-4">
              Reste en stock après transfert : {{ remainingStock }}
            </v-alert>

          </v-container>
        </template>
    </BaseForm>
  </v-dialog>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';
import BaseForm from '@/components/common/BaseForm.vue';

const props = defineProps({
  modelValue: Boolean,
  consumable: Object
});

const emit = defineEmits(['update:modelValue', 'transfer-complete']);
const api = useApi(API_BASE_URL);

const dialog = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
});

const valid = ref(false);
const loading = ref(false);
const sourceStore = ref(null);
const transfers = ref([{ to_magasin: null, quantite: 1 }]);
const allStores = ref([]);
const loadingStores = ref(false);

// Stores that have stock
const availableStores = computed(() => {
  if (!props.consumable?.stocks) return [];
  return props.consumable.stocks
    .filter(s => s.quantite > 0)
    .map(s => ({ ...s, title: `${s.magasin_nom} (Stock: ${s.quantite})` }));
});

const remainingStock = computed(() => {
  if (!sourceStore.value) return 0;
  const totalTransfer = transfers.value.reduce((sum, t) => sum + (parseInt(t.quantite) || 0), 0);
  return sourceStore.value.quantite - totalTransfer;
});

const isValid = computed(() => {
  return sourceStore.value && transfers.value.length > 0 && remainingStock.value >= 0 && transfers.value.every(t => t.to_magasin && t.quantite > 0);
});

const fetchAllStores = async () => {
    loadingStores.value = true;
    try {
        const response = await api.get('magasins/');
        allStores.value = response.results || response;
    } catch(e) {
        console.error("Error fetching stores", e);
    } finally {
        loadingStores.value = false;
    }
};

const addTransfer = () => {
  transfers.value.push({ to_magasin: null, quantite: 1 });
};

const removeTransfer = (index) => {
  transfers.value.splice(index, 1);
};

const close = () => {
  dialog.value = false;
  sourceStore.value = null;
  transfers.value = [{ to_magasin: null, quantite: 1 }];
};

const submit = async () => {
  // BaseForm sets loading automatically if handleSubmit returns promise? No, BaseForm prop 'loading' controls button state usually.
  // Actually BaseForm calls handleSubmit(formData)
  // BaseForm's handleSubmit:
  /*
  if (props.handleSubmit && typeof props.handleSubmit === 'function') {
    try {
      await props.handleSubmit(formData.value);
    } ...
  }
  */
  // So I don't need to manually set loading if I pass `loading` prop but BaseForm doesn't auto-set it based on promise.
  // I will keep manual loading management or I can let BaseForm handle errors if I throw?
  // I'll keep my manual loading for now to be safe with existing logic.
  
  if (!isValid.value) return;
  loading.value = true;
  try {
    const payload = {
        from_magasin: sourceStore.value.magasin, // stock object has magasin ID in 'magasin' field
        transfers: transfers.value
    };
    await api.post(`consommables/${props.consumable.id}/transfer_stock/`, payload);
    emit('transfer-complete');
    close();
  } catch (error) {
    console.error("Transfer failed", error);
    // Re-throw to show error in BaseForm? BaseForm catches errors from handleSubmit.
    throw error; 
  } finally {
    loading.value = false;
  }
};

onMounted(fetchAllStores);

</script>
