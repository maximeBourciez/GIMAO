<template>
  <v-container>
    <FabricantForm
      title="Créer un fabricant"
      submit-button-text="Créer le fabricant"
      @created="handleCreated"
      @close="handleClose"
    />
  </v-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import FabricantForm from '@/components/Forms/FabricantForm.vue'

const router = useRouter()

const handleCreated = (newFabricant) => {
  router.push({
    name: 'ManufacturerDetail',
    params: { id: newFabricant.id }
  })
}

const handleClose = () => {
  router.push({ name: 'ManufacturerList' })
}
</script>