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
              <v-chip v-if="utilisateur.a_permissions_personnalisees" size="x-small" variant="tonal" color="warning" class="ml-1">
                Permissions personnalisées
              </v-chip>
            </p>
          </div>
          <v-btn variant="text" prepend-icon="mdi-arrow-left" @click="$router.push({ name: 'UserDetail', params: { id: userId } })">
            Retour
          </v-btn>
        </div>

        <!-- Chargement -->
        <v-alert v-if="loading" type="info" variant="tonal" class="mb-4">
          <v-progress-circular indeterminate size="20" class="mr-2" />
          Chargement...
        </v-alert>

        <!-- Erreur globale -->
        <v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-4" closable @click:close="errorMessage = ''">
          {{ errorMessage }}
        </v-alert>

        <!-- Succès -->
        <v-alert v-if="successMessage" type="success" variant="tonal" class="mb-4" closable @click:close="successMessage = ''">
          {{ successMessage }}
        </v-alert>

        <template v-if="!loading && utilisateur">

          <!-- Bandeau info permissions -->
          <v-sheet class="pa-4 mb-4" elevation="1" rounded>
            <div class="d-flex align-center justify-space-between flex-wrap gap-2">
              <div>
                <p class="text-body-1 font-weight-medium mb-1">
                  Source des permissions actuelles :
                  <v-chip
                    :color="utilisateur.a_permissions_personnalisees ? 'warning' : 'primary'"
                    variant="tonal"
                    size="small"
                    class="ml-1"
                  >
                    {{ utilisateur.a_permissions_personnalisees ? 'Personnalisées' : `Rôle : ${utilisateur.role?.nomRole}` }}
                  </v-chip>
                </p>
                <p class="text-body-2 text-medium-emphasis">
                  {{ selectedIds.length }} permission(s) sélectionnée(s) sur {{ allPermissions.length }}
                </p>
              </div>
              <div class="d-flex gap-2 flex-wrap">
                <v-btn
                  v-if="utilisateur.a_permissions_personnalisees"
                  variant="outlined"
                  color="warning"
                  size="small"
                  prepend-icon="mdi-restore"
                  :loading="resetting"
                  @click="resetToRole"
                >
                  Réinitialiser (rôle)
                </v-btn>
                <v-btn
                  variant="outlined"
                  color="secondary"
                  size="small"
                  prepend-icon="mdi-content-copy"
                  @click="copyFromRole"
                >
                  Copier depuis le rôle
                </v-btn>
                <v-btn
                  color="primary"
                  size="small"
                  prepend-icon="mdi-content-save"
                  :loading="saving"
                  @click="savePermissions"
                >
                  Enregistrer
                </v-btn>
              </div>
            </div>
          </v-sheet>

          <!-- Recherche -->
          <v-text-field
            v-model="searchPerm"
            placeholder="Rechercher une permission..."
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            density="compact"
            clearable
            class="mb-4"
          />

          <!-- Permissions groupées par module -->
          <v-row>
            <v-col
              v-for="(perms, module) in filteredPermissionsByModule"
              :key="module"
              cols="12"
              md="6"
              lg="4"
            >
              <v-card elevation="1" rounded class="mb-2">
                <v-card-title class="d-flex align-center justify-space-between pa-3 pb-1">
                  <span class="text-body-1 font-weight-medium">{{ moduleLabel(module) }}</span>
                  <v-checkbox
                    :model-value="isModuleFullySelected(perms)"
                    :indeterminate="isModulePartiallySelected(perms)"
                    density="compact"
                    hide-details
                    color="primary"
                    @update:model-value="toggleModule(perms, $event)"
                  />
                </v-card-title>
                <v-divider />
                <v-card-text class="pa-2">
                  <v-checkbox
                    v-for="perm in perms"
                    :key="perm.id"
                    :model-value="selectedIds.includes(perm.id)"
                    :label="permActionLabel(perm.nomPermission)"
                    density="compact"
                    hide-details
                    color="primary"
                    class="mb-1"
                    @update:model-value="togglePermission(perm.id, $event)"
                  />
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <p v-if="Object.keys(filteredPermissionsByModule).length === 0" class="text-body-2 text-medium-emphasis text-center mt-4">
            Aucune permission trouvée.
          </p>

        </template>

      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import { API_BASE_URL } from '@/utils/constants'

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
    allPermissions.value = Array.isArray(permsRes) ? permsRes : []
    selectedIds.value = (userPermsRes.permissions || []).map(p => p.id)
  } catch (e) {
    errorMessage.value = 'Erreur lors du chargement des données.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)

// ==================== PERMISSIONS PAR MODULE ====================
const getModule = (nomPermission) => nomPermission.split(':')[0]

const permissionsByModule = computed(() => {
  const groups = {}
  for (const perm of allPermissions.value) {
    const module = getModule(perm.nomPermission)
    if (!groups[module]) groups[module] = []
    groups[module].push(perm)
  }
  return groups
})

const filteredPermissionsByModule = computed(() => {
  if (!searchPerm.value) return permissionsByModule.value
  const search = searchPerm.value.toLowerCase()
  const result = {}
  for (const [module, perms] of Object.entries(permissionsByModule.value)) {
    const filtered = perms.filter(p => p.nomPermission.toLowerCase().includes(search))
    if (filtered.length > 0) result[module] = filtered
  }
  return result
})

const MODULE_LABELS = {
  di: 'Demandes d\'intervention',
  bt: 'Bons de travail',
  eq: 'Équipements',
  cp: 'Compteurs',
  mp: 'Maintenances préventives',
  stock: 'Stocks',
  cons: 'Consommables',
  mag: 'Magasins',
  user: 'Utilisateurs',
  role: 'Rôles',
  loc: 'Lieux',
  sup: 'Fournisseurs',
  man: 'Fabricants',
  eqmod: 'Modèles d\'équipement',
  export: 'Export',
  menu: 'Menu',
  dash: 'Dashboard'
}

const moduleLabel = (module) => MODULE_LABELS[module] || module

const permActionLabel = (nomPermission) => {
  const action = nomPermission.split(':')[1] || nomPermission
  const labels = {
    viewList: 'Voir liste',
    viewDetail: 'Voir détail',
    create: 'Créer',
    edit: 'Modifier',
    editAll: 'Modifier tout',
    editCreated: 'Modifier les siens',
    editAssigned: 'Modifier assignés',
    delete: 'Supprimer',
    export: 'Exporter',
    accept: 'Accepter',
    refuse: 'Refuser',
    transform: 'Transformer',
    start: 'Démarrer',
    end: 'Clôturer',
    refuseClosure: 'Refuser clôture',
    acceptClosure: 'Accepter clôture',
    acceptConsumableRequest: 'Valider consommable',
    view: 'Voir',
    disable: 'Désactiver',
    enable: 'Activer',
  }
  return labels[action] || action
}

// ==================== SÉLECTION ====================
const isModuleFullySelected = (perms) =>
  perms.every(p => selectedIds.value.includes(p.id))

const isModulePartiallySelected = (perms) => {
  const count = perms.filter(p => selectedIds.value.includes(p.id)).length
  return count > 0 && count < perms.length
}

const toggleModule = (perms, value) => {
  const ids = perms.map(p => p.id)
  const current = new Set(selectedIds.value)
  if (value) {
    ids.forEach(id => current.add(id))
  } else {
    ids.forEach(id => current.delete(id))
  }
  selectedIds.value = [...current]
}

const togglePermission = (id, value) => {
  if (value) {
    if (!selectedIds.value.includes(id)) selectedIds.value.push(id)
  } else {
    selectedIds.value = selectedIds.value.filter(x => x !== id)
  }
}

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