<template>
  <v-app>
    <!-- Contenu principal -->
    <v-main>
      <v-container>
        <!-- Filtres et tableau -->
        <v-row>
          <!-- Colonne contenant les filtres -->
          <v-col cols="3">
            <v-card elevation="1" class="rounded-lg pa-2 mb-4">
              <v-card-title class="font-weight-bold text-uppercase text-primary">Filtre</v-card-title>
              <v-divider></v-divider>
              <v-list dense>
                <v-list-item
                  v-for="role in roles"
                  :key="role"
                  @click="filterByRole(role)"
                  :class="{ 'text-primary font-weight-bold': selectedRole === role }"
                >
                  <v-list-item-title>{{ role }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>

          <!-- Tableau des utilisateurs -->
          <v-col cols="9">
            <v-data-table
              :headers="headers"
              :items="filteredUsers"
              :items-per-page="5"
              class="elevation-1 rounded-lg"
              :loading="loading"
            ></v-data-table>
            <v-alert v-if="errorMessage" type="error" class="mt-2">
              {{ errorMessage }}
            </v-alert>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useApi } from '@/composables/useApi';
import { API_BASE_URL } from '@/utils/constants';

const headers = [
  { text: "Nom", value: "nom" },
  { text: "Role", value: "role" },
];

// États
const users = ref([]);
const roles = ref(["Tous"]);
const selectedRole = ref("Tous");
const errorMessage = ref("");

// API
const api = useApi(API_BASE_URL);
const loading = ref(false);

// Utilisateurs filtrés selon le rôle
const filteredUsers = computed(() => {
  if (selectedRole.value === "Tous") return users.value;
  return users.value.filter(u => u.role === selectedRole.value);
});

// Changement de filtre
const filterByRole = (role) => {
  selectedRole.value = role;
};

// Fonction pour récupérer les utilisateurs depuis le backend
const fetchUsers = async () => {
  loading.value = true;
  errorMessage.value = "";
  try {
    await api.get('utilisateurs/');
    console.log("Users API full value:", api.data.value);

    if (Array.isArray(api.data.value)) {
      // Transformation pour correspondre aux colonnes du tableau
      users.value = api.data.value.map(u => ({
        nom: `${u.prenom} ${u.nomFamille}`,
        role: u.role?.nomRole || u.role || '-', // adapte selon la structure
      }));
    } else {
      console.warn("Format inattendu ou data undefined", api.data.value);
      users.value = [];
    }
  } catch (err) {
    console.error(err);
    errorMessage.value = "Erreur lors du chargement des utilisateurs";
    users.value = [];
  } finally {
    loading.value = false;
  }
};



// Fonction pour récupérer les rôles depuis le backend
const fetchRoles = async () => {
  errorMessage.value = "";
  try {
    await api.get('roles/'); // les données sont maintenant dans api.data.value
    console.log("Roles API full value:", api.data.value);

    if (Array.isArray(api.data.value)) {
      const roleNames = api.data.value.map(r => r.nomRole);
      roles.value = ["Tous", ...roleNames];
    } else {
      console.warn("Format inattendu ou data undefined", api.data.value);
      roles.value = ["Tous"];
    }
  } catch (err) {
    console.error(err);
    errorMessage.value = "Erreur lors du chargement des rôles";
    roles.value = ["Tous"];
  }
};




// Récupération des données au montage
onMounted(() => {
  fetchRoles();
  fetchUsers();
});
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

/* Mettre en surbrillance le rôle sélectionné */
.v-list-item.text-primary {
  background-color: #E4E9FF;
  border-radius: 4px;
}
</style>
