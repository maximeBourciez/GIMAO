import { computed } from 'vue'

export const PERM_HIERARCHY = {
  'di:editAll': ['di:editCreated'],
  'bt:editAll': ['bt:editAssigned'],
  'dash:stats.full': ['dash:stats.bt', 'dash:stats.di'],
  'dash:display.bt': ['dash:display.btAssigned'],
  'dash:display.di': ['dash:display.diCreated'],
}

const PERM_TYPE = {
  viewList: 'affichage', viewDetail: 'affichage', view: 'affichage',
  'display.bt': 'affichage', 'display.di': 'affichage', 'display.eq': 'affichage',
  'display.mag': 'affichage', 'display.vertical': 'affichage',
  'display.btAssigned': 'affichage', 'display.diCreated': 'affichage',
  'stats.full': 'affichage', 'stats.bt': 'affichage', 'stats.di': 'affichage',
  create: 'action', edit: 'action', editAll: 'action', editCreated: 'action',
  editAssigned: 'action', delete: 'action', accept: 'action', refuse: 'action',
  transform: 'action', start: 'action', end: 'action', refuseClosure: 'action',
  acceptClosure: 'action', acceptConsumableRequest: 'action',
  disable: 'action', enable: 'action', dataManagement: 'affichage',
}

/**
 * Composable partagé pour la sélection de permissions.
 *
 * @param {Ref<Array>} allPermissions - Ref vers la liste complète des permissions
 * @param {Ref<Array>} selectedIds    - Ref vers le tableau des IDs sélectionnés (modifiable)
 * @param {Ref<string>} searchPerm    - Ref vers la chaîne de recherche
 */
export function usePermissionSelector(allPermissions, selectedIds, searchPerm) {
  const getPermType = (nomPermission) => {
    const action = nomPermission.split(':')[1] || nomPermission
    return PERM_TYPE[action] || 'action'
  }

  const isPermDisabledByHierarchy = (nomPermission) => {
    for (const [parent, children] of Object.entries(PERM_HIERARCHY)) {
      if (children.includes(nomPermission)) {
        const parentPerm = allPermissions.value.find(p => p.nomPermission === parent)
        if (parentPerm && selectedIds.value.includes(parentPerm.id)) {
          return true
        }
      }
    }
    return false
  }

  // Permissions groupées par module, en excluant les permissions d'export
  const permissionsByModule = computed(() => {
    const groups = {}
    for (const perm of allPermissions.value) {
      if (perm.nomPermission === 'export:view') continue
      if (perm.nomPermission.endsWith(':export')) continue
      const code = perm.module?.code ?? perm.nomPermission.split(':')[0]
      const nom = perm.module?.nom ?? code
      if (!groups[code]) groups[code] = { nom, affichage: [], action: [] }
      groups[code][getPermType(perm.nomPermission)].push(perm)
    }
    return groups
  })

  // Permissions filtrées par la recherche
  const filteredPermissionsByModule = computed(() => {
    if (!searchPerm.value) return permissionsByModule.value
    const search = searchPerm.value.toLowerCase()
    const result = {}
    for (const [code, data] of Object.entries(permissionsByModule.value)) {
      const filteredAffichage = data.affichage.filter(p => p.nomPermission.toLowerCase().includes(search))
      const filteredAction = data.action.filter(p => p.nomPermission.toLowerCase().includes(search))
      if (filteredAffichage.length || filteredAction.length) {
        result[code] = { ...data, affichage: filteredAffichage, action: filteredAction }
      }
    }
    return result
  })

  const isModuleFullySelected = (perms) => perms.every(p => selectedIds.value.includes(p.id))

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
    const perm = allPermissions.value.find(p => p.id === id)
    if (!perm) return

    if (value) {
      if (!selectedIds.value.includes(id)) selectedIds.value.push(id)
      if (PERM_HIERARCHY[perm.nomPermission]) {
        for (const childName of PERM_HIERARCHY[perm.nomPermission]) {
          const childPerm = allPermissions.value.find(p => p.nomPermission === childName)
          if (childPerm && !selectedIds.value.includes(childPerm.id)) {
            selectedIds.value.push(childPerm.id)
          }
        }
      }
    } else {
      selectedIds.value = selectedIds.value.filter(x => x !== id)
      if (PERM_HIERARCHY[perm.nomPermission]) {
        for (const childName of PERM_HIERARCHY[perm.nomPermission]) {
          const childPerm = allPermissions.value.find(p => p.nomPermission === childName)
          if (childPerm) {
            selectedIds.value = selectedIds.value.filter(x => x !== childPerm.id)
          }
        }
      }
    }
  }

  // Applique la hiérarchie sur les IDs sélectionnés (à appeler après chargement)
  const applyHierarchy = () => {
    for (const [parent, children] of Object.entries(PERM_HIERARCHY)) {
      const parentPerm = allPermissions.value.find(p => p.nomPermission === parent)
      if (parentPerm && selectedIds.value.includes(parentPerm.id)) {
        for (const childName of children) {
          const childPerm = allPermissions.value.find(p => p.nomPermission === childName)
          if (childPerm && !selectedIds.value.includes(childPerm.id)) {
            selectedIds.value.push(childPerm.id)
          }
        }
      }
    }
  }

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
