<template>
  <v-card class="rounded-lg">
    <v-card-title class="text-h5 text-primary font-weight-bold pb-1">
      BT en attente de validation
    </v-card-title>
    <v-card-subtitle class="pb-3">
      {{ bonsWithPendingConsommables.length }} bon(s) de travail en attente de validation
    </v-card-subtitle>

    <v-card-text class="pt-0">
      <!-- Loading -->
      <div v-if="loading" class="text-center py-4">
        <v-progress-circular indeterminate color="primary" size="32" />
      </div>

      <!-- Liste vide -->
      <v-alert 
        v-else-if="bonsWithPendingConsommables.length === 0" 
        type="success" 
        variant="tonal"
        icon="mdi-check-circle"
      >
        Aucun bon de travail en attente de distribution
      </v-alert>

      <!-- Liste des BT -->
      <div v-else class="bt-list">
        <v-expansion-panels variant="accordion">
          <v-expansion-panel
            v-for="bt in bonsWithPendingConsommables"
            :key="bt.id"
            class="bt-item mb-2"
            elevation="0"
          >
            <v-expansion-panel-title class="py-3">
              <div class="d-flex align-center flex-grow-1">
                <v-icon color="primary" size="20" class="mr-3">mdi-wrench</v-icon>
                <div class="bt-info">
                  <span class="bt-name">{{ bt.nom }}</span>
                  <span class="bt-date">Date: {{ formatDate(bt.date_assignation) }}</span>
                </div>
                <v-chip 
                  size="small" 
                  color="primary" 
                  variant="tonal"
                  class="ml-auto mr-2"
                >
                  {{ getPendingCount(bt) }} consomable(s)
                </v-chip>
              </div>
            </v-expansion-panel-title>

            <v-expansion-panel-text>
              <v-list density="compact" class="py-0">
                <v-list-item
                  v-for="cons in getPendingConsommables(bt)"
                  :key="cons.consommable"
                  class="consommable-item px-0"
                >
                  <template #prepend>
                    <v-avatar size="36" rounded="lg" class="mr-3">
                      <v-img 
                        v-if="cons.image" 
                        :src="cons.image" 
                        cover
                      />
                      <v-icon v-else color="grey">mdi-package-variant</v-icon>
                    </v-avatar>
                  </template>

                  <v-list-item-title class="text-body-2">
                    {{ cons.designation }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-caption">
                    Quantité demandée : {{ cons.quantite }}
                  </v-list-item-subtitle>

                  <template #append>
                    <v-btn
                      color="success"
                      size="small"
                      variant="tonal"
                      :loading="distributingId === `${bt.id}-${cons.consommable}`"
                      @click="handleDistribute(bt, cons)"
                    >
                      <v-icon size="18" class="mr-1">mdi-check</v-icon>
                      Distribuer
                    </v-btn>
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
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const api = useApi(API_BASE_URL);
const emit = defineEmits(['count-updated']);

const bonsTravail = ref([]);
const loading = ref(false);
const distributingId = ref(null);
const distributingAll = ref(null);

// Filtrer les BT qui ont des consommables non distribués
const bonsWithPendingConsommables = computed(() => {
  return bonsTravail.value.filter(bt => 
    bt.consommables?.some(c => !c.distribue)
  );
});

// Émettre le count quand il change
watch(bonsWithPendingConsommables, (newVal) => {
  emit('count-updated', newVal.length);
}, { immediate: true });

// Récupérer les consommables non distribués d'un BT
const getPendingConsommables = (bt) => {
  return bt.consommables?.filter(c => !c.distribue) || [];
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