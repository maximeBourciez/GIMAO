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
 * - parent_id : id de la permission requise (ex. di:archive.parent = di:viewDetail)
 *
 * Règle de parenté :
 *   Cocher une permission coche aussi tous ses ancêtres (remontée de chaîne).
 *   Décocher une permission décoche aussi toutes les permissions qui en dépendent.
 *   Une permission est grisée si au moins une permission sélectionnée en dépend.
 */
export function usePermissionSelector(allPermissions, selectedIds, searchPerm) {

  // Remonte la chaîne des parents depuis un id et retourne tous les ids ancêtres
  function getAncestorIds(id) {
    const ancestors = []
    let perm = allPermissions.value.find(p => p.id === id)
    while (perm?.parent_id) {
      ancestors.push(perm.parent_id)
      perm = allPermissions.value.find(p => p.id === perm.parent_id)
    }
    return ancestors
  }

  // Collecte récursivement tous les ids qui dépendent de l'id donné (descendants)
  function getDescendantIds(id) {
    const result = []
    for (const p of allPermissions.value) {
      if (p.parent_id === id) {
        result.push(p.id)
        result.push(...getDescendantIds(p.id))
      }
    }
    return result
  }

  // Une permission est grisée si une permission sélectionnée en dépend (directement ou transitivement)
  const isPermDisabledByHierarchy = (permId) => {
    return allPermissions.value.some(p => {
      if (!selectedIds.value.includes(p.id) || p.id === permId) return false
      return getAncestorIds(p.id).includes(permId)
    })
  }

  // Réordonne : parents avant leurs enfants directs, avec _isChild ajouté
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
    for (const code of Object.keys(groups)) {
      groups[code].affichage = orderedWithChildren(groups[code].affichage)
      groups[code].action    = orderedWithChildren(groups[code].action)
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
    const current = new Set(selectedIds.value)
    if (value) {
      for (const perm of perms) {
        current.add(perm.id)
        // Cocher aussi tous les ancêtres requis
        for (const ancestorId of getAncestorIds(perm.id)) {
          current.add(ancestorId)
        }
      }
    } else {
      for (const perm of perms) {
        current.delete(perm.id)
        // Décocher aussi tout ce qui dépend de cette permission
        for (const descendantId of getDescendantIds(perm.id)) {
          current.delete(descendantId)
        }
      }
    }
    selectedIds.value = [...current]
  }

  const togglePermission = (id, value) => {
    const current = new Set(selectedIds.value)
    if (value) {
      current.add(id)
      // Remonter la chaîne : cocher tous les ancêtres requis
      for (const ancestorId of getAncestorIds(id)) {
        current.add(ancestorId)
      }
    } else {
      current.delete(id)
      // Décocher tout ce qui dépendait de cette permission
      for (const descendantId of getDescendantIds(id)) {
        current.delete(descendantId)
      }
    }
    selectedIds.value = [...current]
  }

  // À appeler après chargement : s'assure que tous les ancêtres requis sont cochés
  const applyHierarchy = () => {
    const current = new Set(selectedIds.value)
    for (const id of [...current]) {
      for (const ancestorId of getAncestorIds(id)) {
        current.add(ancestorId)
      }
    }
    selectedIds.value = [...current]
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
