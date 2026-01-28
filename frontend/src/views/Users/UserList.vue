<template>
  <BaseListView
    :title="title"
    :headers="headers"
    :items="filteredUsers"
    :loading="loading"
    :error-message="errorMessage"
    :show-search="true"
    :show-create-button="false"
    no-data-icon="mdi-account-off"
    :internal-search="true"
    @clear-error="errorMessage = ''"
    @row-click="goToAfficherUser($event.id)"
  >
    <template #before-table>
      <v-card elevation="1" class="rounded-lg pa-3 mb-4">
        <div class="d-flex align-center justify-space-between flex-wrap gap-2">
          <div class="text-subtitle-1 font-weight-bold text-primary">Filtrer par rôle</div>
          <v-chip-group v-model="selectedRole" mandatory selected-class="text-primary" class="role-chip-group">
            <v-chip
              v-for="role in roles"
              :key="role"
              :value="role"
              variant="outlined"
              size="small"
            >
              {{ role }}
            </v-chip>
          </v-chip-group>
        </div>
      </v-card>
    </template>

    <template #item.role="{ item }">
      <v-chip variant="outlined" size="small" color="primary">
        {{ item.role || '-' }}
      </v-chip>
    </template>

    <template #item.actif="{ item }">
      <v-chip
        variant="outlined"
        size="small"
        :color="item.actif ? 'success' : 'grey'"
      >
        {{ item.actif ? 'Oui' : 'Non' }}
      </v-chip>
    </template>
  </BaseListView>

  <!-- Bouton flottant en bas à droite -->
  <v-btn
    color="primary"
    size="large"
    icon
    class="floating-add-button"
    elevation="4"
    @click="goToCreerUser"
    v-if="store.getters.hasPermission('user:create')"
  >
    <v-icon size="large">mdi-plus</v-icon>
    <v-tooltip activator="parent" location="left">
      {{ createButtonText }}
    </v-tooltip>
  </v-btn>
</template>

<script setup>
import BaseListView from '@/components/common/BaseListView.vue';
import { ref, computed, onMounted } from 'vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';
import { useRouter } from 'vue-router';

// Données
const title = 'Gestion des comptes';
const router = useRouter();
const createButtonText = "Créer un nouvel utilisateur";

// Headers Vuetify 3 (même format que dans TABLE_HEADERS)
const headers = [
  { title: "Nom d'utilisateur", value: 'nomUtilisateur', sortable: true, align: 'start' },
  { title: 'Nom', value: 'nom', sortable: true, align: 'start' },
  { title: 'Rôle', value: 'role', sortable: true, align: 'center' },
  { title: 'Actif', value: 'actif', sortable: true, align: 'end' },
];

// États
const users = ref([]);
const roles = ref(['Tous']);
const selectedRole = ref('Tous');
const loading = ref(true);
const errorMessage = ref('');

// API
const api = useApi(API_BASE_URL);

// Utilisateurs filtrés selon le rôle
const filteredUsers = computed(() => {
  if (selectedRole.value === 'Tous') return users.value;
  return users.value.filter((u) => u.role === selectedRole.value);
});

const loadData = async () => {
  loading.value = true;
  errorMessage.value = '';

  const [rolesResult, usersResult] = await Promise.allSettled([
    api.get('roles/'),
    api.get('utilisateurs/'),
  ]);

  if (rolesResult.status === 'fulfilled' && Array.isArray(rolesResult.value)) {
    const roleNames = rolesResult.value
      .map((r) => r?.nomRole)
      .filter(Boolean);
    roles.value = ['Tous', ...roleNames];
  } else {
    roles.value = ['Tous'];
  }

  if (usersResult.status === 'fulfilled' && Array.isArray(usersResult.value)) {
    users.value = usersResult.value.map((u) => ({
      id: u?.id,
      nomUtilisateur: u?.nomUtilisateur ?? '-',
      nom: `${u?.prenom ?? ''} ${u?.nomFamille ?? ''}`.trim() || '-',
      role: u?.role?.nomRole || u?.role || '-',
      actif: Boolean(u?.actif),
    }));
  } else {
    users.value = [];
  }

  if (rolesResult.status === 'rejected' && usersResult.status === 'rejected') {
    errorMessage.value = 'Erreur lors du chargement des rôles et des utilisateurs.';
  } else if (rolesResult.status === 'rejected') {
    errorMessage.value = 'Erreur lors du chargement des rôles.';
  } else if (usersResult.status === 'rejected') {
    errorMessage.value = 'Erreur lors du chargement des utilisateurs.';
  }

  // Si le rôle sélectionné n'existe plus (ex: roles non chargés), on revient à "Tous"
  if (!roles.value.includes(selectedRole.value)) {
    selectedRole.value = 'Tous';
  }

  loading.value = false;
};

onMounted(() => {
  loadData();
});

const goToAfficherUser = (id) => {
  router.push({
    name: 'UserDetail',
    params: { id },
  });
};

const goToCreerUser = () => {
  router.push({ name: 'CreateUser' });
};
</script>

<style scoped>
.text-primary {
  color: #05004E;
}

.text-dark {
  color: #3C3C3C;
}

.v-card {
  background-color: #FFFFFF;
}

.v-btn {
  background-color: #F1F5FF;
  border-radius: 50%;
}

h1 {
  color: #05004E;
}

.role-chip-group {
  max-width: 100%;
}

.floating-add-button {
  position: fixed !important;
  bottom: 24px;
  right: 24px;
  z-index: 100;
}

.floating-add-button:hover {
  transform: scale(1.1);
  transition: transform 0.2s ease;
}
</style>
