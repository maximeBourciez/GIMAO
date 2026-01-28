<template>
  <v-container fluid style="max-width: 90%">
    <div class="dashboard">

      <!-- STATS COMPONENT -->
      <StatsComponent v-if="hasStats" :perms="getPermsForStats" />

      <div v-if="role === 'Responsable GMAO'" class="row two-columns">
        <!-- FAILURE LIST COMPONENT -->
        <FailureListComponent
          :compact="true"
          :limit="5"
          :show-create-button="true"
          @row-click="handleRowClickDI"
          @create-click="handleCreateDI"
        />

        <!-- INTERVENTION LIST COMPONENT -->
        <InterventionListComponent
          :compact="true"
          :limit="5"
          :show-create-button="true"
          @row-click="handleRowClickBT"
          @create-click="handleCreateBT"
        />
      </div>

      <div v-else class="column">
        <!-- FAILURE LIST COMPONENT -->
        <FailureListComponent
          :compact="true"
          :limit="5"
          :show-create-button="true"
          @row-click="handleRowClickDI"
          @create-click="handleCreateDI"
        />

        <!-- INTERVENTION LIST COMPONENT -->
        <InterventionListComponent
          :compact="true"
          :limit="5"
          :show-create-button="true"
          @row-click="handleRowClickBT"
          @create-click="handleCreateBT"
        />
      </div>

    </div>
  </v-container>
</template>


<script setup>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

import FailureListComponent from '@/components/FailureListComponent.vue'
import InterventionListComponent from '@/components/InterventionListComponent.vue'
import StatsComponent from '@/components/StatsComponent.vue'
import Stocks from '@/views/Stocks/Stocks.vue'

const store = useStore()
const router = useRouter()

const role = computed(() => store.getters.userRole)

/**
 * Helpers
 */
const getPermsForStats = () => {
  const perm = store.getters.hasPermission('dash:stats.full') || store.getters.hasPermission('dash:stats.bt') || store.getters.hasPermission('dash:stats.di')
  return perm
}

const hasStats = computed(() => {
  return store.getters.hasPermission('dash:stats.full') || store.getters.hasPermission('dash:stats.bt') || store.getters.hasPermission('dash:stats.di')
})

onMounted(() => {
  console.log('Dashboard mounted - role:', role.value)
})

const logout = () => {
  // Supprimer les données du store et du localStorage
  store.dispatch('logout');

  // Rediriger vers login avec un reload complet pour nettoyer tout le state
  window.location.href = '/login';
}

// Gestion click DI
const handleRowClickDI = (failure) => {
  router.push({ name: 'FailureDetail', params: { id: failure.id } })
}

const handleCreateDI = () => {
  router.push({ name: 'CreateFailure', query: { from: 'dashboard' } })
}

// Gestion click BT
const handleRowClickBT = (intervention) => {
  router.push({ name: 'InterventionDetail', params: { id: intervention.id } })
}

const handleCreateBT = () => {
  router.push({
    name: 'CreateIntervention',
    query: { from: 'dashboard' }
  })
}

const statsFull = computed(() => isResponsable.value)
</script>



<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Responsable : 2 colonnes */
.row.two-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

/* Technicien / Opérateur : vertical */
.column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Responsive */
@media (max-width: 900px) {
  .row.two-columns {
    grid-template-columns: 1fr;
  }
}

.floating-logout-button {
  position: fixed !important;
  bottom: 24px;
  left: 24px;
  z-index: 100;
  border-radius: 5px !important;
  width: auto !important;
  padding: 0 12px !important;
}

.floating-logout-button-magasinier {
  position: fixed !important;
  bottom: 24px;
  left: 24px;
  z-index: 100;
}
</style>
