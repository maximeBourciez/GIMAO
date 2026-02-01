<template>
  <BaseDetailView
    :title="consumable?.designation"
    :subtitle="''"
    :data="consumable"
    :loading="loading"
    :breadcrumbs="breadcrumbs"
    show-back-button
  >
    <!-- Contenu Principal -->
    <template #default>
      <v-row>
        <!-- Info Consommable -->
        <v-col cols="12" md="4">
          <v-card class="mb-4">
            <v-card-title>Informations</v-card-title>
            <v-card-text>
              <div v-if="consumable?.lienImageConsommable" class="mb-4 text-center">
                 <v-img :src="consumable.lienImageConsommable" max-height="200" contain></v-img>
              </div>
              <v-list density="compact">
                <v-list-item>
                  <v-list-item-title class="font-weight-bold">Désignation</v-list-item-title>
                  <v-list-item-subtitle>{{ consumable?.designation }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                   <v-list-item-title class="font-weight-bold">Seuil Stock Faible</v-list-item-title>
                   <v-list-item-subtitle>{{ consumable?.seuilStockFaible || '-' }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                   <v-list-item-title class="font-weight-bold">Quantité Totale</v-list-item-title>
                   <v-list-item-subtitle>{{ consumable?.quantite_totale }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Stocks par Magasin -->
        <v-col cols="12" md="8">
          <v-card class="mb-4">
             <v-card-title class="d-flex align-center justify-space-between">
                Stocks en Magasin
                 <v-btn
                  v-if="consumable?.stocks?.length"
                  color="secondary"
                  prepend-icon="mdi-transfer"
                  size="small"
                  variant="text"
                  @click="showTransferDialog = true"
                >
                  Transférer
                </v-btn>
             </v-card-title>
             <v-card-text>
               <v-data-table
                 v-if="consumable?.stocks?.length"
                 :headers="stockHeaders"
                 :items="consumable.stocks"
                 class="elevation-1"
                 hide-default-footer
                 :items-per-page="-1"
                 density="compact"
               >
               </v-data-table>
               <v-alert v-else type="info" variant="tonal" class="mt-2">
                 Aucun stock enregistré.
               </v-alert>
             </v-card-text>
          </v-card>

          <!-- Historique des Achats (Fournitures) -->
          <v-card>
             <v-card-title class="d-flex align-center justify-space-between">
                Historique des Achats
                <v-btn
                  color="primary"
                  prepend-icon="mdi-plus"
                  size="small"
                  @click="showAddPurchaseDialog = true"
                >
                  Ajouter un achat
                </v-btn>
             </v-card-title>
             <v-card-text>
               <v-data-table
                 v-if="consumable?.fournitures?.length"
                 :headers="purchaseHeaders"
                 :items="formattedPurchases"
                 class="elevation-1"
                 :items-per-page="5"
                 density="compact"
               >
                 <template #item.date_reference_prix="{ item }">
                   {{ formatDate(item.date_reference_prix) }}
                 </template>
                 <template #item.prix_unitaire="{ item }">
                   {{ formatPrice(item.prix_unitaire) }}
                 </template>
                 <template #item.total="{ item }">
                   {{ formatPrice(item.total) }}
                 </template>
               </v-data-table>
               <v-alert v-else type="info" variant="tonal" class="mt-2">
                 Aucun historique d'achat.
               </v-alert>
             </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
    
    <template #additional-content>
      <AddPurchaseForm
        v-model="showAddPurchaseDialog"
        :consumable-id="route.params.id"
        @purchase-added="fetchConsumable"
      />
      <TransferStockForm
        v-model="showTransferDialog"
        :consumable="consumable"
        @transfer-complete="fetchConsumable"
      />
    </template>
  </BaseDetailView>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import BaseDetailView from '@/components/common/BaseDetailView.vue';
import AddPurchaseForm from './AddPurchaseForm.vue';
import TransferStockForm from './TransferStockForm.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const route = useRoute();
const router = useRouter();
const api = useApi(API_BASE_URL);
const consumable = ref(null);
const loading = ref(false);
const showAddPurchaseDialog = ref(false);
const showTransferDialog = ref(false);

const stockHeaders = [
  { title: 'Magasin', key: 'magasin_nom' },
  { title: 'Quantité', key: 'quantite' },
];

const purchaseHeaders = [
  { title: 'Date', key: 'date_reference_prix' },
  { title: 'Fournisseur', key: 'fournisseur_nom' },
  { title: 'Fabricant', key: 'fabricant_nom' },
  { title: 'Qté', key: 'quantite' },
  { title: 'Prix Unitaire', key: 'prix_unitaire' },
  { title: 'Total', key: 'total' },
];

const breadcrumbs = [
  { title: 'Stocks', disabled: false, href: '/stocks' },
  { title: 'Consommables', disabled: false, href: '/stocks/consommables' },
  { title: 'Détail', disabled: true },
];

const fetchConsumable = async () => {
  loading.value = true;
  try {
    const response = await api.get(`consommables/${route.params.id}/`);
    consumable.value = response;
  } catch (error) {
    console.error('Erreur chargement consommable', error);
  } finally {
    loading.value = false;
  }
};
// ... (rest of script)

const formattedPurchases = computed(() => {
    if (!consumable.value?.fournitures) return [];
    return consumable.value.fournitures.map(achat => ({
        ...achat,
        total: achat.quantite * achat.prix_unitaire
    }));
});

const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('fr-FR');
};

const formatPrice = (price) => {
    if (!price) return '-';
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(price);
};

onMounted(fetchConsumable);
</script>
