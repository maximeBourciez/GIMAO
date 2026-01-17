<template>
  <v-container fluid style="max-width: 90%">

    <!-- ================= RESPONSABLE ================= -->
    <template v-if="isResponsable">

      <!-- Stats -->
      <v-row justify="center">
        <v-col cols="12">
          <StatsComponent :role="role" />
        </v-col>
      </v-row>

      <!-- Failures / Interventions sur une ligne -->
      <v-row justify="center" class="mt-4">
        <v-col cols="12" md="6">
          <FailureListComponent @row-click="handleRowClickDI" />
        </v-col>

        <v-col cols="12" md="6">
          <InterventionListComponent @row-click="handleRowClickBT" />
        </v-col>
      </v-row>

    </template>

    <!-- ============ TECHNICIEN / OPERATEUR ============ -->
    <template v-else-if="isTechnicien || isOperateur">

      <!-- Stats -->
      <v-row justify="center">
        <v-col cols="12">
          <StatsComponent :role="role" />
        </v-col>
      </v-row>

      <!-- Interventions + Failures en colonne -->
      <v-row justify="center" class="mt-4">
        <v-col cols="12" md="10">
          <InterventionListComponent class="mb-4" @row-click="handleRowClickBT" />
          <FailureListComponent @create="handleCreate" @row-click="handleRowClickDI" />
        </v-col>
      </v-row>

      <!-- Bouton logout opérateur -->
      <v-btn v-if="isOperateur" color="primary" icon size="large" elevation="4" class="floating-logout-button"
        @click="logout">
        <v-icon>mdi-logout</v-icon>
        <v-tooltip activator="parent" location="left">
          Se déconnecter
        </v-tooltip>
      </v-btn>

    </template>

    <!-- ================= MAGASINIER ================= -->
    <template v-else-if="isMagasinier">
      <v-row justify="center">
        <v-col cols="12" md="10">
          <Stocks />
        </v-col>
      </v-row>
    </template>

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
const isResponsable = computed(() => role.value === 'Responsable GMAO')
const isTechnicien = computed(() => role.value === 'Technicien')
const isOperateur = computed(() => role.value === 'Opérateur')
const isMagasinier = computed(() => role.value === 'Magasinier')

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

// Gestion click BT
const handleRowClickBT = (intervention) => {
  router.push({ name: 'InterventionDetail', params: { id: intervention.id } })
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
  right: 24px;
  z-index: 100;
}
</style>
