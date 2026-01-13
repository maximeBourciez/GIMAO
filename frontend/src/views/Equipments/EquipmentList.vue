<template>
  <EquipmentFilteredList title="Liste des Équipements" :show-search="false" create-button-text="Ajouter un équipement"
    @create="handleCreate" @row-click="handleRowClick" />
</template>

<script setup>
import { useRouter } from 'vue-router';
import EquipmentFilteredList from '@/components/EquipmentFilteredList.vue';

const router = useRouter();

const handleCreate = () => {
  router.push('/CreateEquipment');
};

const handleRowClick = (item) => {
  router.push({ name: 'EquipmentDetail', params: { id: item.id } });
};
</script>