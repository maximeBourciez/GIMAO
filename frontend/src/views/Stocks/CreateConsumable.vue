<template>
  <ConsommableForm
   :magasins="magasins"
   @create="handleConsommableCreate" @close="handleClose" @magasin-created="handleMagasinCreated"/>
</template>

<script setup>
import ConsommableForm from '@/components/Forms/ConsommableForm.vue';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const router = useRouter();
const magasins = ref([]);
const api = useApi(API_BASE_URL);


// Handling des events émis par le formulaire
const handleConsommableCreate = () => {
  router.go(-1);
}

const handleClose = () => {
  router.go(-1);
}

// Fetch les données
const fetchMagasins = async () => {
  try {
    const response = await api.get('magasins/');
    magasins.value = response;
  } catch (error) {
    console.error('Erreur lors du fetch des magasins:', error);
  }
}

onMounted(() => {
  fetchMagasins();
});

</script>