<template>
  <div>
    <!-- App Bar -->
    <v-app-bar app color="white" elevation="1">
      <v-app-bar-nav-icon @click="drawer = !drawer" />

      <v-toolbar-title class="font-weight-bold">
        {{ pageTitle }}
      </v-toolbar-title>

      <v-spacer />

      <!-- User avatar -->
      <v-avatar size="36" color="primary" class="mr-2">
        <v-img v-if="userPhotoUrl" :src="userPhotoUrl" cover />
        <span v-else class="text-white">{{ userInitials }}</span>
      </v-avatar>
    </v-app-bar>

    <!-- Navigation Drawer -->
    <v-navigation-drawer v-model="drawer" temporary app width="280">
      <v-list dense nav>
        <!-- Logo -->
        <v-list-item lines="two" @click="navigateTo('Dashboard')" style="cursor: pointer"
          class="d-flex flex-column align-center mb-4 py-4">
          <v-img :src="logo" contain max-width="80" class="mb-2" />
          <v-list-item-title class="font-weight-bold text-center text-h6">
            {{ appTitle }}
          </v-list-item-title>
        </v-list-item>

        <v-divider class="mb-2"></v-divider>

        <!-- Navigation items -->
        <v-list-item v-for="item in filteredNavigationItems" :key="item.name"
          @click="navigateTo(item.name, item.disabled)" :class="[
            { 'active-item': isActive(item.name) },
            { 'disabled-item': item.disabled }
          ]" class="my-1">
          <template v-slot:prepend>
            <v-icon>{{ item.icon }}</v-icon>
          </template>
          <v-list-item-title v-html="item.title"></v-list-item-title>
        </v-list-item>
      </v-list>

      <!-- User info at bottom -->
      <template v-slot:append>
        <v-divider></v-divider>

        <v-list dense>
          <v-list-item class="py-2" style="cursor: pointer" @click="goToMyUserDetail">
            <template v-slot:prepend>
              <v-avatar size="36" color="primary">
                <v-img v-if="userPhotoUrl" :src="userPhotoUrl" cover />
                <span v-else class="text-white">{{ userInitials }}</span>
              </v-avatar>
            </template>
            <v-list-item-title>{{ user.name }}</v-list-item-title>
            <v-list-item-subtitle>{{ user.role }}</v-list-item-subtitle>
          </v-list-item>

          <v-list-item @click="logout" class="logout-item">
            <template v-slot:prepend>
              <v-icon>mdi-logout</v-icon>
            </template>
            <v-list-item-title>Déconnexion</v-list-item-title>
          </v-list-item>
        </v-list>
      </template>
    </v-navigation-drawer>
  </div>
</template>

<script>
import { MEDIA_BASE_URL } from "@/utils/constants";

export default {
  name: "TopBar",

  data() {
    return {
      drawer: false,
      appTitle: "GIMAO",
      logo: require("@/assets/images/LogoGIMAO.png"),
      navigationItems: [
        { name: "Dashboard", icon: "mdi-view-dashboard", title: "Tableau de bord", requiresPermission: null },
        { name: "EquipmentList", icon: "mdi-tools", title: "Équipements", requiresPermission: "eq:viewList" },
        { name: "FailureList", icon: "mdi-alert", title: "Demandes d'interventions (DI)", requiresPermission: "di:viewList" },
        { name: "InterventionList", icon: "mdi-wrench", title: "Bons de travail (BT)", requiresPermission: "bt:viewList" },
        { name: "UserList", icon: "mdi-account-cog", title: "Gestion des comptes", requiresPermission: "user:viewList" },
        { name: "Stocks", icon: "mdi-package-variant-closed", title: "Stocks", requiresPermission: "stock:view" },
        { name: "DataManagement", icon: "mdi-database-cog", title: "Gestion des données", requiresPermission: "loc:viewList" }
      ]
    };
  },

  computed: {
    pageTitle() {
      return this.$route.meta?.title || this.appTitle;
    },

    user() {
      const currentUser = this.$store.getters.currentUser;

      if (currentUser) {
        return {
          id: currentUser.id,
          name: `${currentUser.prenom} ${currentUser.nomFamille}`,
          role: currentUser.role?.nomRole || 'Utilisateur',
          photoProfil: currentUser.photoProfil || null,
        };
      }

      // Fallback: essayer de lire depuis localStorage
      const userFromStorage = localStorage.getItem('user');
      if (userFromStorage) {
        try {
          const userData = JSON.parse(userFromStorage);
          return {
            id: userData.id,
            name: `${userData.prenom} ${userData.nomFamille}`,
            role: userData.role?.nomRole || 'Utilisateur',
            photoProfil: userData.photoProfil || null,
          };
        } catch (e) {
          console.error('Error parsing user from localStorage:', e);
        }
      }

      return {
        id: null,
        name: 'Utilisateur',
        role: 'Non défini',
        photoProfil: null,
      };
    },

    userPhotoUrl() {
      if (!this.user?.photoProfil) return null;
      return `${MEDIA_BASE_URL}${this.user.photoProfil}`;
    },

    userInitials() {
      return this.user.name
        .split(' ')
        .map(word => word[0])
        .join('')
        .toUpperCase()
        .substring(0, 2);
    },

    filteredNavigationItems() {
      const role = this.user.role;
      return this.navigationItems.filter(item =>
        item.requiresPermission === null || this.$store.getters.hasPermission(item.requiresPermission)
      );
    }
  },

  methods: {
    isActive(routeName) {
      return this.$route.name === routeName;
    },

    navigateTo(routeName, disabled = false) {
      if (!disabled) {
        this.$router.push({ name: routeName });
        this.drawer = false;
      }
    },

    logout() {
      // Supprimer les données du store et du localStorage
      this.$store.dispatch('logout');
      this.drawer = false;

      // Rediriger vers login avec un reload complet pour nettoyer tout le state
      window.location.href = '/login';
    },

    goToMyUserDetail() {
      const id = this.user?.id;
      if (!id) return;
      this.drawer = false;
      this.$router.push({ name: 'UserDetail', params: { id } });
    }
  }
};
</script>

<style scoped>
.active-item {
  background-color: #5d5fef;
  color: white;

  &:hover {
    background-color: #5d5fef !important;
  }
}

.active-item .v-icon {
  color: white;
}

.disabled-item {
  pointer-events: none;
  opacity: 0.5;
  cursor: not-allowed;
}

.logout-item:hover {
  background-color: #f5f5f5;
}
</style>