<template>
  <BaseListView
    :title="title"
    :subtitle="subtitle"
    :headers="vuetifyHeaders"
    :items="displayUsers"
    :loading="loading"
    :error-message="errorMessage"
    :show-search="true"
    :show-create-button="false"
    table-class="bt-table"
    no-data-icon="mdi-account-outline"
    :no-data-text="noDataText"
    @row-click="onRowClick"
    @clear-error="errorMessage = ''"
  >
    <!-- Role -->
    <template #item.role="{ item }">
      <v-chip small outlined color="primary">{{ item.role }}</v-chip>
    </template>
  </BaseListView>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import BaseListView from '@/components/common/BaseListView.vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const props = defineProps({
  title: { type: String, default: 'Gestion des comptes utilisateurs' },
  subtitle: { type: String, default: '' },
  noDataText: { type: String, default: "Aucun utilisateur trouvé" },
});

const emit = defineEmits(['row-click']);

// API composable
const api = useApi(API_BASE_URL);

// États
const users = ref([]);
const roles = ref(["Tous"]);
const selectedRole = ref("Tous");
const errorMessage = ref("");

// Loading depuis useApi
const loading = computed(() => api.loading.value);

// Récupération des utilisateurs
const fetchUsers = async () => {
  errorMessage.value = "";
  try {
    const response = await api.get('utilisateurs/');
    users.value = response.data; // [{ nom, role }, ...]
  } catch (err) {
    console.error(err);
    errorMessage.value = "Erreur lors du chargement des utilisateurs";
  }
};

// Récupération des rôles
const fetchRoles = async () => {
  try {
    const response = await api.get('roles/');
    roles.value = ["Tous", ...response.data]; // Ajout de "Tous"
  } catch (err) {
    console.error(err);
    errorMessage.value = "Erreur lors du chargement des rôles";
  }
};

// Utilisateurs filtrés selon le rôle
const displayUsers = computed(() => {
  if (selectedRole.value === "Tous") return users.value;
  return users.value.filter(u => u.role === selectedRole.value);
});

// Gestion du clic sur une ligne
const onRowClick = (item) => emit('row-click', item);

// Monté du composant : récupération des données
onMounted(() => {
  fetchRoles();
  fetchUsers();
});
</script>

<style scoped>
.bt-table {
  width: 100%;
}
</style>
