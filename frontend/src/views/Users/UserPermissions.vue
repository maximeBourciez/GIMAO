<template>
  <v-app>
    <v-main>
      <v-container>

        <!-- En-tête -->
        <div class="d-flex align-center justify-space-between mb-4">
          <div>
            <h2 class="text-h5 font-weight-bold">Permissions de l'utilisateur</h2>
            <p v-if="utilisateur" class="text-body-2 text-medium-emphasis mt-1">
              {{ utilisateur.prenom }} {{ utilisateur.nomFamille }}
              <v-chip size="x-small" variant="tonal" color="primary" class="ml-2">
                {{ utilisateur.role?.nomRole }}
              </v-chip>
              <v-chip v-if="utilisateur.a_permissions_personnalisees" size="x-small" variant="tonal" color="warning"
                class="ml-1">
                Permissions personnalisées
              </v-chip>
            </p>
          </div>
          <v-btn variant="text" prepend-icon="mdi-arrow-left"
            @click="$router.push({ name: 'UserDetail', params: { id: userId } })">
            Retour
          </v-btn>
        </div>

        <!-- Chargement -->
        <v-alert v-if="loading" type="info" variant="tonal" class="mb-4">
          <v-progress-circular indeterminate size="20" class="mr-2" />
          Chargement...
        </v-alert>

        <!-- Erreur globale -->
        <v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-4" closable
          @click:close="errorMessage = ''">
          {{ errorMessage }}
        </v-alert>

        <!-- Succès -->
        <v-alert v-if="successMessage" type="success" variant="tonal" class="mb-4" closable
          @click:close="successMessage = ''">
          {{ successMessage }}
        </v-alert>

        <template v-if="!loading && utilisateur">

          <!-- Bandeau info permissions -->
          <v-sheet class="pa-4 mb-4" elevation="1" rounded>
            <div class="d-flex align-center justify-space-between flex-wrap gap-2">
              <div>
                <p class="text-body-1 font-weight-medium mb-1">
                  Source des permissions actuelles :
                  <v-chip :color="utilisateur.a_permissions_personnalisees ? 'warning' : 'primary'" variant="tonal"
                    size="small" class="ml-1">
                    {{ utilisateur.a_permissions_personnalisees ? 'Personnalisées' : `Rôle :
                    ${utilisateur.role?.nomRole}` }}
                  </v-chip>
                </p>
                <p class="text-body-2 text-medium-emphasis">
                  {{ selectedIds.length }} permission(s) sélectionnée(s) sur {{ allPermissions.length }}
                </p>
              </div>
              <div class="d-flex gap-2 flex-wrap">
                <v-btn variant="outlined" color="secondary" size="small" prepend-icon="mdi-content-copy"
                  @click="copyFromRole">
                  Copier depuis le rôle
                </v-btn>
                <v-btn color="primary" size="small" prepend-icon="mdi-content-save" :loading="saving"
                  @click="savePermissions">
                  Enregistrer
                </v-btn>
              </div>
            </div>
          </v-sheet>

          <!-- Recherche -->
          <v-text-field v-model="searchPerm" placeholder="Rechercher une permission..." prepend-inner-icon="mdi-magnify"
            variant="outlined" density="compact" clearable class="mb-4" />

          <!-- Permissions groupées par module -->
          <div v-for="(types, module) in filteredPermissionsByModule" :key="module" class="mb-2">
            <v-expansion-panels variant="accordion">
              <v-expansion-panel>
                <v-expansion-panel-title>
                  <div class="d-flex align-center" style="gap: 12px;">
                    <v-checkbox :model-value="isModuleFullySelected([...types.affichage, ...types.action])"
                      :indeterminate="isModulePartiallySelected([...types.affichage, ...types.action])"
                      density="compact" hide-details color="primary"
                      @update:model-value="toggleModule([...types.affichage, ...types.action], $event)" @click.stop />
                    <span class="font-weight-medium">{{ types.nom }}</span>
                    <v-chip size="x-small" color="primary" variant="tonal">
                      {{[...types.affichage, ...types.action].filter(p => selectedIds.includes(p.id)).length}}/{{
                        types.affichage.length + types.action.length }}
                    </v-chip>
                  </div>
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  <!-- Permissions d'affichage -->
                  <div v-if="types.affichage.length > 0" class="mb-3">
                    <div class="text-caption font-weight-bold text-medium-emphasis mb-1 d-flex align-center"
                      style="gap: 6px;">
                      <v-icon size="14" color="blue">mdi-eye</v-icon>
                      AFFICHAGE
                    </div>
                    <div v-for="perm in types.affichage" :key="perm.id" class="d-flex align-center">
                      <v-checkbox :model-value="selectedIds.includes(perm.id)"
                        :label="perm.description" density="compact" hide-details color="blue"
                        @update:model-value="togglePermission(perm.id, $event)" />
                    </div>
                  </div>
                  <!-- Permissions d'action -->
                  <div v-if="types.action.length > 0">
                    <div class="text-caption font-weight-bold text-medium-emphasis mb-1 d-flex align-center"
                      style="gap: 6px;">
                      <v-icon size="14" color="orange">mdi-lightning-bolt</v-icon>
                      ACTIONS
                    </div>
                    <div v-for="perm in types.action" :key="perm.id" class="d-flex align-center">
                      <v-checkbox :model-value="selectedIds.includes(perm.id)"
                        :label="perm.description" density="compact" hide-details color="orange"
                        :disabled="isPermDisabledByHierarchy(perm.nomPermission)"
                        @update:model-value="togglePermission(perm.id, $event)" />
                    </div>

                    <p v-if="Object.keys(filteredPermissionsByModule).length === 0"
                      class="text-body-2 text-medium-emphasis text-center mt-4">
                      Aucune permission trouvée.
                    </p>
                  </div>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </div>
        </template>

      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import { API_BASE_URL } from '@/utils/constants'
import { usePermissionSelector } from '@/composables/usePermissionSelector'

const props = defineProps({
  id: {
    type: [String, Number],
    required: true
  }
})

const api = useApi(API_BASE_URL)

// ==================== ÉTAT ====================
const userId = computed(() => props.id)
const utilisateur = ref(null)
const allPermissions = ref([])
const selectedIds = ref([])
const loading = ref(false)
const saving = ref(false)
const resetting = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const searchPerm = ref('')

const {
  filteredPermissionsByModule,
  isPermDisabledByHierarchy,
  isModuleFullySelected,
  isModulePartiallySelected,
  toggleModule,
  togglePermission,
  applyHierarchy,
} = usePermissionSelector(allPermissions, selectedIds, searchPerm)

// ==================== CHARGEMENT ====================
const fetchData = async () => {
  loading.value = true
  errorMessage.value = ''
  try {
    const [userRes, permsRes, userPermsRes] = await Promise.all([
      api.get(`utilisateurs/${userId.value}/`),
      api.get('permissions/'),
      api.get(`utilisateurs/${userId.value}/permissions/`)
    ])

    utilisateur.value = userRes
    console.log('userRes:', JSON.stringify(userRes))
    allPermissions.value = Array.isArray(permsRes) ? permsRes : []
    selectedIds.value = (userPermsRes.permissions || []).map(p => p.id)

    applyHierarchy()
  } catch (e) {
    errorMessage.value = 'Erreur lors du chargement des données.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)

// ==================== ACTIONS ====================

// Copier les permissions du rôle dans la sélection courante
const copyFromRole = () => {
  if (utilisateur.value?.role?.permissions) {
    selectedIds.value = utilisateur.value.role.permissions.map(p => p.id)
    successMessage.value = 'Permissions copiées depuis le rôle. N\'oubliez pas d\'enregistrer.'
  }
}

// Enregistrer les permissions personnalisées
const savePermissions = async () => {
  saving.value = true
  errorMessage.value = ''
  successMessage.value = ''

  const menuViewPerm = allPermissions.value.find(p => p.nomPermission === 'menu:view')
  if (menuViewPerm && !selectedIds.value.includes(menuViewPerm.id)) {
    const continuer = confirm('Attention : la permission "Accéder au menu de navigation" n\'est pas cochée. L\'utilisateur n\'aura pas accès à la sidebar. Continuer quand même ?')
    if (!continuer) {
      saving.value = false
      return
    }
  }

  try {
    await api.post(`utilisateurs/${userId.value}/definir_permissions/`, {
      permissions_ids: selectedIds.value
    })
    successMessage.value = 'Permissions enregistrées avec succès.'
    await fetchData()
  } catch (e) {
    errorMessage.value = 'Erreur lors de l\'enregistrement des permissions.'
  } finally {
    saving.value = false
  }
}

// Réinitialiser aux permissions du rôle
const resetToRole = async () => {
  resetting.value = true
  errorMessage.value = ''
  successMessage.value = ''
  try {
    await api.post(`utilisateurs/${userId.value}/reinitialiser_permissions/`)
    successMessage.value = 'Permissions réinitialisées. L\'utilisateur utilise maintenant les permissions de son rôle.'
    await fetchData()
  } catch (e) {
    errorMessage.value = 'Erreur lors de la réinitialisation.'
  } finally {
    resetting.value = false
  }
}
</script>
