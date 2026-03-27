import { computed } from 'vue'

/**
 * Paires d'exclusion mutuelle — aucun lien en base.
 * Cocher l'un grise et décoche l'autre.
 * Remarque : stats.bt et stats.di ne se grisent PAS entre eux,
 * mais chacun grise stats.full (et inversement).
 */
const EXCLUSIVE_PAIRS = [
  ['dash:display.bt',  'dash:display.btAssigned'],
  ['dash:display.di',  'dash:display.diCreated'],
  ['dash:stats.full',  'dash:stats.bt'],
  ['dash:stats.full',  'dash:stats.di'],
]

function getExclusiveGroupNoms(nomPermission) {
  return EXCLUSIVE_PAIRS
    .filter(pair => pair.includes(nomPermission))
    .map(pair => pair.find(n => n !== nomPermission))
}

/**
 * Composable partagé pour la sélection de permissions.
 *
 * @param {Ref<Array>} allPermissions - liste complète des permissions (id, nomPermission, description, type, module)
 * @param {Ref<Array>} selectedIds    - tableau des IDs sélectionnés (modifiable)
 * @param {Ref<string>} searchPerm    - chaîne de recherche
 */
export function usePermissionSelector(allPermissions, selectedIds, searchPerm) {

  // IDs des autres membres du groupe exclusif d'une permission
  function getExclusiveGroupIds(permId) {
    const perm = allPermissions.value.find(p => p.id === permId)
    if (!perm) return []
    return getExclusiveGroupNoms(perm.nomPermission)
      .map(nom => allPermissions.value.find(p => p.nomPermission === nom)?.id)
      .filter(Boolean)
  }

  // Une permission est grisée si un autre membre de son groupe exclusif est sélectionné
  const isPermDisabledByHierarchy = (permId) =>
    getExclusiveGroupIds(permId).some(otherId => selectedIds.value.includes(otherId))

  // Permissions groupées par module { code: { nom, affichage: [], action: [] } }
  const permissionsByModule = computed(() => {
    const groups = {}
    for (const perm of allPermissions.value) {
      const code = perm.module?.code ?? perm.nomPermission.split(':')[0]
      const nom  = perm.module?.nom  ?? code
      if (!groups[code]) groups[code] = { nom, affichage: [], action: [] }
      groups[code][perm.type ?? 'action'].push(perm)
    }
    return groups
  })

  // Permissions filtrées par la recherche
  const filteredPermissionsByModule = computed(() => {
    if (!searchPerm.value) return permissionsByModule.value
    const search = searchPerm.value.toLowerCase()
    const result = {}
    for (const [code, data] of Object.entries(permissionsByModule.value)) {
      const filteredAffichage = data.affichage.filter(p =>
        p.description?.toLowerCase().includes(search) || p.nomPermission.toLowerCase().includes(search)
      )
      const filteredAction = data.action.filter(p =>
        p.description?.toLowerCase().includes(search) || p.nomPermission.toLowerCase().includes(search)
      )
      if (filteredAffichage.length || filteredAction.length) {
        result[code] = { ...data, affichage: filteredAffichage, action: filteredAction }
      }
    }
    return result
  })

  const isModuleFullySelected = (perms) =>
    perms.every(p => selectedIds.value.includes(p.id))

  const isModulePartiallySelected = (perms) => {
    const count = perms.filter(p => selectedIds.value.includes(p.id)).length
    return count > 0 && count < perms.length
  }

  const toggleModule = (perms, value) => {
    const current = new Set(selectedIds.value)
    if (value) {
      for (const perm of perms) current.add(perm.id)
    } else {
      for (const perm of perms) current.delete(perm.id)
    }
    selectedIds.value = [...current]
  }

  const togglePermission = (id, value) => {
    const current = new Set(selectedIds.value)
    if (value) {
      current.add(id)
      // Exclusion mutuelle : décocher les autres membres du groupe
      for (const otherId of getExclusiveGroupIds(id)) current.delete(otherId)
    } else {
      current.delete(id)
    }
    selectedIds.value = [...current]
  }

  // Compatibilité : appelé depuis RoleList après chargement (no-op sans hiérarchie)
  const applyHierarchy = () => {}

  return {
    permissionsByModule,
    filteredPermissionsByModule,
    isPermDisabledByHierarchy,
    isModuleFullySelected,
    isModulePartiallySelected,
    toggleModule,
    togglePermission,
    applyHierarchy,
  }
}
