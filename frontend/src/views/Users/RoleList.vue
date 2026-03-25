<template>
  <v-app>
    <v-main>
      <v-container>

        <!-- En-tête -->
        <div class="d-flex align-center justify-space-between mb-4">
          <h2 class="text-h5 font-weight-bold">Gestion des rôles</h2>
          <v-btn color="primary" prepend-icon="mdi-plus" @click="openCreateDialog">
            Nouveau rôle
          </v-btn>
        </div>

        <!-- Chargement -->
        <v-alert v-if="loading" type="info" variant="tonal" class="mb-4">
          <v-progress-circular indeterminate size="20" class="mr-2" />
          Chargement...
        </v-alert>

        <!-- Erreur -->
        <v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-4" closable
          @click:close="errorMessage = ''">
          {{ errorMessage }}
        </v-alert>

        <!-- Succès -->
        <v-alert v-if="successMessage" type="success" variant="tonal" class="mb-4" closable
          @click:close="successMessage = ''">
          {{ successMessage }}
        </v-alert>

        <!-- Liste des rôles -->
        <v-row>
          <v-col v-for="role in roles" :key="role.id" cols="12" md="6" lg="6">
            <v-card elevation="2" rounded height="220">
              <v-card-title class="pt-3 pb-1">
                <span class="text-body-1 font-weight-bold">{{ role.nomRole }}</span>
              </v-card-title>

              <v-card-text class="pb-1">
                <p class="text-body-2 text-medium-emphasis mb-2">
                  {{ role.permissions?.length || 0 }} permission(s)
                </p>
                <div class="d-flex flex-wrap" style="gap: 6px; max-height: 60px; overflow: hidden;">
                  <v-chip v-for="module in getModules(role.permissions)" :key="module" size="small" variant="outlined"
                    color="secondary">
                    {{ module }}
                  </v-chip>
                </div>
                <span v-if="getModules(role.permissions).length > 1" class="text-caption text-primary"
                  style="cursor: pointer;" @click="openEditDialog(role)">
                  voir plus
                </span>
              </v-card-text>

              <v-card-actions class="mt-auto">
                <v-spacer />
                <v-btn size="small" variant="text" color="primary" prepend-icon="mdi-pencil"
                  @click="openEditDialog(role)">
                  Modifier
                </v-btn>
                <v-btn size="small" variant="text" color="secondary" prepend-icon="mdi-content-copy"
                  @click="dupliquerRole(role)">
                  Dupliquer
                </v-btn>
                <v-btn v-if="!estRoleSysteme(role.nomRole)" size="small" variant="text" color="error"
                  prepend-icon="mdi-delete" @click="confirmDelete(role)">
                  Supprimer
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <!-- État vide -->
        <v-sheet v-if="!loading && roles.length === 0" class="pa-8 text-center" elevation="1" rounded>
          <v-icon size="48" color="grey">mdi-shield-off-outline</v-icon>
          <p class="text-body-1 text-medium-emphasis mt-2">Aucun rôle trouvé.</p>
        </v-sheet>

      </v-container>
    </v-main>

    <!-- ===================== DIALOG CRÉATION / ÉDITION ===================== -->
    <v-dialog v-model="dialog" max-width="800" persistent>
      <v-card>
        <v-card-title class="pa-4 pb-2">
          {{ isEdit ? 'Modifier le rôle' : 'Créer un rôle' }}
        </v-card-title>

        <v-divider />

        <v-card-text class="pa-4">

          <!-- Nom et rang -->
          <v-sheet class="pa-4 mb-4" elevation="1" rounded>
            <h4 class="mb-3">Informations</h4>
            <v-row dense>
              <v-col cols="12" md="8">
                <v-text-field v-model="form.nomRole" label="Nom du rôle" placeholder="Technicien, Responsable..."
                  variant="outlined" density="comfortable" :error-messages="formErrors.nomRole" />
              </v-col>
            </v-row>
          </v-sheet>

          <!-- Permissions -->
          <v-sheet class="pa-4" elevation="1" rounded>
            <div class="d-flex align-center justify-space-between mb-3">
              <h4>Permissions</h4>
              <span class="text-body-2 text-medium-emphasis">
                {{ form.permissions_ids.length }} sélectionnée(s)
              </span>
            </div>

            <!-- Filtre par module -->
            <v-text-field v-model="searchPerm" placeholder="Rechercher une permission..."
              prepend-inner-icon="mdi-magnify" variant="outlined" density="compact" clearable class="mb-3" />


            <div v-for="(types, module) in filteredPermissionsByModule" :key="module" class="mb-2">
              <v-expansion-panels variant="accordion">
                <v-expansion-panel>
                  <v-expansion-panel-title>
                    <div class="d-flex align-center" style="gap: 12px;">
                      <v-checkbox :model-value="isModuleFullySelected([...types.affichage, ...types.action])"
                        :indeterminate="isModulePartiallySelected([...types.affichage, ...types.action])"
                        density="compact" hide-details color="primary"
                        @update:model-value="toggleModule([...types.affichage, ...types.action], $event)"
                        @click.stop />
                      <span class="font-weight-medium">{{ types.nom }}</span>
                      <v-chip size="x-small" color="primary" variant="tonal">
                        {{[...types.affichage, ...types.action].filter(p => form.permissions_ids.includes(p.id)).length
                        }}/{{ types.affichage.length + types.action.length }}
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
                        <v-checkbox :model-value="form.permissions_ids.includes(perm.id)"
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
                        <v-checkbox :model-value="form.permissions_ids.includes(perm.id)"
                          :label="perm.description" density="compact" hide-details color="orange"
                          :disabled="isPermDisabledByHierarchy(perm.nomPermission)"
                          @update:model-value="togglePermission(perm.id, $event)" />
                      </div>
                    </div>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </div>

            <p v-if="Object.keys(filteredPermissionsByModule).length === 0" class="text-body-2 text-medium-emphasis">
              Aucune permission trouvée.
            </p>
          </v-sheet>

          <!-- Erreur formulaire -->
          <v-alert v-if="dialogError" type="error" variant="tonal" class="mt-3">
            {{ dialogError }}
          </v-alert>

        </v-card-text>

        <v-divider />

        <v-card-actions class="pa-4">
          <v-spacer />
          <v-btn variant="text" @click="closeDialog">Annuler</v-btn>
          <v-btn v-if="isEdit" color="secondary" variant="outlined" :loading="saving"
            prepend-icon="mdi-content-save-plus" @click="saveAsNewRole">
            Enregistrer comme nouveau rôle
          </v-btn>
          <v-btn color="primary" :loading="saving" @click="saveRole">
            {{ isEdit ? 'Enregistrer' : 'Créer' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ===================== DIALOG SUPPRESSION ===================== -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Supprimer le rôle</v-card-title>
        <v-card-text>
          Voulez-vous vraiment supprimer le rôle <strong>{{ roleToDelete?.nomRole }}</strong> ?
          Cette action est irréversible.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialog = false">Annuler</v-btn>
          <v-btn color="error" :loading="deleting" @click="deleteRole">Supprimer</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import { API_BASE_URL } from '@/utils/constants'
import { usePermissionSelector } from '@/composables/usePermissionSelector'

const api = useApi(API_BASE_URL)

// ==================== ÉTAT ====================
const roles = ref([])
const allPermissions = ref([])
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Dialog création/édition
const dialog = ref(false)
const isEdit = ref(false)
const saving = ref(false)
const dialogError = ref('')
const searchPerm = ref('')
const editingRoleId = ref(null)

const form = ref({
  nomRole: '',
  permissions_ids: []
})

const formErrors = ref({
  nomRole: '',
})

// Dialog suppression
const deleteDialog = ref(false)
const deleting = ref(false)
const roleToDelete = ref(null)

// Adaptateur pour passer form.permissions_ids au composable comme un ref
const selectedIds = computed({
  get: () => form.value.permissions_ids,
  set: (val) => { form.value.permissions_ids = val }
})

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
  try {
    const [rolesRes, permsRes] = await Promise.all([
      api.get('roles/'),
      api.get('permissions/')
    ])
    roles.value = Array.isArray(rolesRes) ? rolesRes : []
    allPermissions.value = Array.isArray(permsRes) ? permsRes : []
  } catch (e) {
    errorMessage.value = 'Erreur lors du chargement des données.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)

// ==================== MODULES (affichage cartes) ====================

// Retourne les modules uniques d'une liste de permissions
const getModules = (permissions) => {
  if (!permissions) return []
  return [...new Set(permissions.map(p => p.module?.code ?? p.nomPermission.split(':')[0]))]
}

// ==================== DIALOG ====================
const resetForm = () => {
  form.value = { nomRole: '', permissions_ids: [] }
  formErrors.value = { nomRole: '' }
  dialogError.value = ''
  searchPerm.value = ''
}

const openCreateDialog = () => {
  resetForm()
  isEdit.value = false
  editingRoleId.value = null
  dialog.value = true
}

const openEditDialog = (role) => {
  resetForm()
  isEdit.value = true
  editingRoleId.value = role.id
  form.value = {
    nomRole: role.nomRole,
    permissions_ids: (role.permissions || []).map(p => p.id)
  }

  applyHierarchy()

  dialog.value = true
}

const closeDialog = () => {
  dialog.value = false
  resetForm()
}

// ==================== SAUVEGARDE ====================
const validateForm = () => {
  let valid = true
  formErrors.value = { nomRole: '' }

  if (!form.value.nomRole.trim()) {
    formErrors.value.nomRole = 'Le nom du rôle est requis.'
    valid = false
  }
  return valid
}

const saveRole = async () => {
  if (!validateForm()) return

  saving.value = true
  dialogError.value = ''

  try {
    const payload = {
      nomRole: form.value.nomRole.trim(),
      rang: form.value.rang,
      permissions_ids: form.value.permissions_ids
    }

    if (isEdit.value) {
      await api.put(`roles/${editingRoleId.value}/`, payload)
      successMessage.value = 'Rôle modifié avec succès.'
      setTimeout(() => { successMessage.value = '' }, 4000)

    } else {
      await api.post('roles/', payload)
      successMessage.value = 'Rôle créé avec succès.'
      setTimeout(() => { successMessage.value = '' }, 4000)

    }

    closeDialog()
    await fetchData()
  } catch (e) {
    dialogError.value = isEdit.value
      ? 'Erreur lors de la modification du rôle.'
      : 'Erreur lors de la création du rôle.'
  } finally {
    saving.value = false
  }
}

// ==================== SUPPRESSION ====================
const saveAsNewRole = async () => {
  if (!validateForm()) return
  saving.value = true
  dialogError.value = ''
  try {
    const nouveauNom = prompt('Nom du nouveau rôle :', `Copie de ${form.value.nomRole}`)
    if (!nouveauNom || !nouveauNom.trim()) {
      saving.value = false
      return
    }
    const payload = {
      nomRole: nouveauNom.trim(),
      permissions_ids: form.value.permissions_ids
    }
    await api.post('roles/', payload)
    successMessage.value = `Rôle "${nouveauNom}" créé avec succès.`
    setTimeout(() => { successMessage.value = '' }, 4000)
    closeDialog()
    await fetchData()
  } catch (e) {
    dialogError.value = 'Erreur lors de la création du nouveau rôle.'
  } finally {
    saving.value = false
  }
}

const confirmDelete = (role) => {
  roleToDelete.value = role
  deleteDialog.value = true
}

const ROLES_SYSTEME = ['Opérateur', 'Magasinier', 'Technicien', 'Responsable GMAO']

const estRoleSysteme = (nomRole) => ROLES_SYSTEME.includes(nomRole)

const deleteRole = async () => {
  if (!roleToDelete.value) return

  deleting.value = true
  try {
    await api.remove(`roles/${roleToDelete.value.id}/`)
    successMessage.value = `Rôle "${roleToDelete.value.nomRole}" supprimé.`
    setTimeout(() => { successMessage.value = '' }, 4000)
    deleteDialog.value = false
    await fetchData()
  } catch (e) {
    errorMessage.value = 'Erreur lors de la suppression. Le rôle est peut-être utilisé par des utilisateurs.'
    deleteDialog.value = false
  } finally {
    deleting.value = false
  }
}

const dupliquerRole = async (role) => {
  try {
    const nouveau = await api.post(`roles/${role.id}/dupliquer/`, {
      nomRole: `Copie de ${role.nomRole}`
    })
    successMessage.value = `Rôle "${nouveau.nomRole}" créé avec succès.`
    setTimeout(() => { successMessage.value = '' }, 4000)
    await fetchData()
  } catch (e) {
    errorMessage.value = 'Erreur lors de la duplication du rôle.'
  }
}

</script>
