<template>
  <div class="dashboard">

    <!-- ================= RESPONSABLE ================= -->
    <template v-if="isResponsable">
      <StatsComponent :role="role" />

      <v-row>
        <v-col cols="6">
          <FailureListComponent @create="handleCreate" @row-click="handleRowClick" />
        </v-col>
        <v-col cols="6">
          <InterventionListComponent />
        </v-col>
      </v-row>
    </template>

    <!-- ============ TECHNICIEN / OPERATEUR ============ -->
    <template v-else-if="isTechnicien || isOperateur">
      <StatsComponent :role="role" />

      <v-col cols="10" class="mx-auto">
        <InterventionListComponent />
        <FailureListComponent @create="handleCreate" @row-click="handleRowClick" />
      </v-col>
    </template>

    <!-- ================= MAGASINIER ================= -->
    <template v-else-if="isMagasinier">
      <Stocks />
    </template>

  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'

import FailureListComponent from '@/components/FailureListComponent.vue'
import InterventionListComponent from '@/components/InterventionListComponent.vue'
import StatsComponent from '@/components/StatsComponent.vue'
import Stocks from '@/views/Stocks/Stocks.vue'

const store = useStore()

const role = computed(() => store.getters.userRole)

/**
 * Helpers
 */
const isResponsable = computed(() => role.value === 'Responsable GMAO')
const isTechnicien = computed(() => role.value === 'Technicien')
const isOperateur = computed(() => role.value === 'Opérateur')
const isMagasinier = computed(() => role.value === 'Magasinier')

onMounted(() => {
  console.log('Dashboard mounted - role:', role.value)
})

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
</style>
