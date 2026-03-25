import { computed } from 'vue'

/**
 * Composable partagé pour la sélection de permissions.
 *
 * @param {Ref<Array>} allPermissions - Ref vers la liste complète des permissions
 * @param {Ref<Array>} selectedIds    - Ref vers le tableau des IDs sélectionnés (modifiable)
 * @param {Ref<string>} searchPerm    - Ref vers la chaîne de recherche
 *
 * Chaque permission expose depuis l'API : { id, nomPermission, description, type, parent_id, module }
 * - type      : 'affichage' | 'action'
 * - parent_id : id de la permission parente (ou null)
 */
export function usePermissionSelector(allPermissions, selectedIds, searchPerm) {

  // Une permission d'action est désactivée si sa permission parente est déjà cochée
  const isPermDisabledByHierarchy = (permId) => {
    const perm = allPermissions.value.find(p => p.id === permId)
    if (!perm?.parent_id) return false
    return selectedIds.value.includes(perm.parent_id)
  }

  // Réordonne un tableau de permissions : parent d'abord, puis ses enfants juste après.
  // Chaque élément retourné est une copie avec _isChild ajouté.
  function orderedWithChildren(perms) {
    const idsInGroup = new Set(perms.map(p => p.id))
    const result = []
    const added = new Set()
    for (const perm of perms) {
      if (added.has(perm.id)) continue
      const isRoot = !perm.parent_id || !idsInGroup.has(perm.parent_id)
      if (isRoot) {
        result.push({ ...perm, _isChild: false })
        added.add(perm.id)
        for (const child of perms) {
          if (child.parent_id === perm.id && !added.has(child.id)) {
            result.push({ ...child, _isChild: true })
            added.add(child.id)
          }
        }
      }
    }
    return result
  }

  // Permissions groupées par module
  const permissionsByModule = computed(() => {
    const groups = {}
    for (const perm of allPermissions.value) {
      const code = perm.module?.code ?? perm.nomPermission.split(':')[0]
      const nom = perm.module?.nom ?? code
      if (!groups[code]) groups[code] = { nom, affichage: [], action: [] }
      groups[code][perm.type ?? 'action'].push(perm)
    }
    // Réordonner pour placer les enfants juste après leur parent
    for (const code of Object.keys(groups)) {
      groups[code].affichage = orderedWithChildren(groups[code].affichage)
      groups[code].action = orderedWithChildren(groups[code].action)
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
      let newIds = selectedIds.value.includes(id) ? selectedIds.value : [...selectedIds.value, id]
      // Activer aussi les enfants dont c'est la permission parente
      for (const child of allPermissions.value) {
        if (child.parent_id === id && !newIds.includes(child.id)) {
          newIds = [...newIds, child.id]
        }
      }
      selectedIds.value = newIds
    } else {
      // Désactiver la permission et ses enfants
      const childIds = allPermissions.value
        .filter(p => p.parent_id === id)
        .map(p => p.id)
      selectedIds.value = selectedIds.value.filter(x => x !== id && !childIds.includes(x))
    }
  }

  // Applique la hiérarchie sur les IDs sélectionnés (à appeler après chargement)
  const applyHierarchy = () => {
    let ids = [...selectedIds.value]
    for (const perm of allPermissions.value) {
      if (ids.includes(perm.id)) {
        for (const child of allPermissions.value) {
          if (child.parent_id === perm.id && !ids.includes(child.id)) {
            ids = [...ids, child.id]
          }
        }
      }
    }
    selectedIds.value = ids
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
