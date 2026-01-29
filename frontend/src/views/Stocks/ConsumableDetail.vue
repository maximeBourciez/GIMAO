<template>
  <BaseDetailView
    :title="consumable?.designation"
    :subtitle="''"
    :data="consumable"
    :loading="loading"
    :breadcrumbs="breadcrumbs"
    show-back-button
    @back="goBack"
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
               <v-table v-if="consumable?.stocks?.length">
                 <thead>
                   <tr>
                     <th>Magasin</th>
                     <th>Quantité</th>
                   </tr>
                 </thead>
                 <tbody>
                   <tr v-for="stock in consumable.stocks" :key="stock.id">
                     <td>{{ stock.magasin_nom }}</td>
                     <td>{{ stock.quantite }}</td>
                   </tr>
                 </tbody>
               </v-table>
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
                <v-table v-if="consumable?.fournitures?.length">
                 <thead>
                   <tr>
                     <th>Date</th>
                     <th>Fournisseur</th>
                     <th>Fabricant</th>
                     <th>Qté</th>
                     <th>Prix Unitaire</th>
                     <th>Total</th>
                   </tr>
                 </thead>
                 <tbody>
                   <tr v-for="achat in sortedPurchases" :key="achat.id">
                     <td>{{ formatDate(achat.date_reference_prix) }}</td>
                     <td>{{ achat.fournisseur_nom }}</td>
                     <td>{{ achat.fabricant_nom }}</td>
                     <td>{{ achat.quantite }}</td>
                     <td>{{ formatPrice(achat.prix_unitaire) }}</td>
                     <td>{{ formatPrice(achat.quantite * achat.prix_unitaire) }}</td>
                   </tr>
                 </tbody>
               </v-table>
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

const sortedPurchases = computed(() => {
    if (!consumable.value?.fournitures) return [];
    return [...consumable.value.fournitures].sort((a, b) => 
        new Date(b.date_reference_prix) - new Date(a.date_reference_prix)
    );
});

const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('fr-FR');
};

const formatPrice = (price) => {
    if (!price) return '-';
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(price);
};

const goBack = () => {
    router.back();
};

onMounted(fetchConsumable);
</script>
