<template>
  <v-card class="rounded-lg">
    <v-card-title class="text-h5 text-primary font-weight-bold pb-1">
      BT en attente de mise de cote
    </v-card-title>
    <v-card-subtitle class="pb-3">
      {{ pendingBons.length }} en attente, {{ reservedBons.length }} mis de cote, {{ recoveredBons.length }} recupere
    </v-card-subtitle>

    <v-card-text class="pt-0">
      <!-- Loading -->
      <div v-if="loading" class="text-center py-4">
        <v-progress-circular indeterminate color="primary" size="32" />
      </div>

      <!-- Liste vide -->
      <v-alert 
        v-else-if="pendingBons.length === 0 && reservedBons.length === 0 && recoveredBons.length === 0" 
        type="success" 
        variant="tonal"
        icon="mdi-check-circle"
      >
        Aucun bon de travail en attente de mise de cote
      </v-alert>

      <v-alert
        v-if="stockError"
        type="warning"
        variant="tonal"
        icon="mdi-alert-circle"
        class="mb-3"
      >
        {{ stockError }}
      </v-alert>

      <!-- Liste des BT -->
      <div v-else class="bt-list">
        <div v-if="pendingBons.length > 0">
          <div class="section-title">En attente</div>
          <v-expansion-panels variant="accordion">
          <v-expansion-panel
            v-for="bt in pendingBons"
            :key="bt.id"
            class="bt-item mb-2"
            elevation="0"
          >
            <v-expansion-panel-title class="py-3">
              <v-row no-gutters align="center" class="w-100">
                <v-col cols="8" class="d-flex align-center">
                  <v-icon color="primary" size="20" class="mr-3">mdi-wrench</v-icon>
                  <div class="bt-info">
                    <span class="bt-name">{{ bt.nom }}</span>
                    <span class="bt-date">Date: {{ formatDate(bt.date_assignation) }}</span>
                  </div>
                </v-col>
                <v-col cols="4" class="text-right">
                  <v-chip 
                    size="small" 
                    color="primary" 
                    variant="tonal"
                  >
                    {{ getPendingCount(bt) }} consomable(s)
                  </v-chip>
                </v-col>
              </v-row>
            </v-expansion-panel-title>

            <v-expansion-panel-text>
              <v-list density="compact" class="py-0">
                <v-list-item
                  v-for="cons in getPendingConsommables(bt)"
                  :key="cons.consommable"
                  class="consommable-item px-0"
                >
                  <template #prepend>
                    <v-icon color="grey" class="mr-3">mdi-package-variant</v-icon>
                  </template>

                  <v-list-item-title class="text-body-2">
                    {{ cons.designation }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-caption">
                    Quantite demandee : {{ cons.quantite }}
                  </v-list-item-subtitle>

                  <template #append>
                    <v-btn
                      v-if="!isReserved(cons)"
                      color="warning"
                      size="small"
                      variant="tonal"
                      :loading="distributingId === `${bt.id}-${cons.consommable}`"
                      @click="requestDistribute(bt, cons)"
                    >
                      <v-icon size="18" class="mr-1">mdi-package-variant-closed</v-icon>
                      Mettre de cote
                    </v-btn>
                    <v-btn
                      v-else
                      color="success"
                      size="small"
                      variant="outlined"
                      disabled
                    >
                      <v-icon size="18" class="mr-1">mdi-check</v-icon>
                      Mis de cote
                    </v-btn>
                  </template>
                </v-list-item>
              </v-list>

              <!-- Bouton tout mettre de cote -->
              <div class="d-flex justify-end mt-3 pt-3 border-t">
                <v-btn
                  color="success"
                  variant="flat"
                  size="small"
                  :loading="distributingAll === bt.id"
                  @click="requestReserveAll(bt)"
                >
                  <v-icon size="18" class="mr-1">mdi-check-all</v-icon>
                  Tout mettre de cote
                </v-btn>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>
          </v-expansion-panels>
        </div>

        <div v-if="reservedBons.length > 0" class="mt-4">
          <div class="section-title">Mis de cote</div>
          <v-expansion-panels variant="accordion">
            <v-expansion-panel
              v-for="bt in reservedBons"
              :key="bt.id"
              class="bt-item mb-2"
              elevation="0"
            >
            <v-expansion-panel-title class="py-3">
              <v-row no-gutters align="center" class="w-100">
                <v-col cols="8" class="d-flex align-center">
                  <v-icon color="success" size="20" class="mr-3">mdi-check-circle</v-icon>
                  <div class="bt-info">
                    <span class="bt-name">{{ bt.nom }}</span>
                    <span class="bt-date">Date: {{ formatDate(bt.date_assignation) }}</span>
                  </div>
                </v-col>
                <v-col cols="4" class="text-right">
                  <v-chip 
                    size="small" 
                    color="success" 
                    variant="tonal"
                  >
                    Toutes pieces mises de cote
                  </v-chip>
                </v-col>
              </v-row>
            </v-expansion-panel-title>

              <v-expansion-panel-text>
                <v-list density="compact" class="py-0">
                  <v-list-item
                    v-for="cons in getAllConsommables(bt)"
                    :key="cons.consommable"
                    class="consommable-item px-0"
                  >
                  <template #prepend>
                    <v-icon color="grey" class="mr-3">mdi-package-variant</v-icon>
                  </template>
                  <v-list-item-title class="text-body-2">
                    {{ cons.designation }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-caption">
                    Quantite demandee : {{ cons.quantite }}
                  </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
                <div class="d-flex justify-end mt-3 pt-3 border-t ga-2">
                  <v-btn
                    color="error"
                    variant="outlined"
                    size="small"
                    @click="requestCancelReserve(bt)"
                  >
                    <v-icon size="18" class="mr-1">mdi-close</v-icon>
                    Annuler
                  </v-btn>
                  <v-btn
                    color="success"
                    variant="flat"
                    size="small"
                    @click="requestSetRecupere(bt)"
                  >
                    <v-icon size="18" class="mr-1">mdi-check</v-icon>
                    Recupere
                  </v-btn>
                </div>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>

        <div v-if="recoveredBons.length > 0" class="mt-4">
          <div class="section-title">Recupere</div>
          <v-expansion-panels variant="accordion">
            <v-expansion-panel
              v-for="bt in recoveredBons"
              :key="bt.id"
              class="bt-item mb-2"
              elevation="0"
            >
              <v-expansion-panel-title class="py-3">
                <v-row no-gutters align="center" class="w-100">
                  <v-col cols="8" class="d-flex align-center">
                    <v-icon color="success" size="20" class="mr-3">mdi-check-circle</v-icon>
                    <div class="bt-info">
                      <span class="bt-name">{{ bt.nom }}</span>
                      <span class="bt-date">Date: {{ formatDate(bt.date_assignation) }}</span>
                    </div>
                  </v-col>
                  <v-col cols="4" class="text-right">
                    <v-chip 
                      size="small" 
                      color="success" 
                      variant="tonal"
                    >
                      Pieces recuperees
                    </v-chip>
                  </v-col>
                </v-row>
              </v-expansion-panel-title>

              <v-expansion-panel-text>
                <v-list density="compact" class="py-0">
                  <v-list-item
                    v-for="cons in getAllConsommables(bt)"
                    :key="cons.consommable"
                    class="consommable-item px-0"
                  >
                    <template #prepend>
                      <v-icon color="grey" class="mr-3">mdi-package-variant</v-icon>
                    </template>

                    <v-list-item-title class="text-body-2">
                      {{ cons.designation }}
                    </v-list-item-title>
                    <v-list-item-subtitle class="text-caption">
                      Quantite demandee : {{ cons.quantite }}
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </div>
      </div>
    </v-card-text>
  </v-card>

  <ConfirmationModal
    v-model="confirmDialog"
    type="warning"
    title="Confirmer la mise de cote"
    message="Etes-vous sur de vouloir mettre ce consommable de cote ?"
    confirm-text="Mettre de cote"
    confirm-icon="mdi-check"
    :loading="confirmLoading"
    @confirm="confirmDistribute"
    @cancel="confirmDialog = false"
  />

  <ConfirmationModal
    v-model="confirmAllDialog"
    type="warning"
    title="Confirmer la mise de cote"
    message="Etes-vous sur de vouloir mettre de cote tous les consommables de ce BT ?"
    confirm-text="Tout mettre de cote"
    confirm-icon="mdi-check"
    :loading="confirmAllLoading"
    @confirm="confirmReserveAll"
    @cancel="confirmAllDialog = false"
  />

  <ConfirmationModal
    v-model="confirmCancelDialog"
    type="warning"
    title="Confirmer l'annulation"
    message="Etes-vous sur de vouloir annuler la mise de cote pour ce BT ?"
    confirm-text="Annuler"
    confirm-icon="mdi-close"
    :loading="confirmCancelLoading"
    @confirm="confirmCancelReserve"
    @cancel="confirmCancelDialog = false"
  />

  <ConfirmationModal
    v-model="confirmRecupereDialog"
    type="success"
    title="Confirmer la recuperation"
    message="Etes-vous sur de vouloir valider la recuperation de ce BT ?"
    confirm-text="Recupere"
    confirm-icon="mdi-check"
    :loading="confirmRecupereLoading"
    @confirm="confirmSetRecupere"
    @cancel="confirmRecupereDialog = false"
  />

  <v-dialog v-model="magasinDialog" max-width="420">
    <v-card class="rounded-lg">
      <v-card-title class="pa-4 pb-2">
        Choisir un magasin
      </v-card-title>
      <v-card-text class="pa-4 pt-2">
        <v-radio-group v-model="magasinSelected">
          <v-radio
            v-for="m in magasinOptions"
            :key="m.id"
            :label="`${m.nom} (dispo: ${m.quantite})`"
            :value="m.id"
          />
        </v-radio-group>
      </v-card-text>
      <v-card-actions class="pa-4 pt-0 d-flex justify-end">
        <v-btn variant="outlined" @click="magasinDialog = false">Annuler</v-btn>
        <v-btn color="primary" :disabled="!magasinSelected" @click="confirmMagasinSelection">
          Confirmer
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-dialog v-model="stockIssueDialog" max-width="560">
    <v-card class="rounded-lg">
      <v-card-title class="pa-4 pb-2 d-flex align-center">
        <v-icon color="warning" size="22" class="mr-2">mdi-alert-circle</v-icon>
        Stock insuffisant
      </v-card-title>
      <v-card-subtitle class="px-4 pb-2 text-caption text-grey">
        Impossible de mettre de cote les pieces suivantes
      </v-card-subtitle>
      <v-card-text class="pa-4 pt-2">
        <v-list density="compact" class="py-0">
          <v-list-item
            v-for="item in stockIssueItems"
            :key="`${item.consommable_id}-${item.magasin_id || 'global'}`"
            class="px-0 stock-issue-item"
          >
            <v-list-item-title class="text-body-2 d-flex align-center">
              <v-icon size="18" color="grey" class="mr-2">mdi-package-variant</v-icon>
              {{ item.designation || ('Consommable #' + item.consommable_id) }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-caption d-flex align-center ga-2">
              <v-chip size="x-small" color="error" variant="tonal">
                Besoin: {{ item.needed }}
              </v-chip>
              <v-chip size="x-small" color="warning" variant="tonal">
                Dispo: {{ item.available }}
              </v-chip>
              <v-chip v-if="item.magasin_nom" size="x-small" color="grey" variant="tonal">
                Magasin: {{ item.magasin_nom }}
              </v-chip>
            </v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-card-text>
      <v-card-actions class="pa-4 pt-0 d-flex justify-end">
        <v-btn variant="outlined" @click="stockIssueDialog = false">Fermer</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';
import ConfirmationModal from '@/components/common/ConfirmationModal.vue';

const api = useApi(API_BASE_URL);
const emit = defineEmits(['count-updated', 'counts-updated', 'stock-updated']);

const bonsTravail = ref([]);
const loading = ref(false);
const distributingId = ref(null);
const distributingAll = ref(null);
const confirmDialog = ref(false);
const confirmLoading = ref(false);
const pendingAction = ref({ bt: null, cons: null });
const confirmAllDialog = ref(false);
const confirmAllLoading = ref(false);
const pendingAllBt = ref(null);
const confirmCancelDialog = ref(false);
const confirmCancelLoading = ref(false);
const pendingCancelBt = ref(null);
const confirmRecupereDialog = ref(false);
const confirmRecupereLoading = ref(false);
const pendingRecupereBt = ref(null);
const stockError = ref('');
const magasinDialog = ref(false);
const magasinOptions = ref([]);
const magasinSelected = ref(null);
const magasinPendingAction = ref({ bt: null, cons: null });
const stockIssueDialog = ref(false);
const stockIssueItems = ref([]);
const stockIssueMessage = ref('');

// Filtrer les BT qui ont des consommables non distribués
const pendingBons = computed(() => {
  return bonsTravail.value.filter(bt => {
    const hasConsommables = (bt.consommables || []).length > 0;
    return hasConsommables && bt.consommables.some(c => !isReserved(c));
  });
});

const reservedBons = computed(() => {
  return bonsTravail.value.filter(bt => {
    const hasConsommables = (bt.consommables || []).length > 0;
    return hasConsommables && bt.consommables.every(c => isReserved(c)) && !bt.pieces_recuperees;
  });
});

const recoveredBons = computed(() => {
  return bonsTravail.value.filter(bt => bt.pieces_recuperees === true);
});

// Émettre le count quand il change
watch([pendingBons, reservedBons, recoveredBons], ([pending, reserved, recovered]) => {
  emit('count-updated', pending.length);
  emit('counts-updated', { pending: pending.length, reserved: reserved.length, recovered: recovered.length });
}, { immediate: true });

// Récupérer les consommables non distribués d'un BT
const getPendingConsommables = (bt) => {
  return bt.consommables?.filter(c => !isReserved(c)) || [];
};

const getAllConsommables = (bt) => {
  return bt.consommables || [];
};

const isReserved = (cons) => {
  return cons?.distribue === true || cons?.distribue === 1 || cons?.distribue === 'true';
};

const requestDistribute = (bt, cons) => {
  pendingAction.value = { bt, cons };
  confirmDialog.value = true;
};

const confirmDistribute = async () => {
  if (!pendingAction.value.bt || !pendingAction.value.cons) {
    confirmDialog.value = false;
    return;
  }
  confirmLoading.value = true;
  try {
    await handleDistribute(pendingAction.value.bt, pendingAction.value.cons);
  } finally {
    confirmLoading.value = false;
    confirmDialog.value = false;
    pendingAction.value = { bt: null, cons: null };
  }
};

const requestReserveAll = (bt) => {
  pendingAllBt.value = bt;
  confirmAllDialog.value = true;
};

const confirmReserveAll = async () => {
  if (!pendingAllBt.value) {
    confirmAllDialog.value = false;
    return;
  }
  confirmAllLoading.value = true;
  try {
    await handleDistributeAll(pendingAllBt.value);
  } finally {
    confirmAllLoading.value = false;
    confirmAllDialog.value = false;
    pendingAllBt.value = null;
  }
};

const confirmMagasinSelection = async () => {
  if (!magasinPendingAction.value.bt || !magasinPendingAction.value.cons || !magasinSelected.value) {
    magasinDialog.value = false;
    return;
  }
  await handleDistribute(magasinPendingAction.value.bt, magasinPendingAction.value.cons, magasinSelected.value);
  magasinDialog.value = false;
  magasinOptions.value = [];
  magasinSelected.value = null;
  magasinPendingAction.value = { bt: null, cons: null };
};

const requestCancelReserve = (bt) => {
  pendingCancelBt.value = bt;
  confirmCancelDialog.value = true;
};

const confirmCancelReserve = async () => {
  if (!pendingCancelBt.value) {
    confirmCancelDialog.value = false;
    return;
  }
  confirmCancelLoading.value = true;
  try {
    await handleCancelReserve(pendingCancelBt.value);
  } finally {
    confirmCancelLoading.value = false;
    confirmCancelDialog.value = false;
    pendingCancelBt.value = null;
  }
};

const requestSetRecupere = (bt) => {
  pendingRecupereBt.value = bt;
  confirmRecupereDialog.value = true;
};

const confirmSetRecupere = async () => {
  if (!pendingRecupereBt.value) {
    confirmRecupereDialog.value = false;
    return;
  }
  confirmRecupereLoading.value = true;
  try {
    await handleSetRecupere(pendingRecupereBt.value);
  } finally {
    confirmRecupereLoading.value = false;
    confirmRecupereDialog.value = false;
    pendingRecupereBt.value = null;
  }
};

// Compter les pièces en attente
const getPendingCount = (bt) => {
  return getPendingConsommables(bt).length;
};

// Formater la date
const formatDate = (dateString) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString('fr-FR');
};

// Charger les BT
const fetchBonsTravail = async () => {
  loading.value = true;
  try {
    const response = await api.get('bons-travail/list_stock/');
    bonsTravail.value = Array.isArray(response) ? response : [response];
  } catch (error) {
    console.error('Erreur chargement BT:', error);
  } finally {
    loading.value = false;
  }
};

// Distribuer un consommable
const handleDistribute = async (bt, consommable, magasinId = null) => {
  distributingId.value = `${bt.id}-${consommable.consommable}`;
  try {
    stockError.value = '';
    await api.patch(`bons-travail/${bt.id}/update_consommable_distribution/`, {
      consommable_id: consommable.consommable,
      distribue: true,
      magasin_id: magasinId
    });
    // Mettre à jour localement
    const btIndex = bonsTravail.value.findIndex(b => b.id === bt.id);
    if (btIndex !== -1) {
      const consIndex = bonsTravail.value[btIndex].consommables.findIndex(
        c => c.consommable === consommable.consommable
      );
      if (consIndex !== -1) {
        bonsTravail.value[btIndex].consommables[consIndex].distribue = true;
        bonsTravail.value[btIndex].consommables[consIndex].date_distribution = new Date().toISOString();
        if (magasinId) {
          bonsTravail.value[btIndex].consommables[consIndex].magasin_reserve = magasinId;
        }
      }
    }
    emit('stock-updated');
  } catch (error) {
    const data = error?.response?.data;
    if (error?.response?.status === 409 && data?.needs_magasin_selection) {
      magasinOptions.value = data.magasins || [];
      magasinSelected.value = null;
      magasinPendingAction.value = { bt, cons: consommable };
      magasinDialog.value = true;
      return;
    }
    if (data?.insuffisants) {
      stockIssueItems.value = data.insuffisants;
      stockIssueMessage.value = data.error || 'Stock insuffisant pour ce consommable.';
      stockIssueDialog.value = true;
    } else if (data?.error) {
      stockError.value = data.error;
    } else {
      stockError.value = 'Stock insuffisant pour mettre de cote ce consommable.';
    }
    console.error('Erreur distribution:', error);
  } finally {
    distributingId.value = null;
  }
};

// Distribuer tous les consommables d'un BT
const handleDistributeAll = async (bt) => {
  distributingAll.value = bt.id;
  try {
    stockError.value = '';
    const pendingConsommables = getPendingConsommables(bt);
    for (const cons of pendingConsommables) {
      await api.patch(`bons-travail/${bt.id}/update_consommable_distribution/`, {
        consommable_id: cons.consommable,
        distribue: true
      });
    }
    // Mettre à jour localement
    const btIndex = bonsTravail.value.findIndex(b => b.id === bt.id);
    if (btIndex !== -1) {
      bonsTravail.value[btIndex].consommables.forEach(c => {
        c.distribue = true;
        c.date_distribution = new Date().toISOString();
      });
    }
    emit('stock-updated');
  } catch (error) {
    const data = error?.response?.data;
    if (error?.response?.status === 409 && data?.needs_magasin_selection) {
      stockError.value = 'Choisissez un magasin en passant par la mise de cote individuelle.';
    } else if (data?.insuffisants) {
      stockIssueItems.value = data.insuffisants;
      stockIssueMessage.value = data.error || 'Stock insuffisant pour ce BT.';
      stockIssueDialog.value = true;
    } else if (data?.error) {
      stockError.value = data.error;
    } else {
      stockError.value = 'Stock insuffisant pour mettre de cote tout le BT.';
    }
    console.error('Erreur distribution multiple:', error);
  } finally {
    distributingAll.value = null;
  }
};

const handleCancelReserve = async (bt) => {
  try {
    await api.patch(`bons-travail/${bt.id}/cancel_mise_de_cote/`, {});
    const btIndex = bonsTravail.value.findIndex(b => b.id === bt.id);
    if (btIndex !== -1) {
      bonsTravail.value[btIndex].consommables.forEach(c => {
        c.distribue = false;
        c.date_distribution = null;
      });
      bonsTravail.value[btIndex].pieces_recuperees = false;
      bonsTravail.value[btIndex].date_recuperation = null;
    }
    emit('stock-updated');
  } catch (error) {
    console.error('Erreur annulation mise de cote:', error);
  }
};

const handleSetRecupere = async (bt) => {
  try {
    const response = await api.patch(`bons-travail/${bt.id}/set_recupere/`, { recupere: true });
    const btIndex = bonsTravail.value.findIndex(b => b.id === bt.id);
    if (btIndex !== -1) {
      bonsTravail.value[btIndex].pieces_recuperees = response?.pieces_recuperees ?? true;
      bonsTravail.value[btIndex].date_recuperation = response?.date_recuperation ?? new Date().toISOString();
    }
  } catch (error) {
    console.error('Erreur validation recuperation:', error);
  }
};



onMounted(() => {
  fetchBonsTravail();
});
</script>

<style scoped>
.bt-list {
  max-height: 500px;
  overflow-y: auto;
}

.section-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6B7280;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 8px;
}

.bt-item {
  border: 1px solid #E5E7EB;
  border-radius: 8px !important;
}

.bt-item:hover {
  border-color: #05004E;
}

.bt-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.bt-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #05004E;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.bt-date {
  font-size: 0.75rem;
  color: #6B7280;
}

.consommable-item {
  border-bottom: 1px solid #F3F4F6;
}

.consommable-item:last-child {
  border-bottom: none;
}

.consommable-item :deep(.v-list-item__content) {
  flex: 1 1 auto;
  min-width: 0;
}

.consommable-item :deep(.v-list-item__append) {
  margin-left: auto;
}

.stock-issue-item {
  border-bottom: 1px solid #F3F4F6;
  padding-bottom: 8px;
  margin-bottom: 8px;
}

.stock-issue-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
  margin-bottom: 0;
}

.border-t {
  border-top: 1px solid #E5E7EB;
}
</style>


