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
          <v-card rounded="">
            <FailureListComponent @row-click="handleRowClickDI" title="Liste des DI" :showSearch="true" />

            <v-btn color="primary" class="mt-4 float-right mr-4 mb-4" rounded="" @click="handleCreateDI">
              Créer une DI
            </v-btn>


          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card rounded="">
            <InterventionListComponent @row-click="handleRowClickBT" title="Liste des BT" :showSearch="true" />

            <v-btn color="primary" class="mt-4 float-right mr-4 mb-4" @click="handleCreateBT">
              Créer un BT
            </v-btn>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <!-- ============ TECHNICIEN ============ -->
    <template v-else-if="isTechnicien">

      <!-- Stats -->
      <v-row justify="center">
        <v-col cols="12">
          <StatsComponent :role="role" />
        </v-col>
      </v-row>

      <!-- Interventions + Failures en colonne -->
      <v-row justify="center" class="mt-4">
        <v-col cols="12" md="10">
          <v-card rounded="" class="mb-4">
            <InterventionListComponent @row-click="handleRowClickBT" title="Liste des BT" :showSearch="true" />
          </v-card>
          <v-card rounded="">
            <FailureListComponent @create="handleCreate" @row-click="handleRowClickDI" title="Liste des DI"
              :showSearch="true" />

            <v-btn color="primary" class="mt-4 float-right mr-4 mb-4" rounded="" @click="handleCreateDI">
              Créer une DI
            </v-btn>
          </v-card>
        </v-col>
      </v-row>

    </template>

    <!-- ================= OPÉRATEUR ================= -->
    <template v-else-if="isOperateur">
      <v-row justify="center" class="dashboard">

        <!-- Stats -->
        <v-col cols="12">
          <StatsComponent :role="role" :full="statsFull" />
        </v-col>




        <v-col cols="12">
          <v-card rounded="" class="mb-4">
            <FailureListComponent @row-click="handleRowClickDI" title="Liste des DI" :showSearch="true" />
            <v-btn color="primary" class="mt-4 float-right mr-4 mb-4" rounded="" @click="handleCreateDI">
              Créer une DI
            </v-btn>
          </v-card>
        </v-col>

        <v-col cols="12">
          <v-card rounded="">
            <InterventionListComponent @row-click="handleRowClickBT" title="Liste des BT" :showSearch="true" />
          </v-card>
        </v-col>
      </v-row>

      <!-- Bouton logout opérateur -->
      <v-btn v-if="isOperateur" color="primary" icon size="large" elevation="4" class="floating-logout-button"
        @click="logout">
        <v-icon class="mr-2">mdi-logout</v-icon> Se déconnecter
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

        <v-btn color="primary" icon size="large" elevation="4" class="floating-logout-button-magasinier"
          @click="logout">
          <v-icon>mdi-logout</v-icon>
          <v-tooltip activator="parent" location="left">
            Se déconnecter
          </v-tooltip>
        </v-btn>
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
