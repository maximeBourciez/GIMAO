<template>
  <FailureListComponent 
    @create="handleCreate"
    @row-click="handleRowClick"
    :showCreateButton="true" />
</template>

<script setup>
import { useRouter } from 'vue-router';
import FailureListComponent from '@/components/FailureListComponent.vue';

const router = useRouter();

const handleCreate = () => {
  router.push({ name: 'CreateFailure' });
};

const handleRowClick = (item) => {
  router.push({ name: 'FailureDetail', params: { id: item.id } });
};
</script>