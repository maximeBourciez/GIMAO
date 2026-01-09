<template>
  <ConsommableList 
    title="Gestion des Consommables" 
    create-button-text="Ajouter un consommable"
    @create="handleCreate" 
    @row-click="handleRowClick"
  />
</template>

<script setup>
import { useRouter } from 'vue-router';
import ConsommableList from '@/components/ConsommableList.vue';

const router = useRouter();

const handleCreate = () => {
  // TODO: Navigation vers la création d'un consommable
  console.log('Créer un consommable');
  // router.push('/CreateConsommable');
};

const handleRowClick = (item) => {
  // TODO: Navigation vers le détail d'un consommable
  console.log('Clic sur consommable:', item);
  // router.push({ name: 'ConsommableDetail', params: { id: item.id } });
};
</script>
  