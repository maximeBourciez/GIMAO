<template>
  <v-sheet class="pa-4 mb-4" elevation="2" rounded>
    <!-- Message d'erreur -->
    <v-alert v-if="localError" type="error" dismissible @click:close="localError = ''" class="mb-4">
      {{ localError }}
    </v-alert>

    <h3 class="mb-4">
      {{ isEditMode ? 'Modifier le compteur' : 'Ajouter un compteur' }}
    </h3>

    <!-- Informations générales -->
    <v-sheet class="pa-4 mb-4" elevation="1" rounded>
      <h4 class="mb-3">Informations générales</h4>

      <v-row dense>
        <v-col cols="12" md="6">
          <v-text-field v-model="counter.nom" label="Nom du compteur *" outlined dense
            :error="!counter.nom?.trim()" />
        </v-col>

        <v-col cols="12" md="6">
          <v-text-field v-model="counter.description" label="Description (optionnel)" outlined dense />
        </v-col>
      </v-row>

      <v-row dense>
        <v-col cols="6">
          <v-text-field v-model="counter.intervalle" type="number" label="Intervalle *" outlined dense
            :error="!counter.intervalle || counter.intervalle <= 0" />
        </v-col>

        <v-col cols="6">
          <v-text-field v-model="counter.unite" label="Unité *" outlined dense :error="!counter.unite?.trim()" />
        </v-col>
      </v-row>
    </v-sheet>

    <!-- Options -->
    <v-sheet class="pa-4 mb-4" elevation="1" rounded>
      <h4 class="mb-3">Options du compteur</h4>

      <v-row dense>
        <v-col cols="6">
          <v-text-field v-model.number="counter.valeurCourante" label="Valeur actuelle" type="number" outlined
            dense />
        </v-col>

        <v-col cols="6">
          <v-text-field v-model="counter.derniereIntervention" label="Dernière intervention" outlined dense />
        </v-col>
      </v-row>

      <v-row dense justify="space-around">
        <v-checkbox v-model="counter.estGlissant" label="Compteur glissant" dense />
        <v-checkbox v-model="counter.estPrincipal" label="Compteur principal" dense />
      </v-row>

      <v-row dense>
        <v-col>
          <p class="mb-2">La maintenance nécessite :</p>
          <v-row justify="space-around" dense>
            <v-checkbox v-model="counter.habElec" label="Habilitation électrique" dense />
            <v-checkbox v-model="counter.permisFeu" label="Permis feu" dense />
          </v-row>
        </v-col>
      </v-row>
    </v-sheet>

    <!-- Plan de maintenance -->
    <v-sheet class="pa-4 mb-4" elevation="1" rounded>
      <h4 class="mb-3">Plan de maintenance associé</h4>
      <v-col cols="12" v-if="existingPMs.length > 0">
        <v-select v-model="counter.planMaintenance.nom" :items="existingPMs" item-title="nom"
          item-value="nom" label="Plan existant" outlined dense clearable @update:model-value="applyExistingPM" />
      </v-col>
      <v-row>
        <v-col cols="8">
          <v-text-field v-model="counter.planMaintenance.nom" label="Nom du plan de maintenance"
            outlined dense />
        </v-col>
        <v-col cols="4">
          <v-select v-model="counter.planMaintenance.type" :items="typesPM" item-title="libelle"
            item-value="id" label="Type" outlined dense />
        </v-col>
      </v-row>
    </v-sheet>

    <!-- Consommables -->
    <v-sheet class="pa-4 mb-4" elevation="1" rounded>
      <h4 class="mb-3">Consommables</h4>

      <v-row v-for="(c, index) in counter.planMaintenance.consommables" :key="index" dense
        class="mb-3">
        <v-col cols="6">
          <v-select v-model="c.consommable" :items="consumables" item-title="designation"
            item-value="id" label="Consommable" outlined dense />
        </v-col>

        <v-col cols="3">
          <v-text-field v-model.number="c.quantite" type="number" min="1" label="Quantité" outlined
            dense />
        </v-col>

        <v-col cols="3" class="d-flex align-center">
          <v-btn icon color="red" @click="removePMConsumable(index)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-col>
      </v-row>

      <v-btn color="primary" @click="addPMConsumable">
        Ajouter un consommable
      </v-btn>
    </v-sheet>

    <!-- Documents -->
    <v-sheet class="pa-4 mb-4" elevation="1" rounded>
      <h4 class="mb-3">Documents</h4>

      <v-row v-for="(doc, index) in counter.planMaintenance.documents" :key="index" dense
        class="mb-3">
        <v-col cols="4">
          <v-text-field v-model="doc.titre" label="Titre" outlined dense />
        </v-col>

        <v-col cols="5">
          <v-file-input v-model="doc.file" dense outlined show-size clearable label="Document">
            <template #selection>
              <span v-if="doc.file">
                {{ doc.file.name }}
              </span>
              <span v-else-if="doc.path">
                {{ getFileName(doc.path) }}
              </span>
              <span v-else>
                Aucun fichier sélectionné
              </span>
            </template>
          </v-file-input>
        </v-col>

        <v-col cols="2">
          <v-select v-model="doc.type" :items="typesDocuments" item-title="nomTypeDocument"
            item-value="id" label="Type" outlined dense />
        </v-col>

        <v-col cols="1" class="d-flex align-center">
          <v-btn icon color="red" @click="removePMDocument(index)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-col>
      </v-row>

      <v-btn color="primary" @click="addPMDocument">
        Ajouter un document
      </v-btn>
    </v-sheet>

    <!-- Actions du formulaire -->
    <v-row class="mt-4" justify="end">
      <v-btn v-if="!isFirstCounter" variant="text" @click="handleCancel">
        Annuler
      </v-btn>
      <v-btn color="primary" class="ml-2" @click="handleSave">
        {{ isEditMode ? 'Modifier le compteur' : 'Ajouter le compteur' }}
      </v-btn>
    </v-row>
  </v-sheet>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  existingPMs: {
    type: Array,
    default: () => []
  },
  typesPM: {
    type: Array,
    default: () => []
  },
  consumables: {
    type: Array,
    default: () => []
  },
  typesDocuments: {
    type: Array,
    default: () => []
  },
  isEditMode: {
    type: Boolean,
    default: false
  },
  isFirstCounter: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'save', 'cancel'])

const localError = ref('')

const counter = computed({
  get: () => props.modelValue,
  set: v => emit('update:modelValue', v)
})

const addPMConsumable = () => {
  counter.value.planMaintenance.consommables.push({ consommable: null, quantite: 1 })
}

const removePMConsumable = (i) => {
  counter.value.planMaintenance.consommables.splice(i, 1)
}

const addPMDocument = () => {
  counter.value.planMaintenance.documents.push({ titre: '', file: null, type: null })
}

const removePMDocument = (i) => {
  counter.value.planMaintenance.documents.splice(i, 1)
}

const applyExistingPM = (nom) => {
  const pm = props.existingPMs.find(p => p.nom === nom)
  if (!pm) return

  counter.value.planMaintenance = {
    nom: pm.nom,
    type: pm.type ?? null,
    consommables: pm.consommables ? JSON.parse(JSON.stringify(pm.consommables)) : [],
    documents: pm.documents ? [...pm.documents] : []
  }
}

const handleSave = () => {
  // Validation
  localError.value = ''

  if (!counter.value.nom?.trim()) {
    localError.value = 'Le nom du compteur est requis'
    return
  }

  if (!counter.value.intervalle || counter.value.intervalle <= 0) {
    localError.value = 'L\'intervalle doit être supérieur à 0'
    return
  }

  if (!counter.value.unite?.trim()) {
    localError.value = 'L\'unité est requise'
    return
  }

  // Si tout est valide, émettre l'événement save
  emit('save')
}

const handleCancel = () => {
  localError.value = ''
  emit('cancel')
}

const getFileName = (path) => {
  return path?.split('/').pop() || ''
}
</script>

<style scoped>
/* Styles spécifiques si nécessaire */
</style>
