<template>
  <v-dialog v-model="dialog" max-width="800px">
    <BaseForm
      title="Ajouter un achat"
      :show-actions="false"
      @cancel="close"
    >
        <template #default>
            <v-stepper v-model="step" :items="['Informations', 'Distribution']"  class="elevation-0" :hide-actions="true">
            <template v-slot:item.1>
                <v-card flat>
                <v-form ref="form" v-model="valid" @submit.prevent>
                        <v-container>
                            <v-row>
                            <!-- Date -->
                            <v-col cols="12" sm="6">
                                <v-text-field
                                v-model="purchase.date_reference_prix"
                                label="Date"
                                type="date"
                                required
                                :rules="dateRules"
                                ></v-text-field>
                            </v-col>

                            <!-- Quantité -->
                            <v-col cols="12" sm="6">
                                <v-text-field
                                v-model.number="purchase.quantite"
                                label="Quantité Achetée"
                                type="number"
                                min="1"
                                required
                                :rules="quantityRules"
                                ></v-text-field>
                            </v-col>

                            <!-- Prix Unitaire -->
                            <v-col cols="12" sm="6">
                                <v-text-field
                                v-model.number="purchase.prix_unitaire"
                                label="Prix Unitaire (€)"
                                type="number"
                                min="0"
                                step="0.01"
                                required
                                :rules="priceRules"
                                ></v-text-field>
                            </v-col>

                            <!-- Fournisseur -->
                            <v-col cols="12">
                                <v-autocomplete
                                v-model="purchase.fournisseur"
                                :items="suppliers"
                                item-title="nom"
                                item-value="id"
                                label="Fournisseur"
                                required
                                :rules="supplierRules"
                                :loading="loadingSuppliers"
                                clearable
                                ></v-autocomplete>
                            </v-col>

                            <!-- Fabricant -->
                            <v-col cols="12">
                                <v-autocomplete
                                v-model="purchase.fabricant"
                                :items="manufacturers"
                                item-title="nom"
                                item-value="id"
                                label="Fabricant"
                                required
                                :rules="manufacturerRules"
                                :loading="loadingManufacturers"
                                clearable
                                ></v-autocomplete>
                            </v-col>
                            </v-row>
                        </v-container>
                </v-form>
                </v-card>
            </template>

            <template v-slot:item.2>
                <v-card flat>
                    <v-card-text>
                        <div class="d-flex justify-space-between mb-4">
                            <strong>Total Acheté: {{ purchase.quantite }}</strong>
                            <strong>Distribué: {{ totalDistributed }}</strong>
                            <strong :class="remainingToDistribute === 0 ? 'text-success' : 'text-error'">
                                Reste: {{ remainingToDistribute }}
                            </strong>
                        </div>
                    
                        <v-list density="compact">
                            <v-list-item v-for="store in distributionList" :key="store.id">
                                <template v-slot:prepend>
                                    <v-checkbox v-model="store.selected" density="compact" hide-details></v-checkbox>
                                </template>
                                <v-list-item-title>{{ store.nom }}</v-list-item-title>
                                <template v-slot:append>
                                    <v-text-field
                                        v-model.number="store.quantite"
                                        type="number"
                                        min="0"
                                        density="compact"
                                        hide-details
                                        style="width: 100px"
                                        :disabled="!store.selected"
                                    ></v-text-field>
                                </template>
                            </v-list-item>
                        </v-list>
                        <v-alert v-if="remainingToDistribute !== 0" type="warning" density="compact" variant="tonal" class="mt-2">
                            Vous devez distribuer exactement la quantité achetée.
                        </v-alert>
                    </v-card-text>
                </v-card>
            </template>
            </v-stepper>
            
            <div class="d-flex justify-end pa-4">
                <v-btn v-if="step > 1" variant="text" @click="step--">Précédent</v-btn>
                <v-spacer></v-spacer>
                <v-btn color="blue-darken-1" variant="text" @click="close">Annuler</v-btn>
                <v-btn 
                    v-if="step < 2" 
                    color="primary" 
                    @click="nextStep" 
                    :disabled="!valid"
                    class="ml-2"
                >
                    Suivant
                </v-btn>
                <v-btn 
                    v-else 
                    color="primary" 
                    @click="save" 
                    :disabled="remainingToDistribute !== 0 || loading"
                    :loading="loading"
                    class="ml-2"
                >
                Confirmer Achat
                </v-btn>
            </div>
        </template>
    </BaseForm>
  </v-dialog>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';
import BaseForm from '@/components/common/BaseForm.vue';

const props = defineProps({
  modelValue: Boolean,
  consumableId: {
    type: [Number, String],
    required: true
  }
});
// ... (rest of script as before, minimal changes needed except imports)
const emit = defineEmits(['update:modelValue', 'purchase-added']);
const api = useApi(API_BASE_URL);
const dialog = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
});

const step = ref(1);
const valid = ref(false);
const loading = ref(false);
// ... (data refs same as before)
// Data for selects
const suppliers = ref([]);
const manufacturers = ref([]);
const stores = ref([]);
const loadingSuppliers = ref(false);
const loadingManufacturers = ref(false);

const purchase = ref({
  date_reference_prix: new Date().toISOString().substr(0, 10),
  quantite: 1,
  prix_unitaire: 0,
  fournisseur: null,
  fabricant: null
});
const distributionList = ref([]);

// Rules
const dateRules = [v => !!v || 'La date est requise'];
const quantityRules = [
  v => !!v || 'La quantité est requise',
  v => v > 0 || 'La quantité doit être positive'
];
const priceRules = [
  v => v !== null && v !== '' || 'Le prix est requis',
  v => v >= 0 || 'Le prix doit être positif'
];
const supplierRules = [v => !!v || 'Le fournisseur est requis'];
const manufacturerRules = [v => !!v || 'Le fabricant est requis'];

const totalDistributed = computed(() => {
    return distributionList.value
        .filter(s => s.selected)
        .reduce((sum, s) => sum + (parseInt(s.quantite) || 0), 0);
});

const remainingToDistribute = computed(() => {
    return (parseInt(purchase.value.quantite) || 0) - totalDistributed.value;
});

// Fetch functions same as before
const fetchSuppliers = async () => {
  loadingSuppliers.value = true;
  try {
    const response = await api.get('fournisseurs/');
    suppliers.value = response.results || response; 
  } catch (e) {
    console.error('Error fetching suppliers', e);
  } finally {
    loadingSuppliers.value = false;
  }
};
const fetchManufacturers = async () => {
  loadingManufacturers.value = true;
  try {
    const response = await api.get('fabricants/');
    manufacturers.value = response.results || response;
  } catch (e) {
    console.error('Error fetching manufacturers', e);
  } finally {
    loadingManufacturers.value = false;
  }
};
const fetchStores = async () => {
    try {
        const response = await api.get('magasins/');
        stores.value = response.results || response;
        distributionList.value = stores.value.map(s => ({
            id: s.id,
            nom: s.nom,
            quantite: 0,
            selected: false
        }));
    } catch (e) {
        console.error('Error fetching stores', e);
    }
};

onMounted(() => {
  fetchSuppliers();
  fetchManufacturers();
  fetchStores();
});

const nextStep = () => {
    if (step.value === 1 && valid.value) {
        step.value = 2;
    }
};

const close = () => {
  dialog.value = false;
  step.value = 1;
};

const save = async () => {
  if (remainingToDistribute.value !== 0) return;
  loading.value = true;
  try {
    const payload = {
      consommable: props.consumableId,
      fournisseur: purchase.value.fournisseur,
      fabricant: purchase.value.fabricant,
      quantite: purchase.value.quantite,
      prix_unitaire: purchase.value.prix_unitaire,
      date_reference_prix: purchase.value.date_reference_prix,
      distribution: distributionList.value
        .filter(s => s.selected && s.quantite > 0)
        .map(s => ({ magasin: s.id, quantite: s.quantite }))
    };
    await api.post('fournitures/', payload);
    emit('purchase-added');
    close();
    step.value = 1;
    purchase.value = {
        date_reference_prix: new Date().toISOString().substr(0, 10),
        quantite: 1,
        prix_unitaire: 0,
        fournisseur: null,
        fabricant: null
    };
    distributionList.value.forEach(s => {
        s.quantite = 0;
        s.selected = false;
    });

  } catch (error) {
    console.error('Error saving purchase', error);
  } finally {
    loading.value = false;
  }
};
</script>
