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
                <v-list-item v-for="role in roles" :key="role" @click="filterByRole(role)">
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
            ></v-data-table>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'Users',
  data() {
    return {
      roles: ["Tous", "Magasinier", "Responsable GMAO", "Administrateur", "Technicien", "Opérateur"],
      headers: [
        { text: "Nom", value: "nom" },
        { text: "Role", value: "role" },
      ],
      users: [
        { nom: "Admin 1", role: "Administrateur" },
        { nom: "Admin 2", role: "Administrateur" },
        { nom: "Admin 3", role: "Administrateur" },
        { nom: "Responsable 1", role: "Responsable GMAO" },
        { nom: "Responsable 2", role: "Responsable GMAO" },
        { nom: "Technicien 1", role: "Technicien" },
        { nom: "Technicien 2", role: "Technicien" },
        { nom: "Magasinier 1", role: "Magasinier" },
      ],
      selectedRole: "Tous",
    };
  },
  computed: {
    filteredUsers() {
      if (this.selectedRole === "Tous") {
        return this.users;
      }
      return this.users.filter(user => user.role === this.selectedRole);
    },
  },
  methods: {
    filterByRole(role) {
      this.selectedRole = role;
    },
  },
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
</style>
