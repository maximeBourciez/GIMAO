<template>
  <UtilisateurForm @created="handleCreated" @close="goBack" />
</template>

<script setup>
import { useRouter } from 'vue-router';
import UtilisateurForm from '@/components/Forms/UtilisateurForm.vue';

const router = useRouter();

const handleCreated = (created) => {
  if (created?.id) {
    router.push({ name: 'UserDetail', params: { id: created.id } });
  } else {
    router.push({ name: 'UserList' });
  }
};

const goBack = () => {
  router.push({ name: 'UserList' });
};
</script>
