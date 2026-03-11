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
         <!-- Permissions groupées par module -->
<div v-for="(perms, module) in filteredPermissionsByModule" :key="module" class="mb-2">
  <v-expansion-panels variant="accordion">
    <v-expansion-panel>
      <v-expansion-panel-title>
        <div class="d-flex align-center" style="gap: 12px;">
          <v-checkbox
            :model-value="isModuleFullySelected(perms)"
            :indeterminate="isModulePartiallySelected(perms)"
            density="compact"
            hide-details
            color="primary"
            @update:model-value="toggleModule(perms, $event)"
            @click.stop
          />
          <span class="font-weight-medium">{{ moduleLabel(module) }}</span>
          <v-chip size="x-small" color="primary" variant="tonal">
            {{ perms.filter(p => selectedIds.includes(p.id)).length }}/{{ perms.length }}
          </v-chip>
        </div>
      </v-expansion-panel-title>
      <v-expansion-panel-text>
        <div class="d-flex flex-column" style="gap: 4px;">
          <div v-for="perm in perms" :key="perm.id" class="d-flex align-center">
            <v-checkbox
              :model-value="selectedIds.includes(perm.id)"
              :label="permActionLabel(perm.nomPermission)"
              density="compact"
              hide-details
              color="primary"
              @update:model-value="togglePermission(perm.id, $event)"
            />
          </div>
        </div>
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</div>

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
    console.log('userRes:', JSON.stringify(userRes)) 
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
    // if (perm.nomPermission.startsWith('dash:display')) continue
    if (perm.nomPermission === 'export:view') continue
    if (perm.nomPermission.endsWith(':export')) continue  
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
  const FULL_LABELS = {
    // Demandes d'intervention
    'di:viewList': 'Voir la liste des DI',
    'di:viewDetail': "Voir le détail d\'une DI",
    'di:create': 'Créer une DI',
    'di:editCreated': 'Modifier ses propres DI',
    'di:editAll': 'Modifier toutes les DI',
    'di:delete': 'Supprimer une DI',
    'di:accept': 'Accepter une DI',
    'di:refuse': 'Refuser une DI',
    'di:transform': 'Transformer une DI en BT',
    // Bons de travail
    'bt:viewList': 'Voir la liste des BT',
    'bt:viewDetail': "Voir le détail d\'un BT",
    'bt:create': 'Créer un BT',
    'bt:editAll': 'Modifier tous les BT',
    'bt:editAssigned': 'Modifier ses BT assignés',
    'bt:delete': 'Supprimer un BT',
    'bt:start': 'Démarrer un BT',
    'bt:end': 'Clôturer un BT',
    'bt:refuse': 'Refuser un BT',
    'bt:refuseClosure': 'Refuser la clôture d\'un BT',
    'bt:acceptClosure': 'Accepter la clôture d\'un BT',
    'bt:acceptConsumableRequest': 'Valider une demande de consommable',
    // Équipements
    'eq:viewList': 'Voir la liste des équipements',
    'eq:viewDetail': "Voir le détail d\'un équipement",
    'eq:create': 'Créer un équipement',
    'eq:edit': 'Modifier un équipement',
    'eq:delete': 'Supprimer un équipement',
    // Compteurs
    'cp:viewList': 'Voir la liste des compteurs',
    'cp:viewDetail': "Voir le détail d\'un compteur",
    'cp:create': 'Créer un compteur',
    'cp:edit': 'Modifier un compteur',
    'cp:delete': 'Supprimer un compteur',
    // Maintenances préventives
    'mp:viewList': 'Voir la liste des maintenances préventives',
    'mp:viewDetail': 'Voir le détail d\'une maintenance préventive',
    'mp:create': 'Créer une maintenance préventive',
    'mp:edit': 'Modifier une maintenance préventive',
    'mp:delete': 'Supprimer une maintenance préventive',
    // Stocks
    'stock:view': 'Voir les stocks',
    // Consommables
    'cons:viewDetail': "Voir le détail d\'un consommable",
    'cons:create': 'Créer un consommable',
    'cons:edit': 'Modifier un consommable',
    'cons:delete': 'Supprimer un consommable',
    // Magasins
    'mag:viewList': 'Voir la liste des magasins',
    'mag:viewDetail': "Voir le détail d\'un magasin",
    'mag:create': 'Créer un magasin',
    'mag:edit': 'Modifier un magasin',
    'mag:delete': 'Supprimer un magasin',
    // Utilisateurs
    'user:viewList': 'Voir la liste des utilisateurs',
    'user:viewDetail': "Voir le détail d\'un utilisateur",
    'user:create': 'Créer un utilisateur',
    'user:edit': 'Modifier un utilisateur',
    'user:disable': 'Désactiver un utilisateur',
    'user:enable': 'Activer un utilisateur',
    'user:delete': 'Supprimer un utilisateur',
    // Rôles
    'role:viewList': 'Voir la liste des rôles',
    'role:viewDetail': "Voir le détail d\'un rôle",
    'role:create': 'Créer un rôle',
    'role:edit': 'Modifier un rôle',
    'role:delete': 'Supprimer un rôle',
    // Lieux
    'loc:viewList': 'Voir la liste des lieux',
    'loc:viewDetail': "Voir le détail d\'un lieu",
    'loc:create': 'Créer un lieu',
    'loc:edit': 'Modifier un lieu',
    'loc:delete': 'Supprimer un lieu',
    // Fournisseurs
    'sup:viewList': 'Voir la liste des fournisseurs',
    'sup:viewDetail': "Voir le détail d\'un fournisseur",
    'sup:create': 'Créer un fournisseur',
    'sup:edit': 'Modifier un fournisseur',
    'sup:delete': 'Supprimer un fournisseur',
    // Fabricants
    'man:viewList': 'Voir la liste des fabricants',
    'man:viewDetail': "Voir le détail d\'un fabricant",
    'man:create': 'Créer un fabricant',
    'man:edit': 'Modifier un fabricant',
    'man:delete': 'Supprimer un fabricant',
    // Modèles d'équipement
    'eqmod:viewList': 'Voir la liste des modèles d\'équipement',
    'eqmod:viewDetail': "Voir le détail d\'un modèle d\'équipement",
    'eqmod:create': 'Créer un modèle d\'équipement',
    'eqmod:edit': 'Modifier un modèle d\'équipement',
    'eqmod:delete': 'Supprimer un modèle d\'équipement',
    // Menu
    'menu:view': 'Accéder au menu de navigation',
    // Dashboard
    'dash:display.bt': 'Afficher les BT sur le dashboard',
    'dash:display.btAssigned': 'Afficher ses BT assignés sur le dashboard',
    'dash:display.di': 'Afficher les DI sur le dashboard',
    'dash:display.diCreated': 'Afficher ses DI créées sur le dashboard',
    'dash:display.eq': 'Afficher les équipements sur le dashboard',
    'dash:display.mag': 'Afficher les magasins sur le dashboard',
    'dash:display.vertical': 'Afficher le dashboard en mode vertical',
    'dash:stats.bt': 'Voir les statistiques de ses BT',
    'dash:stats.di': 'Voir les statistiques de ses DI',
    'dash:stats.full': 'Voir toutes les statistiques',
  }
  return FULL_LABELS[nomPermission] || nomPermission
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