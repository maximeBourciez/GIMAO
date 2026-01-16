<template>
  <UtilisateurForm :utilisateur-id="userId" @updated="handleUpdated" @close="goBack" />
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router';
import UtilisateurForm from '@/components/Forms/UtilisateurForm.vue';

const route = useRoute();
const router = useRouter();

const userId = route.params.id;

const handleUpdated = (id) => {
  router.push({ name: 'UserDetail', params: { id } });
};

const goBack = () => {
  if (!userId) {
    router.push({ name: 'UserList' });
    return;
  }
  router.push({ name: 'UserDetail', params: { id: userId } });
};
</script>
