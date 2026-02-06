<template>
  <v-card class="rounded-lg">
    <v-card-title class="text-h5 text-primary font-weight-bold pb-1">
      BT en attente de validation
    </v-card-title>
    <v-card-subtitle class="pb-3">
      {{ pendingBons.length }} en attente, {{ completedBons.length }} complets
    </v-card-subtitle>

    <v-card-text class="pt-0">
      <!-- Loading -->
      <div v-if="loading" class="text-center py-4">
        <v-progress-circular indeterminate color="primary" size="32" />
      </div>

      <!-- Liste vide -->
      <v-alert 
        v-else-if="pendingBons.length === 0 && completedBons.length === 0" 
        type="success" 
        variant="tonal"
        icon="mdi-check-circle"
      >
        Aucun bon de travail en attente de distribution
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
                  <v-list-item-title class="text-body-2">
                    {{ cons.designation }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-caption">
                    Quantite demandee : {{ cons.quantite }}
                  </v-list-item-subtitle>

                  <template #prepend>
                    <v-icon color="grey" class="mr-3">mdi-package-variant</v-icon>
                  </template>

                  <template #append>
                    <div class="d-flex align-center ga-2">
                      <v-btn
                        v-if="!isDistributed(cons)"
                        color="warning"
                        size="small"
                        variant="tonal"
                        :loading="distributingId === `${bt.id}-${cons.consommable}`"
                        @click="requestDistribute(bt, cons)"
                      >
                        <v-icon size="18" class="mr-1">mdi-truck-delivery</v-icon>
                        Distribuer
                      </v-btn>
                      <v-btn
                        v-else
                        color="success"
                        size="small"
                        variant="outlined"
                        disabled
                      >
                        <v-icon size="18" class="mr-1">mdi-check</v-icon>
                        Distribue
                      </v-btn>
                    </div>
                  </template>
                </v-list-item>
              </v-list>

              <!-- Bouton distribuer tout -->
              <div class="d-flex justify-end mt-3 pt-3 border-t">
                <v-btn
                  color="success"
                  variant="flat"
                  size="small"
                  :loading="distributingAll === bt.id"
                  @click="handleDistributeAll(bt)"
                >
                  <v-icon size="18" class="mr-1">mdi-check-all</v-icon>
                  Tout distribuer
                </v-btn>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>
          </v-expansion-panels>
        </div>

        <div v-if="completedBons.length > 0" class="mt-4">
          <div class="section-title">Tout distribue</div>
          <v-expansion-panels variant="accordion">
            <v-expansion-panel
              v-for="bt in completedBons"
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
                    Toutes pieces distribuees
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
                  <v-list-item-title class="text-body-2">
                    {{ cons.designation }}
                  </v-list-item-title>
                    <v-list-item-subtitle class="text-caption">
                      Quantite demandee : {{ cons.quantite }}
                    </v-list-item-subtitle>
                  <template #prepend>
                    <v-icon color="grey" class="mr-3">mdi-package-variant</v-icon>
                  </template>
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
    title="Confirmer la distribution"
    message="Etes-vous sur de vouloir marquer ce consommable comme distribue ?"
    confirm-text="Distribuer"
    confirm-icon="mdi-check"
    :loading="confirmLoading"
    @confirm="confirmDistribute"
    @cancel="confirmDialog = false"
  />
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';
import ConfirmationModal from '@/components/common/ConfirmationModal.vue';

const api = useApi(API_BASE_URL);
const emit = defineEmits(['count-updated', 'counts-updated']);

const bonsTravail = ref([]);
const loading = ref(false);
const distributingId = ref(null);
const distributingAll = ref(null);
const confirmDialog = ref(false);
const confirmLoading = ref(false);
const pendingAction = ref({ bt: null, cons: null });

// Filtrer les BT qui ont des consommables non distribués
const pendingBons = computed(() => {
  return bonsTravail.value.filter(bt => {
    const hasConsommables = (bt.consommables || []).length > 0;
    return hasConsommables && bt.consommables.some(c => !isDistributed(c));
  });
});

const completedBons = computed(() => {
  return bonsTravail.value.filter(bt => {
    const hasConsommables = (bt.consommables || []).length > 0;
    return hasConsommables && bt.consommables.every(c => isDistributed(c));
  });
});

// Émettre le count quand il change
watch([pendingBons, completedBons], ([pending, completed]) => {
  emit('count-updated', pending.length);
  emit('counts-updated', { pending: pending.length, completed: completed.length });
}, { immediate: true });

// Récupérer les consommables non distribués d'un BT
const getPendingConsommables = (bt) => {
  return bt.consommables?.filter(c => !isDistributed(c)) || [];
};

const getAllConsommables = (bt) => {
  return bt.consommables || [];
};

const isDistributed = (cons) => {
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
const handleDistribute = async (bt, consommable) => {
  distributingId.value = `${bt.id}-${consommable.consommable}`;
  try {
    await api.patch(`bons-travail/${bt.id}/update_consommable_distribution/`, {
      consommable_id: consommable.consommable,
      distribue: true
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
      }
    }
  } catch (error) {
    console.error('Erreur distribution:', error);
  } finally {
    distributingId.value = null;
  }
};

// Distribuer tous les consommables d'un BT
const handleDistributeAll = async (bt) => {
  distributingAll.value = bt.id;
  try {
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
  } catch (error) {
    console.error('Erreur distribution multiple:', error);
  } finally {
    distributingAll.value = null;
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

.border-t {
  border-top: 1px solid #E5E7EB;
}
</style>


